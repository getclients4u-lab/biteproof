# 🛡️ BiteProof™ — The Mosquito-Proof Home System™

**Built:** 2026-09-05 (nightly digital-business build by Archie for Castle)
**Live URL:** https://biteproof.vercel.app
**Payment link:** https://buy.stripe.com/test_7sY8wQ1IIcZtee33WL1Nu0k (Stripe TEST mode, $19)
**Data repo (private):** https://github.com/getclients4u-lab/biteproof-data
**Source repo (public):** https://github.com/getclients4u-lab/biteproof

---

## 1. The Niche — Why Now

**2026 West Nile virus outbreak.** The 2026 U.S. West Nile season is the most active
start in 22 years (highest early-season human case counts since ~2004), with dozens
of states reporting virus activity, local outbreaks declared (e.g., South Carolina's
Pee Dee region), and peak transmission happening **right now** (Aug–Sep). There is
**no vaccine and no treatment** — prevention is the entire game.

**The uptrending video targeted:** the viral TikTok from @wrdwnews12 covering the SC
West Nile outbreak (~2.5M views / ~136K likes) — the breakout clip of this outbreak
wave. Health anxiety + a giant "what do I actually DO?" information gap = perfect
info-product moment.

**Previous builds avoided:** gutmap (FODMAP), secondbloom (perimenopause), fallform
(September reset), dermcode (skincare), voiceshield, dopamine-reset, promptpay.

---

## 2. The Business

| | |
|---|---|
| **Business name** | BiteProof™ |
| **Product** | The Mosquito-Proof Home System™ |
| **Mechanism** | The 4-Ring Defense™ (Skin → Yard → Home → Season) |
| **Format** | 8 print-ready PDF tools (guides, checklists, cheat sheets, trackers) |
| **Price** | $19 launch (marked from $79 value) |
| **Guarantee** | 60-day Peace-of-Mind, keep-everything refund |
| **Compliance** | Educational prevention content aligned with CDC/EPA guidance; explicit "not medical advice" disclaimers |
| **Cost to build** | ~$0 (static site + serverless + GitHub; Stripe in test mode) |

**The 8 deliverables:**
1. `core-guide.pdf` — The BiteProof Core Guide (4-Ring Defense™ roadmap + 72-hr launch sequence)
2. `yard-audit.pdf` — The 15-Minute Yard Audit (5 zones, 60+ breeding sites)
3. `standing-water-kill-list.pdf` — The Standing-Water Kill List (weekly drain/tilt/treat + rain sweep)
4. `repellent-cheat-sheet.pdf` — The Repellent Cheat Sheet (decision tree + active decode + myth table)
5. `barrier-blueprint.pdf` — The Home Barrier Blueprint (screens/seals/fans + myth busting)
6. `bite-response-card.pdf` — The Bite Response & Red-Flag Card (bite care + when to call the doctor)
7. `outing-playbook.pdf` — The Outing & Travel Playbook (go-bag + cookout/camping/travel drills)
8. `season-tracker.pdf` — The 12-Week Season Tracker (weekly rhythm + family duty roster)

---

## 3. Order Stack (how it works)

- **Landing page** (index.html) → CTAs point to the **Stripe test payment link** ($19)
- Stripe → **webhook** `POST /api/webhook` (checkout.session.completed +
  async_payment_succeeded, HMAC-verified) → stores buyer in private `biteproof-data`
  repo (`buyers.json`), registers user with a generated access code
  (`users.json`), and **emails the buyer** their `BP-XXXXX-XXXXX` code via AgentMail
- Buyer clicks through to **thank-you.html** → **download.html** member area where
  they enter email + code → `/api/verify` → `/api/download` serves the PDFs
  (fetched from the private data repo — **never** from the public site; direct
  `/product/*.pdf` on the public site returns 404)
- **admin.html** (password-protected) → `/api/admin`: view orders/users, grant
  manual access codes

**Env vars (Vercel):** `GH_TOKEN`, `GH_OWNER`, `GH_DATA_REPO=biteproof-data`,
`ACCESS_PEPPER=<secret, set in Vercel env>`, `STRIPE_WEBHOOK_SECRET`,
`AGENTMAIL_API_KEY`, `BITEPROOF_MAIL_FROM=gentledesk632@agentmail.to`,
`ADMIN_PASSWORD`.

**E2E status:** simulated purchase via signed Stripe event → `{"received":true,
"stored":1,"registered":1,"emailed":true}`; Castle (heyeverlastingmemories@gmail.com)
added via admin API; code verify `ok:true`; PDF download 200 + valid PDF; wrong
code → 403; public `/product/*.pdf` → 404. Test buyers cleaned; only Castle remains.

---

## 4. Launch Assets

- **Landing page:** `index.html` (long-form, conversion-optimized, 6 CTAs → payment link)
- **Emails:** `emails/launch-emails.md` — 3-email sequence (Teaser / Launch / Follow-up)
- **VSL:** `vsl/vsl-script.md` — 5-minute VSL script + 90-slide storyboard targeting
  the viral SC West Nile video; `vsl/vsl-slideshow.mp4` — rendered silent UPPERCASE
  slideshow (1920×1080, 4:57, ~4.4MB). Voiceover (ElevenLabs voiceId
  PeMXWXe7DDCb8HldBr2s) can be dropped onto the slideshow when a key is available.
- **Backend:** `api/` (hub.js, webhook.js, verify.js, admin.js, download.js) —
  proven gutmap architecture, fully adapted (BP- codes, FILES list, email body,
  brand references). `node --check` clean on all JS + inline HTML scripts.

---

## 5. Admin & Ops for Castle

- **Admin panel:** https://biteproof.vercel.app/admin.html (password = ADMIN_PASSWORD env)
- **Orders/users live in:** private repo `getclients4u-lab/biteproof-data`
  (`buyers.json`, `users.json`)
- **Regenerate access:** admin panel → "Add User" → generates code instantly
- **Refunds:** handled manually via Stripe dashboard (test mode)
- **Rebuild/update:** push to `getclients4u-lab/biteproof` → Vercel auto-deploys

---

*BiteProof™ is an educational prevention system, not medical advice. Follow CDC,
EPA, and local health department guidance; consult a healthcare provider for any
health concerns. © 2026 BiteProof™. Built nightly by Archie for Castle 🏛️*
