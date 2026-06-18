---
name: design-principles
description: A product and UX design constitution — the principles that guide any interface, dashboard, prototype, or user flow you build or review. Apply when designing or critiquing app UI, deciding what to actually build for a user, running a design process (research, define, sketch, prototype, test, deliver), laying out data visualizations, or judging whether a design is simple, consistent, and action-first. Encodes action-first (not data-first) UX, progressive disclosure, informed simplicity, form-from-function beauty, Nir Eyal's two behavior levers (ease and motivation), in-product education and NUXs, mobile-vs-web tradeoffs, app-agnostic integration rules, Material data-viz accessibility, and a friendly-and-concise copy style. Triggers — 'design principles', 'apply our design principles', 'review this design', 'critique this prototype', 'how should this screen work', 'what is the right UX for this', 'design this dashboard or flow', 'is this UI any good'.
license: MIT
metadata:
  source: Notion design principles. Distilled from Jon Yablonski (Laws of UX), Nir Eyal (Hooked), Paul Graham, Material Design.
---

A product and UX design constitution. Use it two ways: as a **decision lens** while designing (pick the action, apply the tiers, check the levers) and as a **review checklist** while critiquing (run the design against the Prime Directives, then the Key UX Principles, then Consistency). When giving feedback, cite the principle by name.

Good principles are direct and actionable, not bland and obvious. These are opinionated on purpose.

## Prime Directives (non-negotiable, ranked)

1. **Design what the user needs, not what they ask for.** Like a doctor: treat the disease, not the symptom the user reports. (Paul Graham)
2. **Action-first, not data-first.** Never just show charts. Show "what should I do next?" — every insight ends in a button.
3. **Informed simplicity.** Eliminate unnecessary complexity, but never simplify past the point where users lose the cues they need to make an informed decision. Abstraction that strips decision cues is worse than mild complexity. (Yablonski)
4. **Form from function.** Aesthetics serve the job. Fast and smooth *is* beautiful — never trade speed or robustness for looks.
5. **Consistency, internal and external.** Same physics everywhere (if one card uses a 10px radius, none uses 5px). Match the user's existing mental models from other apps. Start from conventions; depart only when you can make a compelling case it improves the core experience.

## Key UX Principles (apply to every screen)

| Principle | What it means in practice |
|-----------|---------------------------|
| **Action-First** | Pair every insight with a primary action ("Send Proposal", "Run Simulation", "Generate Plan"). No dead-end charts. |
| **Real-Time Urgency** | Surface time-sensitivity as a live signal — a countdown, a decaying metric ("deal prob: -8% per hour"). Color-code state: 🟢 safe → 🟡 warning → 🔴 urgent. |
| **Proactive Recommendations** | Surface opportunities the user didn't know to look for. "You're losing to competitor X" beats "here's the competitor data, you figure it out." |
| **One-Click Workflows** | Collapse a multi-step job into a single action with smart defaults ("Generate Plan" produces the full draft instantly; "Route to Building B" auto-sends the new info). |
| **Progressive Disclosure** | Three tiers: summary card (key metric + action button) → "View Details" expands the analysis → "See Analysis" opens the deep-dive (charts, tables, scenarios). |

## Simplicity & Beauty

- Friendly and welcoming, yet minimalist. Form from function.
- The interface should emulate real-world physics: dynamic motion that carries momentum, fluid state transitions.
- **Aesthetic-usability effect:** a pleasing design *feels* like it works better and buys tolerance for minor flaws — but never use polish to hide a real usability problem (it also hides problems from your usability tests).
- A busy interface (unclear actions, buried information) taxes the user's brain. Reduce that load.

## Behavior Design (why users act)

- **Two levers** (Eyal): the *ease* of doing the action × the *psychological motivation* to do it. To increase any behavior, raise one or both.
- **Habit loop:** solve the user's pain so reliably they associate the product with relief.
- **Robust input, structured output:** accept messy human input and translate it into clean, machine-friendly structure. Move the burden off the user; anticipate and plan for the things that will go wrong.
- **Two data rules:** (1) make it as easy as possible to collect behavior data; (2) make that data as useful and actionable as possible.

## Design Process (6 steps)

1. **Research** — understand the user and the problem.
2. **Define** — frame what's actually being solved.
3. **Sketch** — sketch separately, move to wireframes, then preliminary-test the wireframes with users and iterate.
4. **Prototype** — make wireframes hi-fi, close to the final deliverable. A developer should look at it and know exactly what to build.
5. **Test** — test the specific thing you're building: a linear flow of just what's needed. Collect qualitative (interviews, surveys, feelings) and quantitative (in-app observation, usage metrics) data, benchmark it, and socialize the results across the company.
6. **Deliver** — give developers what they ask for: written functionality description, a storyboard/flow diagram, and a pixel-spec mockup. Centralize all deliverable docs.

## Information Architecture (UX layout)

1. List the tasks users need to complete.
2. Rank tasks by how often they're performed.
3. Treat navigation as its own feature — decide what's always-accessible vs. contextual to certain pages.
4. Group similar functionality; divide pages into sections from those groups.
5. Break the customer journey into phases.
6. Align features to phases — ask when the user needs to know about each feature (right away? after an action? only if…?).

## In-Product Education

- Don't underestimate it. Surface contextual tips on the page the user is actually on.
- **Never leave null/empty states blank** — use them to educate or point the way.
- Trigger tips by engagement and usage patterns; track metrics to learn when and where to introduce them.
- **NUXs** (new-user experiences): dismissible prompts that persist until acknowledged — educate without being annoying.

## Data Visualization (Material accessibility guide)

1. **Facilitate comparisons** — arrange data so sets and points are easy to compare.
2. **Be a helpful guide** — right context at the right time; build affordances for comprehension and navigation.
3. **Focus on what matters** — prioritize accuracy, integrity, simplicity; every color/element should support the insight and cut cognitive load.
4. **Provide structure** — hierarchy makes the chart's purpose and elements legible.
5. **Embrace flexibility** — respect different needs on depth, complexity, and modality; let viz adapt over time.
6. **Exceed expectations** — dynamic, smart experiences that overdeliver.

## Platform: Mobile vs Web

- **Mobile:** every pixel counts; interactions must be concise and intuitive on a small screen.
- **Web:** flexibility — it must scale and adapt gracefully across devices, screen sizes, and contexts.

## Integrations (don't reinvent the wheel)

- If a popular app your users already use does it well, **integrate** with it.
- If most of your users live in another app daily, integrate with it.
- Build it internally only when you have a specific reason to believe you'll cut significant friction or improve the UX. Copy proven UX rather than inventing (e.g., model a scheduler on Google Calendar).

## Copy

Friendly and concise.

## What makes a good designer

- Decide from **reasoning + user feedback + aesthetic taste** — in that order, with taste affecting emotion.
- Form from function first.
- Treat visual attributes as a **tool**, not decoration.
