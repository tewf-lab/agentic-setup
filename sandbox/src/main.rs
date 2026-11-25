// task-sandbox, the launcher of issue 9 version 1 (research/sandbox/review.md, Position): the whole tree
// read-only, the task's declared edit set and its scratch folder writable, the never set read-only where it
// sits inside an edit path, the network closed unless declared, and the confinement that was applied written
// as a record an outside checker can re-derive. It fails closed — nothing runs unsandboxed — and the
// command's exit code is passed through as the launcher's own. Landlock's read/write split and seccomp are
// the versions after this one; version 1 is bubblewrap and the record.
#![forbid(unsafe_code)]

use std::env;
use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::os::unix::process::CommandExt;
use std::path::{Component, Path, PathBuf};
use std::process::{self, Command};

use serde::{Deserialize, Serialize};

const USAGE: &str = "usage: task-sandbox --root DIR --scope SCOPE.toml [--record FILE] -- COMMAND [ARGS...]";

/// A task's declared scope, in the grammar its brief already uses: paths to edit, paths never to touch, a
/// scratch folder that is writable but never judged, and whether the network is open. Every path is relative
/// to the root, and an absent field is read the least-privilege way (nothing, nothing, ".scratch", closed).
#[derive(Deserialize)]
struct Scope {
    #[serde(default)]
    edit: Vec<String>,
    #[serde(default)]
    never: Vec<String>,
    #[serde(default = "default_scratch")]
    scratch: String,
    #[serde(default)]
    network: bool,
}

fn default_scratch() -> String {
    ".scratch".to_string()
}

/// The confinement that was applied, written before the command runs so a checker outside the sandbox can
/// re-derive the scope from the same brief and compare: the result carries its own check.
#[derive(Serialize)]
struct Record {
    launcher: &'static str,
    read_only: Vec<String>,
    writable: Vec<String>,
    never: Vec<String>,
    network: bool,
    argv: Vec<String>,
}

/// The launcher's own command line: a root, a scope file, an optional record, and the command after --.
struct Cli {
    root: PathBuf,
    scope: PathBuf,
    record: Option<PathBuf>,
    command: Vec<String>,
}

fn value_of<'a>(args: &'a [String], i: &mut usize) -> Result<&'a str, String> {
    *i += 1;
    args.get(*i)
        .map(String::as_str)
        .ok_or_else(|| format!("{} needs a value\n{USAGE}", args[*i - 1]))
}

fn parse_cli(args: &[String]) -> Result<Cli, String> {
    let mut root = None;
    let mut scope = None;
    let mut record = None;
    let mut i = 0;
    let command = loop {
        let argument = match args.get(i) {
            Some(argument) => argument,
            None => return Err(format!("no command given\n{USAGE}")),
        };
        if argument == "--" {
            break args[i + 1..].to_vec();
        }
        match argument.as_str() {
            "--root" => root = Some(value_of(args, &mut i)?.to_string()),
            "--scope" => scope = Some(value_of(args, &mut i)?.to_string()),
            "--record" => record = Some(value_of(args, &mut i)?.to_string()),
            other => return Err(format!("unknown argument {other:?}\n{USAGE}")),
        }
        i += 1;
    };
    if command.is_empty() {
        return Err(format!("no command given\n{USAGE}"));
    }
    Ok(Cli {
        root: PathBuf::from(root.ok_or_else(|| format!("--root is required\n{USAGE}"))?),
        scope: PathBuf::from(scope.ok_or_else(|| format!("--scope is required\n{USAGE}"))?),
        record: record.map(PathBuf::from),
        command,
    })
}

/// bwrap must be on PATH before anything else is decided: if it is not, the task does not run at all, and
/// the message says so in the tool's own name rather than as a bare "not found".
fn find_bwrap() -> Result<PathBuf, String> {
    let path = match env::var_os("PATH") {
        Some(path) => path,
        None => return Err("no PATH to search for bubblewrap (bwrap) in; refusing to run unsandboxed".to_string()),
    };
    for directory in env::split_paths(&path) {
        let candidate = directory.join("bwrap");
        if let Ok(metadata) = fs::metadata(&candidate) {
            if metadata.is_file() && (metadata.permissions().mode() & 0o111) != 0 {
                return Ok(candidate);
            }
        }
    }
    Err("bubblewrap (bwrap) not found on PATH; refusing to run the command unsandboxed".to_string())
}

/// The root as an absolute path, lexically cleaned but not resolved: the bind mounts and the record speak
/// the paths the caller gave, while the containment check resolves them separately.
fn absolute(dir: &Path) -> PathBuf {
    let given = if dir.is_absolute() {
        dir.to_path_buf()
    } else {
        env::current_dir()
            .unwrap_or_else(|_| PathBuf::from("/"))
            .join(dir)
    };
    let mut clean = PathBuf::new();
    for component in given.components() {
        match component {
            Component::CurDir => {}
            Component::ParentDir => {
                clean.pop();
            }
            _ => clean.push(component.as_os_str()),
        }
    }
    clean
}

/// Whether a path under the root's lexical reach resolves outside it. Only the nearest existing ancestor
/// can be resolved; the components past it do not exist yet, and the launcher creates those itself as plain
/// folders, so they cannot carry a symlink out of the root.
fn resolves_outside(absolute: &Path, root_canonical: &Path) -> Result<bool, String> {
    let mut existing = absolute.to_path_buf();
    while fs::symlink_metadata(&existing).is_err() {
        let parent = match existing.parent() {
            Some(parent) => parent.to_path_buf(),
            None => return Err(format!("cannot look for {}", absolute.display())),
        };
        existing = parent;
    }
    let resolved = fs::canonicalize(&existing)
        .map_err(|error| format!("cannot resolve {}: {error}", existing.display()))?;
    Ok(resolved != root_canonical && !resolved.starts_with(root_canonical))
}

/// A declared path must be relative, free of .., and must not resolve through a symlink out of the root:
/// the brief's list is the whole of the authority, so a path that leaves the root is refused, not trimmed.
fn scope_path(root: &Path, root_canonical: &Path, given: &str, set: &str) -> Result<PathBuf, String> {
    let path = Path::new(given);
    if path.is_absolute() {
        return Err(format!("{set} path {given:?} is absolute; every scope path is relative to the root"));
    }
    if path.components().any(|component| matches!(component, Component::ParentDir)) {
        return Err(format!("{set} path {given:?} climbs out of the root with .."));
    }
    let absolute = root.join(path);
    if resolves_outside(&absolute, root_canonical)? {
        return Err(format!("{set} path {given:?} resolves outside the root"));
    }
    Ok(absolute)
}

fn create_dir_all(path: &Path, what: &str) -> Result<(), String> {
    fs::create_dir_all(path)
        .map_err(|error| format!("cannot create {what} at {}: {error}", path.display()))
}

fn read_scope(path: &Path) -> Result<Scope, String> {
    let text = fs::read_to_string(path)
        .map_err(|error| format!("cannot read the scope file {}: {error}", path.display()))?;
    toml::from_str(&text)
        .map_err(|error| format!("cannot read the scope file {} as a scope: {error}", path.display()))
}

fn run(args: &[String]) -> Result<(), String> {
    let cli = parse_cli(args)?;
    let bwrap = find_bwrap()?;
    let scope = read_scope(&cli.scope)?;
    let root = absolute(&cli.root);
    let root_metadata = fs::metadata(&root)
        .map_err(|error| format!("cannot read the root {}: {error}", root.display()))?;
    if !root_metadata.is_dir() {
        return Err(format!("the root {} is not a directory", root.display()));
    }
    let root_canonical = fs::canonicalize(&root)
        .map_err(|error| format!("cannot read the root {}: {error}", root.display()))?;

    let edit = scope
        .edit
        .iter()
        .map(|path| scope_path(&root, &root_canonical, path, "edit"))
        .collect::<Result<Vec<PathBuf>, String>>()?;
    let never = scope
        .never
        .iter()
        .map(|path| scope_path(&root, &root_canonical, path, "never"))
        .collect::<Result<Vec<PathBuf>, String>>()?;
    let scratch = scope_path(&root, &root_canonical, &scope.scratch, "scratch")?;

    create_dir_all(&scratch, "the scratch folder")?;
    for path in &edit {
        if fs::symlink_metadata(path).is_err() {
            create_dir_all(path, "an edit path")?;
        }
    }

    let writable = edit.iter().chain([&scratch]);
    let mut argv: Vec<String> = vec![bwrap.to_string_lossy().into_owned()];
    argv.extend(
        ["--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
            .iter()
            .map(|flag| flag.to_string()),
    );
    for path in writable.clone() {
        let bound = path.to_string_lossy().into_owned();
        argv.push("--bind".to_string());
        argv.push(bound.clone());
        argv.push(bound);
    }
    for path in &never {
        if fs::symlink_metadata(path).is_err() {
            continue; // a never path that is not there needs no mount to stay untouched
        }
        let bound = path.to_string_lossy().into_owned();
        argv.push("--ro-bind".to_string());
        argv.push(bound.clone());
        argv.push(bound);
    }
    if !scope.network {
        argv.push("--unshare-net".to_string());
    }
    argv.push("--die-with-parent".to_string());
    argv.push("--new-session".to_string());
    argv.push("--chdir".to_string());
    argv.push(root.to_string_lossy().into_owned());
    argv.extend(cli.command.iter().cloned());

    if let Some(record_path) = &cli.record {
        let record = Record {
            launcher: "bubblewrap",
            read_only: vec!["/".to_string()],
            writable: writable.map(|path| path.to_string_lossy().into_owned()).collect(),
            never: never
                .iter()
                .map(|path| path.to_string_lossy().into_owned())
                .collect(),
            network: scope.network,
            argv: argv.clone(),
        };
        let mut text = serde_json::to_string_pretty(&record)
            .map_err(|error| format!("cannot write the record {}: {error}", record_path.display()))?;
        text.push('\n');
        fs::write(record_path, text)
            .map_err(|error| format!("cannot write the record {}: {error}", record_path.display()))?;
    }

    // The launcher becomes the sandbox, so the command's exit code is the launcher's own.
    let mut sandbox = Command::new(&argv[0]);
    sandbox.args(&argv[1..]);
    let failure = sandbox.exec();
    Err(format!("cannot exec the sandbox {}: {failure}", argv[0]))
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if let Err(message) = run(&args) {
        eprintln!("task-sandbox: {message}");
        process::exit(2);
    }
}
