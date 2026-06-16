---
name: browser
description: Unified browser skill that routes between Claude in Chrome (authenticated browsing, form filling, real-browser interaction) and Playwright (headless screenshots, scraping, testing). Use when asked to browse websites, fill forms, take screenshots, or interact with web pages.
license: MIT
metadata:
  version: 2.0.0
---

# Browser

Unified browser automation skill. Routes between two backends based on the task.

## Triggers

- "browse to [URL]", "go to [site]", "open [URL]"
- "fill out this form", "fill in [form]", "submit [form]"
- "take a screenshot of [site]"
- "click [button/link]", "interact with [page]"
- "read this page", "what's on this page"

---

## Decision Tree: Which Backend?

```
TASK
 │
 ├─ Needs logged-in session / cookies?
 │   └─ YES → Claude in Chrome
 │
 ├─ Filling forms on a live site?
 │   └─ YES → Claude in Chrome
 │
 ├─ Interacting with JS-heavy SPA?
 │   └─ YES → Claude in Chrome
 │
 ├─ Need to see what user sees / debug UI?
 │   └─ YES → Claude in Chrome
 │
 ├─ Headless screenshot of public page?
 │   └─ YES → Playwright
 │
 ├─ Scraping / extracting data from public site?
 │   └─ YES → Playwright
 │
 ├─ Testing a localhost dev server?
 │   └─ YES → Playwright
 │
 └─ Mobile viewport / device emulation?
     └─ YES → Playwright
```

### Quick Decision Table

| Signal | Backend | Why |
|--------|---------|-----|
| Authenticated site (logged in) | Chrome | Has user's cookies/session |
| Form filling | Chrome | Handles JS validation, CAPTCHAs, dynamic fields |
| Public page screenshot | Playwright | Faster, headless, no Chrome needed |
| Scraping text/data | Playwright | Headless, scriptable, no UI overhead |
| localhost / dev testing | Playwright | Direct access, no extension needed |
| Mobile viewport | Playwright | Device emulation built-in |
| Multi-tab workflow | Chrome | Tab management via MCP |
| Click through a flow | Chrome | Sees rendered UI, handles popups |

---

## Branch 1: Claude in Chrome

Uses the Claude in Chrome extension MCP tools. Operates in the user's actual Chrome browser with full auth/cookies.

### Prerequisites
- Claude in Chrome extension installed and connected
- Chrome (or Brave) running
- Tools prefixed `mcp__Claude_in_Chrome__*`

### Core Workflow

```
1. Get tab context       → tabs_context_mcp (ALWAYS first)
2. Create or navigate    → tabs_create_mcp / navigate
3. Read the page         → read_page (accessibility tree) or get_page_text (raw text)
4. Find elements         → find (natural language element search)
5. Interact              → form_input / computer (click/type/scroll)
6. Verify                → read_page or screenshot to confirm
```

### Tool Reference

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `tabs_context_mcp` | Get tab IDs in MCP group | **ALWAYS call first** — required before any other tool |
| `tabs_create_mcp` | Open new tab with URL | Starting a new browsing task |
| `navigate` | Go to URL in existing tab | Changing pages in current tab |
| `read_page` | Get accessibility tree | Understanding page structure, finding elements |
| `get_page_text` | Get visible text content | Extracting text, reading articles |
| `find` | Find element by description | Locating form fields, buttons, links by natural language |
| `form_input` | Set form field value | Filling text inputs, selects, checkboxes |
| `computer` | Mouse/keyboard actions | Clicking buttons, typing, scrolling, submitting |
| `javascript_tool` | Run JS in page context | Custom DOM manipulation, reading values |
| `upload_image` | Upload image to file input | File upload fields |
| `read_console_messages` | Get browser console | Debugging JS errors |
| `read_network_requests` | Get network activity | Debugging API calls |

### Form Filling Pattern

```
Step 1: Get context
  → tabs_context_mcp { createIfEmpty: true }

Step 2: Navigate to form
  → navigate { url: "https://example.com/form", tabId: <id> }

Step 3: Read the page to understand form structure
  → read_page { tabId: <id> }

Step 4: Find each field and fill it
  → find { query: "email input field", tabId: <id> }
  → form_input { ref: <ref_from_find>, value: "user@example.com", tabId: <id> }

  → find { query: "name field", tabId: <id> }
  → form_input { ref: <ref_from_find>, value: "John Doe", tabId: <id> }

Step 5: Submit
  → find { query: "submit button", tabId: <id> }
  → computer { action: "left_click", ref: <ref>, tabId: <id> }

Step 6: Verify submission
  → read_page { tabId: <id> }  (check for success message)
```

### Tips for Claude in Chrome

- **Always start with `tabs_context_mcp`** — other tools fail without it
- **Use `find` with natural language** — "the email field", "submit button", "dropdown for country"
- **Use `read_page` after actions** to verify state changed
- **For dropdowns**: use `find` to locate, then `form_input` with the value, or `computer` with click + option selection
- **For multi-step forms**: read the page after each step to understand what's next
- **Screenshots**: use `computer { action: "screenshot" }` if you need visual confirmation
- **File uploads**: use `upload_image` for file input fields

### Anti-Patterns (Chrome)

| Avoid | Instead |
|-------|---------|
| Calling tools without `tabs_context_mcp` first | Always get context first |
| Guessing element refs | Use `find` to locate elements |
| Rapid-fire actions without reading | `read_page` between actions to verify state |
| Using Chrome for public page screenshots | Use Playwright — faster, no Chrome needed |

---

## Branch 2: Playwright (Headless)

Uses the Python Playwright script for headless browser automation. No auth, no cookies — fresh session every time.

### Prerequisites
- Python 3 with `playwright` installed
- Browser binaries: `playwright install chromium`
- Script: `~/.claude/skills/browser/scripts/browse.py`

### Screenshot (Quick)

```bash
python3 ~/.claude/skills/browser/scripts/browse.py <url> [output] [options]

Options:
  --full-page    Capture full scrollable page
  --mobile       Use iPhone 14 viewport
  --width N      Custom viewport width (default: 1280)
  --height N     Custom viewport height (default: 720)
```

Then view with the Read tool on the output file.

### Manual Script Pattern

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com')
    page.wait_for_load_state('networkidle')

    # Screenshot
    page.screenshot(path='/tmp/screenshot.png', full_page=True)

    # Interact
    page.fill('input[name="email"]', 'value')
    page.click('button[type="submit"]')
    page.wait_for_selector('.success-message', timeout=10000)

    browser.close()
```

### Mobile Viewport

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    device = p.devices['iPhone 14']
    browser = p.webkit.launch(headless=True)
    page = browser.new_page(**device)
    page.goto('https://example.com')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='/tmp/mobile.png')
    browser.close()
```

### Anti-Patterns (Playwright)

| Avoid | Instead |
|-------|---------|
| `headless=False` | Always `headless=True` |
| `wait_for_timeout()` | Use `networkidle` or `wait_for_selector` |
| Forgetting `browser.close()` | Always close browser |
| Not waiting for load | Always `wait_for_load_state('networkidle')` |
| `from playwright.sync_api import devices` | Use `p.devices['iPhone 14']` from playwright instance |
| Using Playwright for authenticated sites | Use Claude in Chrome instead |

---

## Examples

### Fill a form (Chrome)
```
User: "Fill out the contact form on example.com with my info"
→ Route: Claude in Chrome (form filling, may need interaction)
→ tabs_context_mcp → navigate → read_page → find fields → form_input → submit
```

### Screenshot a public page (Playwright)
```
User: "Take a screenshot of the Hacker News front page"
→ Route: Playwright (public page, no auth needed)
→ python3 browse.py https://news.ycombinator.com /tmp/hn.png --full-page
```

### Debug a localhost app (Playwright)
```
User: "Screenshot my app running on localhost:3000"
→ Route: Playwright (localhost, no auth)
→ python3 browse.py http://localhost:3000 /tmp/app.png
```

### Navigate an authenticated dashboard (Chrome)
```
User: "Go to my Notion workspace and check the Projects DB"
→ Route: Claude in Chrome (needs Notion auth cookies)
→ tabs_context_mcp → tabs_create_mcp → read_page → interact
```

### Extract text from a page (either)
```
Public page → Playwright (page.inner_text('body'))
Logged-in page → Chrome (get_page_text)
```
