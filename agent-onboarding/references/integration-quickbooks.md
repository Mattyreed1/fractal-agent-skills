# Integration: QuickBooks Online

Not a channel — an external system the agent reads/writes. Build the connector as a **lean OAuth + scoped REST helper**, NOT the ~144-tool public QuickBooks MCP (a client already burned a day bouncing off that). It becomes a Hermes skill's `scripts/` helper (`~/.hermes/skills/quickbooks/`) — a small module that persists the rotated refresh token and auto-refreshes the access token (see Connector rules below).

## Intuit app
developer.intuit.com → create app → **QuickBooks Online and Payments** → scope **Accounting** (`com.intuit.quickbooks.accounting`; read+write covers transactions / vendors / accounts / classes / categories). Keys & credentials has **Development** (sandbox) + **Production** key sets. Add a redirect URI (the OAuth Playground URL is fine for the first token: `https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl`).

**⚠ App ownership + production gate (decide BEFORE the client call):** production keys are LOCKED until the app passes **App details** (~8 min; requires public **EULA + Privacy Policy URLs**) and a **Compliance questionnaire** (~40–50 min, security/data-handling self-attestation). Sandbox works instantly; real books do not. The vetting attaches to the APP, and **Intuit does not support transferring an app between developer accounts** — so for a client-owned agent, **create the app under the CLIENT's Intuit account** (their QBO login IS an Intuit developer login) and get added as a team member. The client then owns the app outright: when the engagement ends they just remove you, and nothing needs migrating. The operator drafts all compliance answers (they describe the operator's system); the client reviews/submits. The client's only live step, after keys unlock, is the OAuth consent for their company (~1 min, remote-friendly via link). A vendor-owned app is only right for a SaaS product serving many clients from one codebase.

## Tokens
OAuth 2.0 Playground → select app + Accounting scope → authorize the company → access token (~1h), refresh token (~100d, **rotates**), and the **realmId** (company id). Sandbox base URL `https://sandbox-quickbooks.api.intuit.com`; production `https://quickbooks.api.intuit.com`.

## Connector rules (get these right or it dies)
- **Persist the ROTATED refresh token on EVERY refresh** (atomic write to a local token store). Intuit hands back a new refresh token ~daily; drop it and the bot is locked out within days. **The #1 connector death.**
- Cache + auto-refresh the access token (~1h life); retry once on a 401.
- **Verify token refresh from the RUNTIME, not a dev laptop** — it must work where the agent actually runs.
- Secrets stay in the secret store / `~/.hermes/.env`, never pasted into chat or an agent's chat memory.

## Categorizer (guarded write-back)
- **Read path first, proven, before any write.** Dry-run / suggest-only for the first runs; **observe-only 24–72h** unless the client explicitly accepts the risk.
- Auto-apply only at **≥90% confidence**; below that, post a **channel escalation** with the proposed category, the rationale, the receipt/transaction context, and a structured answer path.
- **Learning loop = a rule with provenance:** who answered, message/thread id, transaction/merchant pattern, category/account/class, confidence impact, date, and a rollback/delete path. No opaque "AI learned it" state.
- **Receipt-capture → QBO:** map the source of truth; reconcile against QBO objects and preserve attachment/source links; watch duplicates, sync delays, vendor normalization, taxes, split transactions, classes/locations, and "already reviewed" state.

## Migration to the client (live, with them present)
- Client authorizes QuickBooks OAuth for the correct **production** company/realm (only they can).
- Swap `.env` Development → Production keys + the client's realmId.
- Confirm chart-of-accounts / category / class policy, the confidence threshold, and whether auto-apply starts on or observe-only.
