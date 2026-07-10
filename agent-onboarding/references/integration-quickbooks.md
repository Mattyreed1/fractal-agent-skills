# Integration: QuickBooks Online

Not a channel — an external system the agent reads/writes. Build the connector as a **lean OAuth + scoped REST helper**, NOT the ~144-tool public QuickBooks MCP (a client already burned a day bouncing off that). It becomes a Hermes skill's `scripts/` helper (`~/.hermes/skills/quickbooks/`) — a small module that persists the rotated refresh token and auto-refreshes the access token (see Connector rules below).

## Intuit app
developer.intuit.com → create app → **QuickBooks Online and Payments** → scope **Accounting** (`com.intuit.quickbooks.accounting`; read+write covers transactions / vendors / accounts / classes / categories). Keys & credentials has **Development** (sandbox) + **Production** key sets. Add a redirect URI (the OAuth Playground URL is fine for the first token: `https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl`).

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
