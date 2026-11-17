# BookSaga — Product, Plans, OTO & Bonus — Complete Guide

> **Ye file kis liye hai:** ek hi jagah pe poora product samajhne ke liye — product kya hai, kya banata hai, kitne plans hain, har OTO me kya milta hai, bonus ka actual status kya hai, pricing, credits, guarantee, aur launch se pehle kya pending hai.
>
> **Kiske liye:** owner, marketing team, JV/affiliate partner, support, aur naya team member.
>
> **Source of truth:** `packages/shared/src/plans.ts` (plans + credits), `docs/PRD.md` (funnel §3.1, entitlements §3.2, credits §4.1), `docs/OTO_PAGES.md`, `docs/JV_LANDING_PAGE.md`, `docs/COST_REPORT.md`, `docs/TASKS.md`.
>
> **Aakhri update:** 17 Nov 2026 · **Status:** product built, launch infra pending (neeche §10)

---

## 0. Ek Nazar Me (TL;DR)

| Sawal | Jawab |
| --- | --- |
| Product kya hai? | **BookSaga** — ek AI web app jo **ek idea se poori connected book series** (Book 1 → Book N) likhta hai, covers + metadata + KDP-ready files ke saath. |
| Core USP | "One Idea → A Whole Series." Single book nahi — connected series, kyunki **read-through** se royalties multiply hoti hain. |
| Kis platform ke liye? | Amazon KDP (ebook + paperback + KU), plus audiobook (Google Play / Kobo / apni store). |
| Kitne plans? | **11 SKUs** = 1 FE + 5 OTO + 5 downsell. |
| Entry price | **$17** (BookSaga Basic) |
| Full funnel value | **$312** (FE + saare 5 full OTOs) |
| Downsell-only path | **$202** |
| Monthly fees? | **Nahi.** One-time payment, lifetime access. Credits bhi one-time (koi refill nahi). |
| Bonus stack? | **Product me koi separate bonus bundle nahi hai.** Jo "bonus jaisa" hai wo FE value stack ke andar included hai + ek **optional $9 order bump** (jo abhi bana nahi hai). Detail §6. |
| Guarantee | **30 din money-back**, ek email pe: `softwarevh@gmail.com` |
| Kya upload khud karna hai? | **Haan.** Amazon ka public publishing API nahi hai — user files download karke KDP pe upload karta hai. |
| Total value stacks | **$36,268** (saare value stacks ka sum) vs **$312** max cart |

---

## 1. Product Kya Hai

### 1.1 Ek Line Me

**Type one idea. Get a complete, KDP-ready book series tonight.**

Aap ek sentence likhte ho ("A cozy mystery series about a retired schoolteacher who runs a lakeside bookshop and keeps finding clues inside second-hand books"), genre aur kitni books chahiye — BookSaga series ka poora arc plan karta hai, Series Bible banata hai, Book 1 se Book N tak chapter-by-chapter likhta hai, har book ke baad continuity check karta hai, matching covers banata hai, aur EPUB/PDF/DOCX + metadata export karta hai.

### 1.2 Kaunsa Problem Solve Karta Hai

- **Standalone book = dead end.** Ek book bikti hai, reader chala jaata hai. Series me reader agla book kharidta hai.
- **Series likhna mushkil hai** — continuity (naam, umar, jagah, timeline) 4th book tak toot jaati hai.
- **Ghostwriter mehnga hai** — ek 5-book series $10,800–$31,500 aur 6–12 mahine.
- **AI tools ek-ek book banate hain** — koi series nahi, koi bible nahi, koi continuity nahi, covers match nahi karte.

BookSaga ka jawab: **series-first architecture.** Series plan pehle, Series Bible har chapter ke baad update, continuity check har book ke end pe, cliffhanger + "Read Next" page built-in, aur ek locked cover style jisse poori shelf match kare.

### 1.3 Kis Ke Liye Hai (PRD §2)

| Persona | Kya chahiye |
| --- | --- |
| KDP beginner | Pehli series bina likhe publish karni hai |
| Existing KDP publisher | Standalone nahi bik rahi, series chahiye |
| Faceless / pen-name publisher | Kai genres me kai pen names se publish karna hai |
| Agency / freelancer | Clients ke liye series likh ke bechni hai (OTO4) |
| Reseller | BookSaga ke licenses resell karne hain (OTO5) |

### 1.4 Product Actually Kya-Kya Deliver Karta Hai

**Books (manuscripts)**
- **Short:** ~12,000 words, 8–10 chapters
- **Standard:** ~30,000 words, 15–20 chapters
- **Full-length:** ~55,000 words, 25–30 chapters — *sirf OTO1 (Unlimited) me*
- Fiction + non-fiction, 15+ genres (fantasy, romance, cozy mystery, thriller, sci-fi, horror, paranormal, historical, YA, children's; self-help, business, health, devotional, how-to)
- Kisi bhi pen name se — faceless business chalane ke liye

**Series infrastructure**
- **Series plan / arc** — poori series ka map pehle
- **Series Bible** — characters, locations, world rules, timeline, open threads, glossary (non-fiction), style guide; version history + diff + restore; user edits AI kabhi overwrite nahi karta
- **Continuity check** — har book ke baad contradictions detect + fix; jo bache wo Continuity Report me "go to paragraph" link ke saath
- **Cliffhanger + "Read Next" page** — har chapter aage point karta hai, har book ke end me agle book ka teaser + link
- **Add More Parts** — series ko planned count se aage badhao (plan limit tak, hard max 30 books), 1 credit

**Covers**
- **Cover Studio** — AI art (text-less) + Konva layer editor (series name, title, "Book N", author, tagline)
- **Series Cover Style** — Book 1 se lock hota hai: art style, palette, fonts, positions, effects. Book 2..N same style follow karte hain
- **AI Text Mode** (optional) — model khud lettering render kare (spelling check karna padta hai)
- **Cover sources** — Auto (AI) / Library (pichhli images + presets) / Upload (apni image, max 10MB)
- **Image Editor** — crop, brightness/contrast, text, shapes, layers, ~30 self-hosted fonts
- **Paperback full-wrap cover PDF** — front + spine + back, 300 DPI, KDP print-ready — *sirf OTO1 / Unlimited Lite*
- **Box Set Builder** — 2+ books ka box set (combined TOC, dividers, 3D/flat cover, AI description) — *sirf OTO1 / Unlimited Lite*

**Listing / metadata**
- Har book ka title, subtitle, blurb (150–250 words), **7 KDP keywords**, **3 category suggestions**
- Metadata TXT + CSV (AI-disclosure note ke saath)

**KDP package (exports — sab free, 0 credits)**
| File | FE | OTO1 |
| --- | --- | --- |
| EPUB3 (epubcheck-clean, NCX + nav TOC) | ✅ | ✅ |
| Print interior PDF (5×8 se 6×9, mirrored margins, bleed, running headers) | ✅ | ✅ |
| DOCX (headings, page breaks, TOC field) | ✅ | ✅ |
| Ebook cover JPG 1600×2560 | ✅ | ✅ |
| Metadata TXT + CSV | ✅ | ✅ |
| Paperback full-wrap cover PDF | ❌ | ✅ |
| Box Set EPUB + cover | ❌ | ✅ |

- **KDP Preview** — pdf.js viewer (ebook + print mode) + pre-flight checks: page count, trim size, margins, cover dimensions, missing metadata, unresolved `{{NEXT_BOOK_URL}}` warning
- **KDP Upload Guide** — step-by-step: ebook create, series linking, paperback, KDP Select/KU, AI disclosure kahan bharni hai
- Exports 30 din tak rehte hain, re-export hamesha free

**Audiobook (OTO3)**
- Kokoro voices (US/UK English, male/female, preview ke saath), speed 0.8×–1.2×
- Per chapter MP3 192 kbps CBR, 44.1 kHz, mono
- **ACX technical specs** pe mastered: RMS −23 se −18 dB, peak ≤ −3 dB, noise floor ≤ −60 dB, room tone, opening/closing credits
- 2400×2400 square cover, in-app player + ZIP download

**Agency (OTO4)** — client accounts, agency credit pool, per-client allotment, suspend/activate, read-only view, client commercial license PDF

**Reseller (OTO5)** — license dashboard (create/track/revoke), franchise kit (sales page HTML, email swipes, social posts, banners, demo video link)

**App ke andar baaki**
- Dashboard (stat cards, recent series, part chips), My Series (grid/list, search, filter, duplicate, archive, soft delete + 30-day trash restore)
- TipTap chapter editor (autosave 3s, version snapshots) + AI tools: Rewrite / Expand / Shorten / Regenerate chapter
- Notifications (in-app bell, realtime), Global search ⌘K, Training module (YouTube/Vimeo lessons + progress)
- Profile: pen names CRUD, avatar, password
- Legal pages: Terms, Privacy, Refund, AI Content Disclosure (admin-editable)

---

## 2. Kaise Kaam Karta Hai

### 2.1 User Ke 3 Steps

1. **Log in** — browser me, kuch download nahi
2. **Idea type karo** — ek sentence + genre + kitni books (+ length, POV, tense, trim size, paper, bleed)
3. **Generate + publish** — Book 1 banti hai, phir Book 2..N; files download karke KDP pe upload

### 2.2 Andar Kya Hota Hai (pipeline)

```
Idea + genre + books count
        │
        ▼
Series Plan (poora arc, recurring cast, har book ka role)
        │
        ▼
Series Bible (characters, places, rules, timeline, threads)
        │
        ▼
Book 1 Outline → Chapter 1..N (sequentially, bible loaded har chapter me)
        │                    │
        │                    └─► har chapter ke baad facts extract → Bible update
        ▼
Continuity Check (bible ke against) → fix → Continuity Report
        │
        ▼
Metadata (title, blurb, 7 keywords, 3 categories)
        │
        ▼
Cover (series style + book scene) → Cover Studio edit → flatten JPG
        │
        ▼
Exports: EPUB3 + Print PDF + DOCX + cover + metadata CSV
        │
        ▼
Next part unlock (Part N tab hi banega jab N-1 ready ho — kyunki bible sequential update hoti hai)
```

**Important technical rules**
- Book generation **sequential** hai (ek waqt pe ek book job), taaki bible sahi order me update ho
- Per user: max **1 book generation job** + **3 cover jobs** ek saath
- Daily hard cap: **10 books/day** per user (admin-configurable)
- Job fail hone pe **credits auto-refund** + notification
- User cancel kar sakta hai: agar **<20% chapters** bane the to poora refund, warna nahi (dialog me clearly likha hai)

### 2.3 Asli Speed Aur Cost (measured, 23 Oct 2026)

Model: `deepseek/deepseek-v4.1-flash-1017` via OpenRouter, `AI_MODE=live`

| Preset | Words | Chapters | Time | AI calls | AI cost |
| --- | --- | --- | --- | --- | --- |
| Short (10 credits) | 13,262 | 9 | **16 min** | 30 | **$0.0979** |
| Standard (20 credits) | 32,436 | 18 | **26 min** | 45 | **$0.1560** |
| Full (35 credits) | 56,329 | 28 | **51 min** | 63 | **$0.2148** |

- Cover: ~**$0.012** per image (GPT Image 2, `low` quality, fixed — koi caller medium/high select nahi kar sakta)
- Standard book me sabse zyada kharch: chapters 48%, facts extract 25%, continuity 12%
- **Margin:** FE $17 / 300 credits = **$0.0567 per credit**. Standard book 20 credits = $1.13 revenue-equivalent vs $0.156 cost = **7.3× margin**. Full-length = 9.2×.

> Ye numbers marketing ke liye nahi hain — ye owner ke liye hain, taaki pricing decisions sahi ho. Public page pe sirf value/royalty illustrations jaate hain, income claims nahi.

---

## 3. Credits System (sabse important part)

### 3.1 Teen Pools

| Pool | Kya kharch hota hai |
| --- | --- |
| **main** | Books, covers, AI tools (enhance, rewrite, metadata, arc extend) |
| **audio** | Audiobooks (15 credits/book) |
| **agency** | Agency clients ke saare jobs (owner ke pool se) |

### 3.2 Credit Costs (admin-configurable, `credit_costs` table)

| Action | Kya hai | Credits | Pool |
| --- | --- | --- | --- |
| `book_short` | Short book (~12k words) | **10** | main |
| `book_standard` | Standard book (~30k words) | **20** | main |
| `book_full` | Full-length (~55k words) | **35** | main |
| `cover` | Cover generate / regenerate | **2** | main |
| `enhance` | Enhance with AI / AI suggestions | **1** | main |
| `rewrite` | Chapter rewrite / expand / shorten / regenerate | **1** | main |
| `metadata` | Title/blurb/keywords regenerate | **1** | main |
| `arc_extend` | Add More Parts | **1** | main |
| `audiobook` | Audiobook (per book) | **15** | audio |
| Series plan + Bible | Book 1 me included | **0** | — |
| Exports / re-exports | — | **0** | — |

### 3.3 Rules (PRD §4.2)

- **One-time grants, monthly nahi.** Plan grant hote hi credits ek baar add. Koi refill, reset, expiry nahi.
- **Credits stack hote hain.** FE + U-Lite + U = 300 + 1,000 + 3,000 = **4,300 main credits**.
- **Ek plan dobara grant karne se double credits nahi milte** (idempotent, `user_plan_id` unique).
- **Reserve → Commit → Refund:** job enqueue pe reserve, success pe commit, fail pe refund.
- **Refund/chargeback:** us plan ke diye credits wapas katte hain, par balance 0 se neeche nahi jaata (`deduct = min(balance, granted_by_that_plan)`).
- **Credit packs nahi hain.** Khatam hone pe "Not enough credits" + Upgrade CTA. Admin manually bonus/support credits de sakta hai (reason mandatory, ledger me log).
- **Agency clients:** apna pool nahi; owner ke agency pool se katte hain; owner per client **allotment** deta hai (default 100, kabhi bhi badha/ghata sakta hai).
- **Reseller customers:** FE features + **sirf 100 main credits** (normal FE buyer ko 300).

### 3.4 Credit Math (kaun kitna kaam kar sakta hai)

| Plan | Credits | Kitni books (with covers) |
| --- | --- | --- |
| FE Basic | 300 main | ~13 Standard / ~25 Short |
| OTO1 Unlimited | +3,000 main (total 3,300) | ~81 Full-length (grant se) / ~89 total |
| OTO1 Lite | +1,000 main | ~27 Full-length |
| OTO3 Audiobook | +1,000 audio | ~66 audiobooks |
| OTO3 Lite | +300 audio | ~20 audiobooks |
| OTO4 Agency | +5,000 agency | ~227 Standard books (clients ke liye) |
| OTO4 Lite | +2,000 agency | ~90 Standard books |
| OTO2 / OTO5 | 0 credits | — (feature-only add-ons) |
| Reseller customer | 100 main | ~4 Standard books |

*Formula: Standard book + cover = 22 credits · Full-length + cover = 37 · Audiobook = 15.*

**Sab kharidne pe total credits:** 300 + 3,000 + 1,000 + 1,000 + 300 + 5,000 + 2,000 = **12,600 credits**

---

## 4. Offer Ladder (Funnel)

```
FE  $17  BookSaga Basic
 │
 ├─► OTO1 $47  Unlimited            ── no-thanks ──► Downsell $27  Unlimited Lite
 │
 ├─► OTO2 $37  Done-For-You         ── no-thanks ──► Downsell $17  DFY Lite
 │
 ├─► OTO3 $47  Audiobook            ── no-thanks ──► Downsell $27  Audiobook Lite
 │
 ├─► OTO4 $67  Agency               ── no-thanks ──► Downsell $47  Agency Lite
 │
 ├─► OTO5 $97  Reseller + Franchise ── no-thanks ──► Downsell $67  Reseller Lite
 │
 └─► Members area / thank-you
```

| Step | Offer | Price | Downsell | DS Price |
| --- | --- | --- | --- | --- |
| 1 | FE — BookSaga Basic | **$17** | — | — |
| 2 | OTO 1 — BookSaga Unlimited | **$47** | Unlimited Lite | **$27** |
| 3 | OTO 2 — BookSaga Done-For-You | **$37** | DFY Lite | **$17** |
| 4 | OTO 3 — BookSaga Audiobook | **$47** | Audiobook Lite | **$27** |
| 5 | OTO 4 — BookSaga Agency | **$67** | Agency Lite | **$47** |
| 6 | OTO 5 — BookSaga Reseller + Franchise | **$97** | Reseller Lite | **$67** |

**Cart totals**
- FE only: **$17**
- Saare full OTOs: 17+47+37+47+67+97 = **$312**
- Saare downsells: 17+27+17+27+47+67 = **$202**
- Koi order bump nahi hai (current funnel me)

**Page order (har OTO page ka structure — 25 sections):** top bar + progress → congratulations → headline → video → CTA#1 → "where your plan stops" → problem → introducing → everything it unlocks → how it works → 3 deep dives → numbers → without vs with → ways to use → who it's for → what it costs elsewhere → value stack → price + CTA → guarantee → launch pricing → FAQ → final CTA + P.S. → no-thanks + downsell page.

---

## 5. Har Offer Ka Full Detail

### 5.1 FE — BookSaga Basic · **$17**

| | |
| --- | --- |
| Code | `fe` |
| Credits | **300 main** (one-time) |
| Active series | **3** |
| Books per series | **5** |
| Length presets | **Short + Standard** |
| Paperback wrap cover | ❌ |
| Box Set Builder | ❌ |
| Templates | ❌ (locked preview) |
| DFY packs | ❌ |
| Audiobook | ❌ |
| Agency / Reseller | ❌ |

**Value stack ($10,958 "real-world value")**

| Included | Value |
| --- | --- |
| Series Engine (idea → complete connected series) | $1,997 |
| Series Bible Generator (version history) | $997 |
| Continuity Check & Report | $997 |
| Cliffhanger & "Read Next" Engine | $697 |
| Matching Series Cover Studio (AI art + locked style + layer editor) | $997 |
| Image Editor (crop, text, shapes, layers, 30 fonts) | $297 |
| Titles, Blurbs, 7 Keywords & 3 Categories | $697 |
| KDP Export Pack (EPUB3, print PDF, DOCX, cover JPG, metadata CSV) | $997 |
| KDP Preview & Pre-Flight Checker | $497 |
| AI Chapter Editor (rewrite, expand, shorten, regenerate) | $497 |
| Fiction & Non-Fiction Modes (15+ genres) | $497 |
| Pen Name Manager (faceless business) | $297 |
| KDP Upload Guide + Training | $497 |
| Full Commercial Rights (100% royalties) | $997 |
| 300 one-time credits | Included |
| **Total** | **$10,958** |

**Marketing position:** "One idea. One whole saga. Ready for Amazon tonight." — no writing, no outlining, no plot holes, no ghostwriters, no monthly fees, lifetime access, 30-day guarantee.

---

### 5.2 OTO 1 — BookSaga Unlimited · **$47** (DS: Unlimited Lite **$27**)

**Kya unlock hota hai**
- ✅ **Full-Length Novels** — 25–30 chapters, ~55,000 words
- ✅ **30 Books Per Series** (5 se 30)
- ✅ **Unlimited Active Series** (3 se ∞)
- ✅ **Paperback Full-Wrap Cover PDF** — front + spine + back, 300 DPI
- ✅ **Box Set Builder** — 2+ books ka naya, higher-priced listing
- ✅ **3,000 Extra One-Time Credits**
- ✅ **Add More Parts** — series ko 30 tak extend karo

| | Basic | Unlimited |
| --- | --- | --- |
| Length | Short, Standard | Short, Standard, **Full** |
| Books/series | 5 | **30** |
| Active series | 3 | **∞** |
| Paperback wrap | ❌ | ✅ |
| Box sets | ❌ | ✅ |
| Credits | 300 | **3,300** |

**Value stack: $5,082** — Full-length engine $997 · 30 books + Add More Parts $697 · Unlimited series $697 · Paperback wrap $497 · Box Set Builder $697 · 3,000 credits $1,497

**Numbers jo page pe use hote hain**
- Ebook $4.99 @ 70% = ~$3.49/sale · Paperback $12.99 ≈ ~$4/sale · 5-book box set $9.99 ≈ ~$6.99/sale
- KU: short ~65 pages ≈ $0.29 · standard ~160 ≈ $0.72 · full ~290 ≈ $1.31 per full read
- 10-book full series ≈ 2,900 KENP pages vs 5-book short series ≈ 325 — **~9× page reads**

**Downsell — Unlimited Lite $27:** same formats (full-length, 30 books/series, wrap, box sets), par **25 active series** aur **1,000 credits** (~27 full-length books with covers).

**Honest caveat:** "Unlimited" ka matlab *active series* unlimited — books per series ka **hard system cap 30** hai (sab plans ke liye). Copy me "unlimited books" mat likhna.

---

### 5.3 OTO 2 — BookSaga Done-For-You · **$37** (DS: DFY Lite **$17**)

**Kya unlock hota hai**
- ✅ **120 Series Templates** — 12 categories × 10 (Fantasy, Romance, Mystery & Thriller, Historical, YA, Children's, Sci-Fi, Horror, Business & Money, Health & Wellness, Faith, Self-Help)
- ✅ **One-Click "Use This Template"** — Create Series form prefill (sab editable)
- ✅ **500+ DFY Series Ideas** by niche — title + premise + hook
- ✅ **Blurb Templates** by genre
- ✅ **Keyword Packs** by genre (7 KDP slots ke liye starting points)
- ✅ **Sample cover** har template ka
- ✅ New templates add hote rahenge (admin-managed)

**Har template me:** concept + hook, core cast, **5-book arc**, tone, target audience, sample cover, badge (Bestseller / Popular / New)

| | DFY Lite $17 | DFY $37 |
| --- | --- | --- |
| Series templates | **40** (lite tier) | **120** (full) |
| Series ideas / blurb / keyword packs | Lite selection | Full library |
| One-click prefill | ✅ | ✅ |

**Value stack: $4,782** — Templates $1,997 · 500 ideas $997 · Blurb templates $497 · Keyword packs $697 · Sample covers $297 · One-click prefill $297

**Numbers:** ek 5-book Standard series with covers = **110 credits** (300 ka ek-tihai se zyada). Galat idea pe kharch = paisa gaya. Template tested genre se shuru karo.

**Note:** Templates **sirf** DFY-Lite (40) aur DFY (120) me hain — Unlimited (OTO1) se templates **nahi** milte. Ye galti se bhi galat mat likhna.

---

### 5.4 OTO 3 — BookSaga Audiobook · **$47** (DS: Audiobook Lite **$27**)

**Kya unlock hota hai**
- ✅ **Audiobook Series Module** — koi bhi finished book narrate karo
- ✅ **Curated Natural AI Voices** — US + UK English, male/female, preview ke saath
- ✅ **Speed Control** 0.8×–1.2×
- ✅ **One MP3 Per Chapter** — 192 kbps CBR, 44.1 kHz, mono
- ✅ **ACX-spec mastering** — loudness normalised, peak-limited, room tone
- ✅ **Opening & Closing Credits** files
- ✅ **2400×2400 Square Cover**
- ✅ **In-App Player + ZIP Download**
- ✅ **1,000 one-time audio credits** (~66 audiobooks)

| | Audiobook Lite $27 | Audiobook $47 |
| --- | --- | --- |
| Studio, voices, mastering | ✅ | ✅ |
| Audio credits | **300** (~20 books) | **1,000** (~66 books) |

**Value stack: $4,182** — Studio $1,497 · Voices + speed $497 · ACX mastering $697 · Credits + cover $297 · Player + ZIP $197 · 1,000 credits $997

**Honest selling — ye page pe clearly likha hai (aur aage bhi likhna chahiye):**
- ❌ **Audible via ACX:** direct ACX upload human narration maangta hai (jab tak Audible authorize na kare). **BookSaga audio ACX pe upload mat karo.**
- ✅ **Google Play Books** — AI-narrated audiobooks accept karta hai, disclosure ke saath
- ✅ **Kobo** — narrator ko synthetic voice list karne pe
- ✅ **Apni store** (Payhip, Gumroad, Shopify, website) — ebook ke saath bundle
- ✅ **Reader magnet / bonus** — free audio prequel se list grow karo

> **Launch se pehle har store ki current AI-narration policy dobara verify karni hai** — ye ek legal/trust issue hai, marketing copy ka nahi.

---

### 5.5 OTO 4 — BookSaga Agency · **$67** (DS: Agency Lite **$47**)

**Kya unlock hota hai**
- ✅ **100 Client Accounts** — har client ka apna login
- ✅ **5,000 one-time agency credits** — alag pool
- ✅ **Per-Client Allotments** — default 100, kabhi bhi change
- ✅ **Copy Login Details** — seconds me onboarding
- ✅ **Suspend / Activate** clients
- ✅ **Read-Only View** client ki series ka
- ✅ **Client Commercial License (PDF)**
- ✅ **Clients ko aapke plan ke features milte hain** (Unlimited ho to client ko bhi full-length + 30-book series)

| | Agency Lite $47 | Agency $67 |
| --- | --- | --- |
| Client accounts | **25** | **100** |
| Agency credits | **2,000** | **5,000** |
| Allotments, oversight, license PDF | ✅ | ✅ |

**Value stack: $5,482** — 100 clients $1,997 · 5,000 credits $1,997 · Allotment controls $497 · Oversight $297 · License PDF $497 · Copy login $197

**Key mechanics**
- Client ke jobs **agency pool** se katte hain, aapke main credits safe
- Allotment ya pool khatam → client ko "Not enough credits, contact your agency"
- Clients Page: pool balance + har client ka allotment/used/remaining
- Client ka apna pool nahi hota; owner plan ke features/limits milte hain

---

### 5.6 OTO 5 — BookSaga Reseller + Franchise · **$97** (DS: Reseller Lite **$67**)

**Kya unlock hota hai**
- ✅ **100 Reseller Licenses** — har license ek BookSaga Basic account banata hai
- ✅ **Reseller Dashboard** — create, track, revoke
- ✅ **Revoke = license wapas** (refund case me useful)
- ✅ **Ready-Made Sales Page Template** (HTML download)
- ✅ **Promo Email Swipes**
- ✅ **Social Media Posts**
- ✅ **Banners & Ad Graphics**
- ✅ **Demo Video Link**
- ✅ **Keep 100% of what you charge**

| | Reseller Lite $67 | Reseller $97 |
| --- | --- | --- |
| Licenses | **50** | **100** |
| Dashboard | ✅ | ✅ |
| Franchise kit | ✅ | ✅ |

**Value stack: $5,782** — 100 licenses $2,997 · Dashboard $497 · Sales page $997 · Email swipes $497 · Social + banners $497 · Demo video $297

**Reseller customer ko kya milta hai (ye clearly bolna zaroori hai)**
- **BookSaga Basic** account: full series engine, Bible, continuity, covers, metadata, KDP exports
- Short + Standard lengths, **3 active series**, **5 books per series**
- **100 one-time credits** (direct Basic buyer ko 300)
- **Upgrades included nahi hain** — customer OTO nahi khareed sakta us account se

**Economics warning (COST_REPORT §3):** worst case = 100 customers × 100 credits = 1,000 Short books ≈ **$98 AI cost against $97 revenue**. Ye deliberate worst case hai, typical nahi — par launch ke baad data se re-check karna.

---

## 6. Bonus — Poora Sach (Important)

### 6.1 Short Answer

**Product me koi "bonus bundle" nahi hai.** Na FE pe, na kisi OTO pe. 11 SKUs hain — bas.

Jo "bonus" ke naam pe dikh sakta hai, wo teen categories me aata hai:

1. **Included value** (FE value stack ke andar already hai) — 300 credits, full commercial rights, lifetime access, training, KDP preview, image editor
2. **Ek optional $9 order bump** (Saga-Stacker Kit) — **copy likhi hui hai, product bana nahi hai**
3. **OTO ke andar "free" lagne wali cheezein** — jaise franchise kit, sample covers, template library — par ye paid add-ons hain, bonus nahi

### 6.2 Jo Cheezein "Free Bonus" Jaisi Lagti Hain (Aur Sach Me Included Hain)

| Cheez | Kahan milta hai | Status |
| --- | --- | --- |
| **300 one-time credits** | FE ($17) | ✅ Built |
| **Full commercial rights** — 100% royalties aapki | FE | ✅ Built (legal copy) |
| **Lifetime access, no monthly fees** | FE | ✅ Business decision |
| **KDP Upload Guide + Training** | FE (Training module) | ✅ Page built · ⚠️ **video lessons ka content admin ko daalna hai** |
| **KDP Preview + pre-flight checks** | FE | ✅ Built |
| **Cover Studio + Image Editor** (~30 fonts) | FE | ✅ Built |
| **Read Next / cliffhanger engine** | FE | ✅ Built |
| **Pen name manager (faceless)** | FE | ✅ Built |
| **10 starter series templates** (seeded) | Catalog | ✅ Seed script · ⚠️ **tier = lite**, yani DFY Lite ke bina FE buyer use nahi kar sakta |
| **Sample covers har template ka** | DFY | ✅ Seed script (paid add-on) |
| **Franchise kit** (sales page, swipes, banners, demo) | OTO5 | ✅ Built · ⚠️ **assets admin upload karega** — content ready karna hai |

### 6.3 Order Bump — "Saga-Stacker Kit" $9

**Kya hai (copy ke hisaab se):** niche list + 90-day release calendar + per-genre keyword sets + launch checklist — "ek series se stacking tak" ka playbook.

**Actual status:**
- `docs/JV_LANDING_PAGE.md` §40 me **poori copy likhi hui hai**
- **PRD §3.1 me order bump nahi hai** — funnel me sirf FE + 5 OTO + 5 DS
- App me bump product, checkout integration, ya delivery mechanism **bana hua nahi** hai
- Doc me hi note hai: *"sirf tab rakhna jab bump product actually bana ho… agar nahi banana to is section ko 'Fast-Start Training' free bonus bana do"*

**Teen options (decision chahiye):**

| Option | Kya karna hoga | Effort | Trade-off |
| --- | --- | --- | --- |
| **A. Bump banao ($9)** | Content banao (niche list, calendar, keyword sets, checklist) + checkout pe bump add karo + delivery (PDF/Notion) | Medium | Extra revenue per buyer, par launch se pehle content + checkout kaam |
| **B. Free bonus banao** | Wahi content banao, FE buyers ko free do, "Fast-Start Training" ke naam se | Low-Medium | Conversion + trust badhta hai, per-buyer revenue nahi |
| **C. Section hatao** | Copy se section delete | Zero | Sabse safe, par ek conversion lever chhoot jaata hai |

**Recommendation:** launch ke liye **B** (free bonus) — kyunki (1) content dono case me banana padega, (2) checkout integration ka risk nahi, (3) "free bonus" FE conversion badhata hai, aur (4) baad me easily $9 bump me convert ho sakta hai.

### 6.4 Agar Launch Pe Bonus Stack Chahiye — Ready Plan

Ye cheezein **already built hain ya bahut kam kaam me ban jaati hain**, aur inhe bonus bolna honest rahega:

| # | Bonus | Kya hai | Kaam | Status |
| --- | --- | --- | --- | --- |
| 1 | **Fast-Start Training** | 5–8 short videos: idea se publish tak, KU setup, AI disclosure, series linking | Record karna hai | Module built, content pending |
| 2 | **Saga-Stacker Kit** | Niche list + 90-day calendar + keyword sets + launch checklist | Likho (1 PDF) | Copy ready, product nahi |
| 3 | **KDP Upload Playbook** | Step-by-step screenshots (ebook → paperback → series link → KU) | Guide page built, PDF banana hai | ✅ Page built |
| 4 | **10 Starter Series Templates** | Published lite templates with real AI covers | Seed script ready | ⚠️ Tier gating dekhna |
| 5 | **Cover Style Presets** | 5–10 ready series cover styles (palette + font + layout) | Design karna hai | Product me feature hai, presets nahi |
| 6 | **Launch Checklist (1-page)** | Publish day ka checklist | 30 min | Nahi bana |

**Sabse sasta + strongest combo:** #1 + #3 + #2 → "**Publisher's Fast-Start Pack**" (value $297 bata sakte ho, cost ~0).

### 6.5 Bonus Ke Naam Pe Ye Galtiyan Mat Karo

| Galti | Kyun kharab hai |
| --- | --- |
| OTO features ko "bonus" bolna (jaise "bonus: full-length books") | OTO ki value gir jaati hai, aur jo OTO kharid chuka hai usse refund ka case banta hai |
| "Unlimited books" bolna | Hard cap **30 books/series** hai — false claim |
| "Audible-ready audiobook" bolna | ACX pe AI narration allowed nahi — refund + platform risk |
| Fake value ("$10,958 value!") bina breakdown | FTC/WarriorPlus/JVZoo approval me problem |
| Fake testimonials / income screenshots | Same — JV page me hi likha hai: sirf verified data |
| "Aaj ke baad kabhi nahi milega" | OTO pages launch ke baad bhi live rahenge (in-app Upgrade CTA) — sirf "launch price" wali line sach hai |

---

## 7. Value & Cart Math

### 7.1 Value Stacks

| Offer | Price | Value stack | Ratio |
| --- | --- | --- | --- |
| FE Basic | $17 | $10,958 | 645× |
| OTO1 Unlimited | $47 | $5,082 | 108× |
| OTO2 Done-For-You | $37 | $4,782 | 129× |
| OTO3 Audiobook | $47 | $4,182 | 89× |
| OTO4 Agency | $67 | $5,482 | 82× |
| OTO5 Reseller | $97 | $5,782 | 60× |
| **Total** | **$312** | **$36,268** | **116×** |

> Ye value numbers **copy ke liye** hain, accounting ke liye nahi. Inhe "guaranteed worth" ki tarah present mat karo — "what this would cost any other way" ke hisaab se present karo.

### 7.2 Owner Ke Liye Real Economics

| Metric | Number |
| --- | --- |
| FE revenue per credit | $17 / 300 = **$0.0567** |
| Standard book cost | **$0.156** (20 credits = $1.13 revenue-equivalent → **7.3× margin**) |
| Full-length cost | **$0.215** (35 credits = $1.98 → **9.2× margin**) |
| Cover cost | **$0.012** (2 credits = $0.113 → 9.4×) |
| Max AI cost per FE buyer (300 credits) | 300 × ~$0.008/book-credit ≈ **$2.4** worst case |
| Max AI cost per OTO1 buyer (3,300 credits) | ~**$26** worst case |
| Reseller worst case | $97 revenue vs ~**$98** AI cost (100 customers × 100 credits) ⚠️ |

**Conclusion:** one-time credits model ne recurring-cost risk khatam kar diya — har buyer ka max AI cost uske credits tak fixed hai. Sirf reseller worst case monitor karna hai.

---

## 8. Guarantee, Refund, Support, Legal

| | |
| --- | --- |
| **Guarantee** | 30-day money-back, har offer pe (FE + saare OTOs) |
| **Refund process** | Ek email `softwarevh@gmail.com` — "no forms, no hoops" |
| **Refund window** | 30 calendar days |
| **Refund hone pe system kya karta hai** | Us plan ke credits revoke (`deduct = min(balance, granted)`), purchase log me record, agar koi active plan nahi bacha to account suspend |
| **Support email** | `softwarevh@gmail.com` |
| **Legal pages** | Terms · Privacy · Refund Policy · AI Content Disclosure (admin-editable markdown) |
| **AI disclosure** | KDP pe AI-generated content disclose karna **user ki zimmedari** hai — upload guide me dikhaya gaya hai |
| **Trademark disclaimer** | Amazon/Kindle/KU/KDP Amazon ke trademarks; site unse affiliated nahi |
| **Earnings disclaimer** | Har page ke footer me — royalty figures illustrations hain, promises nahi |

---

## 9. Delivery & Provisioning (Account Kaise Milta Hai)

**Current flow (manual — "Launchpad"):**

1. Buyer payment karta hai (platform: WarriorPlus / JVZoo — **abhi OFF**)
2. Admin **Admin → Users → Create** se account banata hai, ya **Bulk Import CSV** se (⚠️ CSV import **abhi bana nahi**)
3. Admin FE + jo OTO khareede wo plans assign karta hai
4. Admin **"Copy Login Details"** (email + password + login URL) se details copy karke apne thank-you page se buyer ko deta hai
5. Buyer login karta hai → credits already granted

**Important:**
- App ke andar koi checkout, claim page, ya auto-email flow **nahi** hai
- Login details bhejna app ke scope se **bahar** hai — team apne thank-you page se karti hai
- Public signup **disabled** hai
- Email system built hai par **default OFF** — OFF hone pe koi email nahi jaati, "Forgot password" link hide rehta hai
- Har grant `purchases` table me record hota hai (`source = manual / csv / warriorplus / jvzoo`)

**Admin panel me kya-kya hai:** Overview (users, books, queue, AI cost) · Users (create/edit/suspend/impersonate/grant plans/adjust credits) · Credit Ledger · Bulk Import ⚠️ · Plans & Credits · Purchases · Integrations ⚠️ · Email ⚠️ · Templates · Training · Franchise Kit · Jobs monitor · Settings · Audit Log · View-as.

---

## 10. Kya Bana Hua Hai vs Kya Pending Hai

### ✅ Built & Tested

- Poora generation pipeline (series plan → bible → chapters → continuity → metadata), mock + live mode
- Roadmap, My Series, Series Bible (version history + diff + restore), chapter editor + AI tools
- Cover Studio, Image Editor, series cover style lock, paperback wrap, Box Set Builder
- Exports (EPUB3 / Print PDF / DOCX / cover / metadata), KDP Preview + pre-flight, KDP Upload Guide
- Templates (120 + 40 lite), DFY ideas/packs, Audiobook (Kokoro + ACMS spec mastering)
- Agency (clients, pool, allotments, license PDF), Reseller (licenses, dashboard, franchise kit), Training
- Admin: users, ledger, plans, purchases, jobs, view-as, audit, settings, templates
- Credits: one-time grants, stacking, reserve/commit/refund, revoke, agency pools
- Security: RLS, rate limits, CSP, sanitize, upload re-encode; 192 unit/DB tests pass; production build passes
- Docker images (web + worker with chromium/ffmpeg/fonts), Coolify compose, Caddy

### ⚠️ Pending / Deferred

| Item | Status | Impact |
| --- | --- | --- |
| **Bulk Import CSV** (T7.2) | ❌ Deferred by owner | Launch pe har buyer manually banana padega |
| **WarriorPlus / JVZoo webhooks** (T7.5–T7.6) | ❌ Deferred | Auto-provisioning nahi; sab manual |
| **SMTP / email system** (T7.7–T7.8) | ❌ Deferred (built, default OFF) | Welcome/reset emails nahi; credentials manual |
| **200-book load test** (T8.4) | ❌ Skipped | VPS capacity unmeasured |
| **VPS + Supabase Cloud go-live** (T8.6–T8.9) | ❌ Pending | Real deployment + smoke test baaki |
| **Backups / restore rehearsal** (T8.8) | ⚠️ Files + timer ready | Installed/restore-tested nahi |
| **Training videos** | ⚠️ Module built, content nahi | FE value stack me "$497 training" claim karna hai to content chahiye |
| **Franchise kit assets** | ⚠️ Page built, assets admin upload karega | OTO5 bechne se pehle assets chahiye |
| **Regular prices** (`[$XX]`) | ⚠️ Brackets khali | Launch ke baad price badhane ka claim sach hona chahiye |
| **Demo video** (`[VIDEO]`) | ⚠️ Nahi bana | FE + har OTO page pe placeholder |
| **Login delivery line** | ⚠️ Nahi likha | OTO pages ke "congratulations" section me chahiye |
| **Order bump decision** | ⚠️ Pending | §6.3 dekho |
| **Affiliate/JV commission structure** | ⚠️ Repo me defined nahi | JV page me sirf sales copy hai, commission % kahin nahi — platform pe decide hoga |
| **Audiobook store policies** | ⚠️ Launch se pehle verify | Google Play/Kobo AI-narration rules badalte hain |

---

## 11. Marketing Angles (Jo Copy Me Already Hain)

**Top hooks (FE page se):**
1. **"One idea. One whole saga."** — single book vs series ka contrast
2. **Read-through** — "a standalone book has no read-through"; series reader dobara kharidta hai
3. **Amazon series engine** — series pages, also-boughts, new release purane books bikwata hai, KU page reads stack
4. **Royalty maths** — 1 book = $3.49/reader vs 5 books = $17.45/reader (illustrative)
5. **Cost contrast** — ghostwritten 5-book series $10,800–$31,500 aur 6–12 months vs $17 aaj
6. **Faceless business** — pen name, no audience, no social media
7. **Continuity** — "a character who changes in Book Three" = reviews me problem
8. **Fully editable** — AI se shuru, aap finish karo

**Objection handlers (already likhe hue):**
- "Amazon AI books allow karta hai?" → Haan, disclosure ke saath
- "Readers finish karenge?" → length + consistency + reason to keep going + anti-cliché filter
- "Isn't Amazon full of AI books?" → quality/originality enforcement, series depth
- "Do I need an audience?" → Nahi, Amazon readers laata hai
- "Returns?" → proper length + consistent characters + satisfying endings

**Har page pe rehna chahiye:** earnings disclaimer, trademark disclaimer, 30-day guarantee, support email.

---

## 12. Launch Se Pehle Decisions (Checklist)

- [ ] **Order bump:** banao ($9), free bonus banao, ya hatao? (§6.3)
- [ ] **Regular prices** tay karo — `[$XX]` har page pe hai (FE + 5 OTO)
- [ ] **Demo video** record karo (FE + 5 OTO pages)
- [ ] **Login delivery line** likho (thank-you page flow ke saath match kare)
- [ ] **Training videos** banao — warna FE value stack se "$497 training" hatao
- [ ] **Franchise kit assets** upload karo (sales page HTML, swipes, banners, demo link)
- [ ] **Template counts confirm** karo: 120 full / 40 lite / 500 ideas (copy me brackets hain)
- [ ] **Audiobook store policies** verify karo (Google Play, Kobo, ACX)
- [ ] **Provisioning plan** — CSV import nahi hai, to launch pe manually kitne buyers handle honge?
- [ ] **Reseller worst case** ka call lo (100 × 100 credits ≈ $98 AI cost)
- [ ] **Affiliate/JV commission** decide karo (repo me nahi hai)
- [ ] **JV page ke saare brackets** bharo — testimonials sirf verified + permission ke saath

---

## 13. Source of Truth Map

| Fact | File |
| --- | --- |
| 11 plans, prices, limits, credit grants | `packages/shared/src/plans.ts` |
| Effective entitlements (union/max rules) | `packages/shared/src/entitlements.ts` |
| Credit actions, costs, pools, agency routing | `packages/shared/src/credits.ts` |
| Funnel, entitlement matrix, credit rules, features | `docs/PRD.md` §3, §4, §8 |
| OTO page copy (25 sections × 5 + downsells) | `docs/OTO_PAGES.md` |
| FE sales page copy (50 sections) + value stack + bump | `docs/JV_LANDING_PAGE.md` |
| Measured AI cost, latency, margins | `docs/COST_REPORT.md` |
| Build status, pending tasks, scope update | `docs/TASKS.md` |
| Architecture, DB, queue, security | `docs/ARCHITECTURE.md` |
| Admin operations (users, refunds, integrations) | `docs/ADMIN_RUNBOOK.md` |
| Deployment (VPS / Coolify) | `docs/LAUNCH.md`, `docs/SUPABASE_COOLIFY.md` |
| Known bugs | `BUGS.md` |

---

## Appendix A — Plan Matrix (poora table)

Legend: ✅ milta hai · ❌ nahi · – ye plan is feature ko change nahi karta

| Feature | FE $17 | U-Lite $27 | U $47 | DFY-Lite $17 | DFY $37 | AB-Lite $27 | AB $47 | Ag-Lite $47 | Ag $67 | Res-Lite $67 | Res $97 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Main credits (one-time) | 300 | +1,000 | +3,000 | – | – | – | – | – | – | – | – |
| Active series | 3 | 25 | ∞ | – | – | – | – | – | – | – | – |
| Books per series | 5 | 30 | 30 | – | – | – | – | – | – | – | – |
| Short + Standard | ✅ | ✅ | ✅ | – | – | – | – | – | – | – | – |
| Full-length | ❌ | ✅ | ✅ | – | – | – | – | – | – | – | – |
| Paperback wrap PDF | ❌ | ✅ | ✅ | – | – | – | – | – | – | – | – |
| Box Set Builder | ❌ | ✅ | ✅ | – | – | – | – | – | – | – | – |
| Templates | ❌ | – | – | 40 | 120 | – | – | – | – | – | – |
| DFY ideas/blurbs/keywords | ❌ | – | – | lite | full | – | – | – | – | – | – |
| Audio credits | 0 | – | – | – | – | +300 | +1,000 | – | – | – | – |
| Audiobook | ❌ | – | – | – | – | ✅ | ✅ | – | – | – | – |
| Client accounts | 0 | – | – | – | – | – | – | 25 | 100 | – | – |
| Agency credits | 0 | – | – | – | – | – | – | +2,000 | +5,000 | – | – |
| Resell licenses | 0 | – | – | – | – | – | – | – | – | 50 | 100 |
| Franchise kit | ❌ | – | – | – | – | – | – | – | – | ✅ | ✅ |

**Rules:**
- FE baseline har buyer ko milta hai (koi bhi active plan ho to)
- Downsell + full OTO dono ho to **features full OTO ke** (max/union)
- **Credits dono ke judte hain** (dono ka paisa diya hai)
- Hard system cap: **30 books per series** (sab plans)
- Daily cap: **10 books/day** per user
- Archived/deleted series "3 active" me count nahi hoti

---

## Appendix B — Ek Buyer Ka Typical Journey (numbers ke saath)

**Scenario: FE + Unlimited + Audiobook**

1. $17 FE kharida → 300 credits
2. OTO1 $47 → +3,000 credits (total 3,300), full-length unlock, 30 books/series, unlimited series, wrap + box sets
3. OTO3 $47 → +1,000 audio credits, audiobook module
4. Total paid: **$111** · Credits: **3,300 main + 1,000 audio**
5. Pehli series: 5 full-length books + 5 covers = 5 × 37 = **185 main credits** → 5 books ~4–5 ghante me
6. Box set banaya → +2 credits (cover) → **187**
7. Audiobook (5 books) → 5 × 15 = **75 audio credits**
8. Baaki **3,113 main credits** ≈ **84 full-length books with covers**

**Uska ROI math (illustrative):** 5 books, har book $4.99 pe 70% = $3.49; agar 100 readers poora series padhein = 100 × 5 × $3.49 = **$1,745** (KU page reads alag).

---

*Ye document product docs se generate hua hai. Numbers badalne pe (prices, credit costs, template counts, regular prices) is file ko update karna — warna marketing copy aur app ke beech mismatch ho jayega.*
