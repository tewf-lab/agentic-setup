# Brief: review the literature for a work queue driven to a fixed point

**Shape:** [brief](https://github.com/Tewf/ai-augmented-project/blob/1a749dfcc4e182c7fe055e00aff3d937a68e5978/shapes/brief.md), pinned at the commit that added Cost, after v0.1.0.
**Kind:** review
**Repo:** localAI (the review moves to tewf-lab/agentic-setup once that repository has a first commit, localAI#59)
**Depends on:** none
**Outcome:** pending

## Task

tewf-lab/agentic-setup#1 asks which exact method makes the work a steering session does converge on the work asked,
without anyone listing it. The first hypothesis is a worklist loop to a fixed point: a program builds the queue from
every source of open work, the seat works it, done items close their source, new items enter, and the loop stops when
a rebuild adds nothing actionable. Review the academic and grey literature on it before any design.

## Decided

- Proof: reference (every claim cites a source that was fetched and read).
- Frameworks: the strands below; each source lists the framework it belongs to.
- Legality: none.
- Shapes to read: [frame](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/frame.md),
  [sources](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/sources.md),
  [state-of-the-art](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/state-of-the-art.md),
  [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/master/shapes/baseline.md)
- The strands, each with its frame, its surveys, the state of the art and a named baseline:
  1. worklist and fixed-point algorithms (data-flow analysis, chaotic iteration) and their termination;
  2. requirements traceability: request, issue, change, test;
  3. coverage metrics for a backlog worked by an agent;
  4. agent task loops in the grey literature (task-queue agents, long-running coding agents): how they decide they are
     done;
  5. hierarchical task decomposition (HTN planning, decomposition as needed), for an item too big for one job.
- Write only under `work/2026-11-25_queue-fixed-point/review/`. Do not edit `test_review.py`.

## To find

Four files under `review/`, each opening with a `**Shape:**` line that names its review shape:

- `frame.md`: the question, the five strands, what is in and out;
- `sources.md`: every source fetched, one line each, with its URL, its strand and one line on what it says; at least
  15 sources, academic and grey;
- `state-of-the-art.md`: per strand, what the best current method is and its known limits;
- `baseline.md`: the named baseline the method of agentic-setup#1 must beat, with the measure (coverage: items closed
  over items open at the start plus items created) and why it is the right one.

## Checks

- `python3 -m unittest discover -s work/2026-11-25_queue-fixed-point -p test_*.py`: the four files exist, each with its
  Shape line; `sources.md` holds at least 15 distinct URLs; `baseline.md` contains a line starting `**Baseline:**`.

## Cost

- Tokens: pending
- Dollars: pending
- Minutes: pending
- Produced: pending
