# Insight Taxonomy

This is the extraction engine's knowledge base. During Phase 1 (EXTRACT), scan the source material and tag every publishable insight with one of the 7 types below.

## The 7 Insight Types

### 1. Framework
A step-by-step process, numbered system, or mental model that can be taught.

**Detection heuristics:**
- "My process for X is..." / "The way I do X is..."
- Numbered steps or sequential logic
- Named systems or methodologies
- Repeatable patterns with clear inputs/outputs

**Content gravity:** HIGH (4-5). Frameworks are the most versatile insight type — they can drive threads, guides, checklists, skills, and workflows.

**Examples:**
- "My 3-step loop for debugging agents: observe, hypothesize, instrument"
- "The Control Loop: every agent needs a trigger, an action, a check, and a correction"
- "I audit every new client in 5 phases: time audit → bottleneck map → automation candidates → build → measure"

### 2. Contrarian Take
A statement that challenges conventional wisdom, common practice, or popular opinion.

**Detection heuristics:**
- "Most people think X, but actually..."
- "Everyone says X. I disagree because..."
- Challenges to popular tools, methods, or beliefs
- "Stop doing X" statements

**Content gravity:** HIGH (4-5). Contrarian takes drive engagement because they create tension. Best for LinkedIn hooks.

**Examples:**
- "MCP servers are overhyped for 90% of use cases — direct API calls are simpler and more reliable"
- "Building agents without a control loop is like driving without brakes"
- "The best agent skill isn't the most sophisticated one — it's the one that saves you 10 minutes every day"

### 3. Aha Moment
A surprising realization, paradigm shift, or "I didn't expect that" discovery.

**Detection heuristics:**
- "I realized that..." / "The moment I understood..."
- Tone shift in the conversation — excitement, surprise
- Non-obvious connections between two things
- "I was wrong about X" admissions

**Content gravity:** MEDIUM-HIGH (3-4). Aha moments make great hooks and turns in LinkedIn posts.

**Examples:**
- "The moment I realized the bottleneck wasn't the model, it was the prompt structure"
- "I thought I needed a better LLM. Turns out I needed better error handling."
- "The real value of BIM wasn't the 3D model — it was the data layer underneath"

### 4. War Story
A specific narrative with tension and resolution. Something that happened, went wrong, or surprised.

**Detection heuristics:**
- "Last week..." / "When we shipped X..." / "On our first client project..."
- Specific timelines, names, or events
- Problem → attempt → failure/success → lesson structure
- Emotional texture — frustration, relief, surprise

**Content gravity:** HIGH (4-5). War stories are the most engaging content type because they're specific and human. They make great LinkedIn post bodies and mini-guide case studies.

**Examples:**
- "We shipped the workflow on Friday. By Monday, it had processed 200 customer responses — but 15% were wrong. Here's what we missed."
- "My first n8n automation took 3 weeks to build. The same pattern now takes me 2 hours."
- "A client asked me to automate their bid review process. I said 2 weeks. It took 6. Here's why."

### 5. Data Point
A specific number, metric, benchmark, or measurable outcome.

**Detection heuristics:**
- Specific numbers: "45 minutes → 3 minutes", "200 responses per day"
- Before/after comparisons
- Time savings, cost reductions, error rate improvements
- Benchmarks or comparisons

**Content gravity:** MEDIUM (3). Data points are supporting evidence — they strengthen other insight types but rarely stand alone. Best paired with war stories or frameworks.

**Examples:**
- "Went from 45min to 3min per customer response"
- "The automation handles 200 daily requests with a 2% error rate"
- "Reduced manual data entry by 80% — 12 hours/week reclaimed"

### 6. Tool/Tactic
A specific tool, configuration, technique, or implementation detail worth sharing.

**Detection heuristics:**
- Named tools, nodes, or configurations
- "I use X for Y" patterns
- Specific settings, parameters, or configurations
- Tips, tricks, or non-obvious usage patterns

**Content gravity:** MEDIUM (2-3). Tools/tactics are useful as supporting details in threads and guides. Multiple related tools/tactics can form a cheat sheet.

**Examples:**
- "Using n8n's Error Workflow node to catch agent failures and alert Slack"
- "Set the AI Agent's maxIterations to 5 — any higher and you're burning tokens on loops"
- "The `waitForCompletion` parameter in the HTTP Request node saves you from polling"

### 7. Principle
A timeless observation, rule of thumb, or philosophical insight about how things work.

**Detection heuristics:**
- Universal statements: "Every X needs Y" / "The best X always..."
- Distilled wisdom from experience
- Applicable beyond the specific context
- Often appears at the end of a story or discussion

**Content gravity:** MEDIUM-HIGH (3-4). Principles make great takeaway lines in LinkedIn posts and section headers in guides.

**Examples:**
- "Every agent needs a control loop, not just a prompt"
- "The companies that capture what their best people know and make it repeatable will win"
- "Automation doesn't replace judgment — it frees up time for better judgment"

## Scoring: Content Gravity

Rate each extracted insight 1-5 on how much standalone content value it carries:

| Score | Meaning | Can It Stand Alone? |
|-------|---------|-------------------|
| 1 | Supporting detail | No — needs context from other insights |
| 2 | Useful tip | Barely — might work as a single tweet |
| 3 | Solid insight | Yes — can anchor a section of a post |
| 4 | Strong anchor | Yes — can drive an entire LinkedIn post |
| 5 | Content goldmine | Yes — can drive a post AND a lead magnet |

## Extraction Output Format

For each insight found, record:

```
### Insight {N}
- **Type**: {Framework | Contrarian Take | Aha Moment | War Story | Data Point | Tool/Tactic | Principle}
- **Gravity**: {1-5}
- **Summary**: {One line — the publishable insight}
- **Raw quote**: "{Exact passage from source}"
- **Lead magnet candidate?**: {Yes/No — could this become a workflow, DB, skill, checklist, or guide?}
```

## Phase 1 Gate
- Minimum 3 insights extracted
- At least 2 different types represented
- At least 1 insight with gravity ≥ 4
- If these minimums aren't met, tell the user: "This source doesn't have enough publishable material for the content engine. Consider adding more context or using a different conversation."
