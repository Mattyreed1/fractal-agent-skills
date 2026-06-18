# Diagram types — when to use each, and how to make it look great in D2

Pick the type that matches the *substance*, then apply the design system (`design-heuristics.md`),
the node classes (`node|focal|data|gate|external|group`), and the edge classes (`flow|accent|feedback|dataflow`).

**Worked, rendered examples of every type live in `examples/`** (`.d2` source + `.png`). Copy the
nearest one and adapt it — it already has the classes, layout engine, and conventions baked in.

---

## Flowchart / process

**Use for:** a sequence of steps with branches, decisions, and feedback loops.
→ `examples/flowchart.d2`

- `direction: down`. Keep the main path on a straight spine; branch the decision to the side.
- Steps = `class: node` (all the **same shape** — number them `1 ·`, `2 ·` to show order). The decision = `class: gate` (diamond); the outcome = `class: focal`.
- **Hexagon is reserved for a service/engine/transform** — don't use it for an ordinary pipeline step (a lone hexagon among rectangles reads as arbitrary).
- **One back-edge max.** Each feedback edge (`class: feedback`) makes dagre staircase the spine; keep the one that matters (`revise`) and push other loops into prose. A terminal write to a store = `class: dataflow` (`log` → `class: data` cylinder).
- Keep it to ~6–10 nodes. More than that → split or use architecture.

## Architecture / system

**Use for:** components and how data/control flows between them.
→ `examples/architecture.d2`

- `direction: right` (or `down` for tall systems). Group subsystems in `class: group` containers.
- **Group the data stores together** in one `class: group` boundary (e.g. "SHARED MEMORY") so the storage layer reads as one thing instead of scattered cylinders.
- Services/engines = hexagon; data stores = `class: data` (cylinder); external systems/actors = `class: external` (person/cloud, dashed).
- The **focal** = the core system/value (one node). Everything feeding it stays quiet.
- Encode flow vs data with edge classes: `flow` (solid) for control, `dataflow` (dashed) for data/async, `accent` for the one edge into the focal.
- Dagre is usually more compact here; ELK gives a straight spine but tends to wrap side-edges around the whole perimeter. Default to dagre, try `--layout elk` only if the spine matters more than compactness.

## Sequence

**Use for:** time-ordered interactions between actors (API calls, agent handoffs, protocols).
→ `examples/sequence.d2`

- Native: `shape: sequence_diagram` with actors as children and ordered messages.
- **Give the container a real label** — its id renders as the diagram title, so an unlabeled `seq:` shows a useless "seq" heading. Name it `handoff: Content handoff { shape: sequence_diagram ... }`.
- **One focal actor** — usually the human/initiator (`class: focal`); the rest are `class: node` (quiet). Don't let the theme paint every lifeline teal.
- Edge classes still apply: `accent` for the human touchpoints, `flow`/`dataflow` for requests/responses.
- **Group related messages** in a labeled sub-map to cluster a sub-protocol (e.g. wrap the two agent-to-agent messages in `"the agent fleet execution": { ... }`).
- Keep actor count ≤ 5.

```d2
handoff: Content handoff {
  shape: sequence_diagram
  matty: the user { class: focal }
  ea: EA { class: node }
  co: CO { class: node }
  matty -> ea: approve { class: accent }
  ea -> co: delegate { class: flow }
  co -> ea: for review { class: dataflow }
}
```

## Knowledge graph / network

**Use for:** entities and relationships with no strict hierarchy (KG, org maps, dependency webs).
→ `examples/knowledge-graph.d2`

- Nodes = circles (`shape: circle`). **Set explicit, uniform `width`/`height`** (e.g. 180) on every circle — D2 sizes a circle to its label by default, so without this a long name balloons and falsely implies importance. Size the focal one notch larger (e.g. 200) so size *means* "this is the subject."
- Make the circles big enough that the **longest label fits inside** (a 15-char label needs ~180–200px), or it spills below the node.
- One focal entity (the subject) `class: focal`; exactly one `accent` edge (the primary relationship), the rest `flow`/`dataflow`. Label every edge with the relationship (`owns`, `runs`).
- **D2 (OSS) has no radial/force layout** — both dagre and ELK lay out top-down/layered. Dagre's organic curves read more like a relationship web; ELK's right-angles read like a hierarchy. Prefer dagre for a KG. For a true radial graph, render to SVG and arrange in a Tier-2 frame.

## Decision tree

**Use for:** branching logic / "if this then that".
→ `examples/decision-tree.d2`

- `direction: down`. Every branch point = `class: gate` (diamond); leaves = `class: node`, the recommended leaf = `focal`. A dead-end / reject leaf = `class: external` (dashed) so it reads as "out of the flow."
- **Consistent exits:** pick a side and hold it — `yes` always one way, `no` the other (declaration order nudges dagre).
- **Glow the success path.** Every edge on the route to the focal = `class: accent`; reject/detour edges = `flow` (muted). The eye should trace one continuous bright thread to the outcome.
- Label every branch edge (`yes`/`no`, ranges).

## Swimlane

**Use for:** a process that crosses teams/systems (who does what, in order).
→ `examples/swimlane.d2`

- Lanes = `class: group` containers (one per actor); steps live inside their lane; edges cross lanes to show handoffs.
- **Render with ELK** — add `vars: { d2-config: { layout-engine: elk } }` to the diagram. ELK's layered orthogonal layout aligns the lanes into equal bands with clean right-angle handoffs; dagre leaves them as ragged diagonals. This is the one type where ELK clearly beats dagre.
- The cross-lane handoff edges are the story — `accent` the critical one (the approval / commit), the rest `flow`.
- **Limit:** even with ELK, D2 has no real swimlane primitive (no shared time-axis columns). For a strict swimlane with an aligned timeline, build it as a Tier-2 HTML/CSS grid — see `social-canvas-embed.md`.

## Timeline / state machine

**Use for:** stages over time, or states + transitions.
→ `examples/state-machine.d2`

- Timeline: `direction: right`, steps as a straight chain; the current/target state = `focal`.
- State machine: **every state is the SAME shape** (`class: node`). Do *not* make a state a `gate` (diamond) — a diamond reads as a decision, but "In review" is a state, not a branch.
- Mark the **initial state** with a small filled dot (`shape: circle; width: 22` styled inline) → first state; the **goal/accept** state = `focal`.
- Transitions = labeled edges. Distinguish the back-edges: rework/kickback = `class: feedback` (amber), a re-enter-the-cycle edge = `class: dataflow` (muted). Self-loops for "stay".

---

## Quick chooser

| You have… | Use |
|-----------|-----|
| Steps with decisions | Flowchart |
| Components + data flow | Architecture |
| Who-calls-whom over time | Sequence |
| Entities + relationships | Knowledge graph |
| Branching logic | Decision tree |
| Cross-team process | Swimlane |
| Stages over time / states | Timeline / state machine |
