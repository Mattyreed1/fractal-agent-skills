# Channel: WhatsApp

Hermes has **two** WhatsApp paths. Pick by whether you need fastest-to-live or official/scalable. Re-verify against current docs before executing; Meta's console drifts.

## A) Baileys bridge (unofficial WhatsApp Web) — fastest, no Meta account
Emulates a WhatsApp Web session, like linking a device. **No Meta developer account, no public webhook.**
1. `~/.hermes/.env`:
   ```
   WHATSAPP_ENABLED=true
   WHATSAPP_MODE=bot            # or "self-chat"
   WHATSAPP_ALLOWED_USERS=15551234567   # comma-separated numbers, or "*" for all
   ```
2. Run `hermes whatsapp` → **scan the QR** from your phone (WhatsApp → Settings → Linked Devices). Session saves to `~/.hermes/platforms/whatsapp/session`.

**Prereqs:** Node.js v18+, a **dedicated phone number** for bot mode, a phone with WhatsApp installed.
**Caveat:** unofficial (WhatsApp-Web emulation). Fine for internal/small use; not the official-support path, and a WhatsApp policy change could break it.

## B) WhatsApp Business Cloud API (official Meta) — scalable, supported
Requires a **Meta Business account + a public webhook URL**. Hermes has a `setup_whatsapp_cloud` CLI. The exact credentials (access token, phone number ID, business account ID, webhook verify token, app secret) and steps are in the separate Hermes guide — **VERIFY there before executing, don't guess Meta's console:** `https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp-cloud`.

## Which to use
For a client-owned agent, **Baileys with a dedicated phone number** is usually the quickest live path. Move to the Cloud API when they need official support, scale, or template messaging.
