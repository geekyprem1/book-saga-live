#!/usr/bin/env python3
"""
BookSaga · OTO + Downsell page generator.

Source of truth for every claim in here: PRODUCT_OFFER_BONUS_GUIDE.md
(funnel §4, per-offer detail §5, value stacks §7.1, guarantee §8).

Output (repo root, same asset paths as index.html):
    oto1.html .. oto5.html   -> full OTO offers
    ds1.html  .. ds5.html    -> matching downsells

Every page: >= 18 sections, and the LAST section is the YES/NO decision block.

Checkout URLs are NOT hardcoded in the markup. Each page carries one
window.BS_CFG block in <head>; paste the Launchpad checkout URL there.
"""

import os

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------- icons
ICONS = {
    "book": "<path d='M4 19.5A2.5 2.5 0 0 1 6.5 17H20'/><path d='M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z'/>",
    "layers": "<path d='M12 2 2 7l10 5 10-5-10-5z'/><path d='M2 17l10 5 10-5'/><path d='M2 12l10 5 10-5'/>",
    "mic": "<path d='M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z'/><path d='M19 10v2a7 7 0 0 1-14 0v-2'/><path d='M12 19v4'/>",
    "users": "<path d='M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2'/><path d='M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z'/><path d='M23 21v-2a4 4 0 0 0-3-3.87'/><path d='M16 3.13a4 4 0 0 1 0 7.75'/>",
    "rocket": "<path d='M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z'/><path d='M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0'/><path d='M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5'/>",
    "chart": "<path d='M18 20V10'/><path d='M12 20V4'/><path d='M6 20v-6'/>",
    "lock": "<path d='M7 11V7a5 5 0 0 1 10 0v4'/><path d='M5 11h14v10a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z'/>",
    "clock": "<path d='M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z'/><path d='M12 6v6l4 2'/>",
    "shield": "<path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/>",
    "star": "<path d='M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 22 12 18.56 5.82 22 7 14.14l-5-4.87 6.91-1.01z'/>",
    "download": "<path d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/><path d='M7 10l5 5 5-5'/><path d='M12 15V3'/>",
    "wand": "<path d='M15 4V2'/><path d='M15 16v-2'/><path d='M8 9h2'/><path d='M20 9h2'/><path d='M17.8 11.8L19 13'/><path d='M17.8 6.2L19 5'/><path d='M3 21l9-9'/><path d='M12.2 6.2L11 5'/>",
    "bolt": "<path d='M13 2 3 14h9l-1 8 10-12h-9l1-8z'/>",
    "copy": "<path d='M20 9h-9a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-9a2 2 0 0 0-2-2z'/><path d='M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1'/>",
    "image": "<path d='M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2z'/><path d='M8.5 10a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z'/><path d='M21 15l-5-5L5 21'/>",
    "grid": "<path d='M3 3h7v7H3z'/><path d='M14 3h7v7h-7z'/><path d='M14 14h7v7h-7z'/><path d='M3 14h7v7H3z'/>",
    "target": "<path d='M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z'/><path d='M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10z'/><path d='M12 11a1 1 0 1 0 0 2 1 1 0 0 0 0-2z'/>",
}

def ico(name, cls="bs-card-ico"):
    return '<span class="%s"><svg viewBox="0 0 24 24" aria-hidden="true">%s</svg></span>' % (cls, ICONS[name])


# --------------------------------------------------------------------------- pages
PAGES = []

# ============================================================== OTO 1 · Unlimited
PAGES.append({
    "slug": "oto1.html",
    "kind": "oto",
    "num": 1,
    "title": "BookSaga Unlimited — Full-Length Novels, 30 Books Per Series, Box Sets",
    "desc": "Unlock the Full-Length engine, 30 books per series, unlimited active series, print-ready paperback wraps, Box Set Builder and 3,000 extra credits.",
    "name": "Unlimited",
    "hl": "Unlimited",
    "price": "$47",
    "price_num": "47",
    "regular": "$297",
    "pill": "Step 2 of 6 · Your order is confirmed",
    "h1_pre": "Your BookSaga Plan Stops At",
    "h1_hl": "Book 5.",
    "lead": "BookSaga Basic writes up to 5 books per series in Short and Standard. Unlimited removes that ceiling: full-length novels, up to 30 books per series, unlimited active series, print-ready paperback wraps, Box Sets — and 3,000 extra one-time credits.",
    "hero_img": "images/booksaga-product-mockup.png",
    "hero_alt": "BookSaga series workspace showing a multi-book series",
    "video_note": "2-minute walkthrough: the Full-Length engine and the Box Set Builder in action",
    "stops_head": "Where your current plan stops",
    "stops_lead": "Basic is a real product — it is just deliberately capped. These are the exact walls you are standing in front of right now.",
    "stops": [
        ("Books per series", "5", "30"),
        ("Active series at once", "3", "Unlimited"),
        ("Length preset", "Short + Standard", "+ Full-Length"),
        ("Paperback full-wrap cover", "Not included", "Included"),
        ("Box Set Builder", "Not included", "Included"),
        ("One-time credits", "300", "3,300"),
    ],
    "problems": [
        ("clock", "Book 5 is a cliff, not a finish line.", "A five-book series ends exactly where read-through starts compounding. Readers who wanted more have nowhere to go — so they go to another author."),
        ("book", "Short and Standard cap your price point.", "At ~12,000 and ~30,000 words you are competing in the crowded cheap end. Full-length novels (~55,000 words) support the $4.99-$6.99 price you actually want."),
        ("grid", "No wrap means no paperback.", "Amazon's paperback is where the physical-looking product lives. Without a print-ready spine, you cannot ship the version readers photograph and share."),
        ("layers", "Three series is not a catalogue.", "Three active series is a test. A catalogue is twenty series, each with a box set and a paperback, all feeding each other."),
    ],
    "intro_head": "Introducing BookSaga Unlimited",
    "intro_lead": "Same app you already own. The ceilings come off.",
    "intro_body": "Unlimited is not a new tool you have to learn. It is the same workspace you just bought, with the limits you hit in week one removed: a Full-Length engine, 30 books per series, unlimited active series, print-ready paperback wraps, Box Set Builder, and 3,000 credits stacked on top of the 300 you already have.",
    "unlocks": [
        ("book", "Full-Length Novels", "25-30 chapters, ~55,000 words per book. The length that supports premium pricing and real KU page reads."),
        ("layers", "30 Books Per Series", "Six times the runway. Arc-level planning that actually pays off across a long series instead of resetting every five books."),
        ("grid", "Unlimited Active Series", "Run as many series in parallel as your catalogue needs — across as many pen names as you like."),
        ("image", "Paperback Full-Wrap Cover PDF", "Front, spine and back at 300 DPI, built to KDP print specs. Spine width calculated for you."),
        ("star", "Box Set Builder", "Combine 2+ books into one higher-priced listing with a combined TOC, dividers and its own cover."),
        ("bolt", "3,000 Extra One-Time Credits", "Stacked on your existing 300 — 3,300 total, one-time, no refills and no expiry."),
        ("wand", "Add More Parts", "Extend a series past its planned count, up to the 30-book system cap, for 1 credit each time."),
        ("download", "Everything you already had", "Series Bible, continuity checks, cliffhangers, metadata, EPUB3 / print PDF / DOCX exports — all unchanged."),
    ],
    "how": [
        ("Open any series", "Pick the series you are already writing, or start a new one. Nothing to import, nothing to rebuild."),
        ("Choose Full-Length", "The length preset appears in the create flow and on any existing series. Plan the arc for 25-30 chapters."),
        ("Generate the run", "BookSaga writes sequentially so the Series Bible stays accurate — Book 2 loads everything Book 1 established."),
        ("Export and publish", "EPUB3, print interior, paperback wrap, Box Set, metadata CSV. Upload to KDP with the built-in guide."),
    ],
    "deep": [
        ("Why length changes the maths", "A ~290-page full-length novel is roughly 1.31 USD of KU page reads per complete read, against about 0.29 USD for a ~65-page short. Same reader, same click — four and a half times the payout. That is before the higher list price.", ["Short ~65 pages ≈ $0.29 per full read", "Standard ~160 pages ≈ $0.72 per full read", "Full-length ~290 pages ≈ $1.31 per full read", "Ebook at $4.99 / 70% ≈ $3.49 per sale"]),
        ("Box sets are a second product from the same work", "Once you have 2+ books in a series, Box Set Builder produces a separate listing at a higher price point — with its own cover, TOC and description. No new writing. A 5-book box set at $9.99 at 70% is roughly $6.99 per sale.", ["Combined TOC generated for you", "Per-book divider pages", "Flat or 3D box set cover", "AI-written box set description"]),
        ("A real catalogue, not a test", "Unlimited active series is what turns three experiments into a catalogue: different genres, different pen names, all cross-promoting. Ten full-length books is roughly 2,900 KENP pages of surface area against roughly 325 for a five-book short series.", ["Per user: 10 book generations per day cap", "1 book job + 3 cover jobs at a time", "Credits are one-time and never expire"]),
    ],
    "math_head": "What the same reader is worth",
    "math_lead": "Illustrative royalty maths, not a promise. Assumes the reader finishes the series and buys at the listed price.",
    "math": [
        ("1 short book, 1 reader", "$0.29 KU + $3.49 ebook", "$3.78"),
        ("5-book short series, 1 reader", "5 × $3.78", "$18.90"),
        ("5-book full-length series, 1 reader", "5 × ($1.31 KU + $3.49)", "$24.00"),
        ("10-book full-length series, 1 reader", "10 × ($1.31 KU + $3.49)", "$48.00"),
        ("5-book box set, 1 reader", "$9.99 at 70%", "$6.99"),
    ],
    "compare_head": "Without Unlimited vs With Unlimited",
    "compare": [
        ("Longest book you can produce", "~30,000 words", "~55,000 words"),
        ("Longest series you can produce", "5 books", "30 books"),
        ("Series running at once", "3", "Unlimited"),
        ("Paperback product", "Not possible", "Print-ready wrap included"),
        ("Second product per series", "Not possible", "Box Set Builder"),
        ("Credits available", "300", "3,300"),
    ],
    "uses_head": "Five ways publishers actually use Unlimited",
    "uses": [
        ("Build one flagship series properly", "30 books at full length, one arc, one cover style, one read-through engine."),
        ("Ship paperbacks of everything", "Turn every finished ebook into a physical listing with a properly calculated spine."),
        ("Launch a box set ladder", "Books 1-3 at entry, 1-5 at mid, 1-10 as the premium bundle."),
        ("Run several pen names at once", "Unlimited active series means no artificial cap on how many catalogues you run."),
        ("Go long in non-fiction", "Full-length self-help, business and health titles carry more authority than a 30,000-word booklet."),
    ],
    "whofor": [
        "You already hit the 5-book ceiling on a series you care about.",
        "You want full-length novels at a premium price point.",
        "You want paperbacks and box sets, not just ebooks.",
        "You are running more than three series or pen names.",
    ],
    "notfor": [
        "You have not published your first Basic series yet.",
        "Short reads are your deliberate strategy and the 5-book cap is fine.",
        "You only ever want one series.",
    ],
    "elsewhere": [
        ("Ghostwritten 5-book series", "$10,800 - $31,500", "and 6-12 months of waiting"),
        ("Full-length novel from a ghostwriter", "$1,200 - $4,000", "per book, before covers"),
        ("Print-ready wrap cover design", "$150 - $400", "per book, per revision"),
        ("Box set formatting service", "$100 - $300", "per box set"),
        ("BookSaga Unlimited, today", "$47", "one time, no monthly fee"),
    ],
    "stack": [
        ("Full-Length Novel Engine (25-30 chapters)", "$997"),
        ("30 Books Per Series + Add More Parts", "$697"),
        ("Unlimited Active Series", "$697"),
        ("Paperback Full-Wrap Cover PDF (300 DPI)", "$497"),
        ("Box Set Builder", "$697"),
        ("3,000 one-time credits", "$1,497"),
    ],
    "stack_total": "$5,082",
    "faq": [
        ("Is 'Unlimited' really unlimited books?", "No — and we will not pretend otherwise. Unlimited means unlimited <em>active series</em>. Books per series has a hard system cap of 30 on every plan. There is also a daily cap of 10 book generations per user."),
        ("Do my existing 300 credits disappear?", "No. Credits stack. You keep the 300 from Basic and add 3,000 — 3,300 total, one time, no expiry, no refill."),
        ("Do I have to rewrite my existing series?", "No. Your series, bible, chapters and covers stay exactly where they are. Full-Length and the higher caps simply become available on them."),
        ("What exactly is a full-wrap cover PDF?", "A single print-ready file containing back cover, spine and front cover at 300 DPI, with spine width calculated from page count and paper stock. It is what KDP wants for a paperback."),
        ("Does this replace my Basic plan?", "It adds to it. Basic stays as your baseline; Unlimited removes its limits and stacks credits on top."),
        ("What if I do not like it?", "30 days, one email to softwarevh@gmail.com. No forms, no hoops. Every offer carries the same guarantee."),
    ],
    "ps": [
        "You have already paid for the hard part — the engine, the Series Bible, the continuity checks. The only thing standing between you and a 30-book full-length catalogue is a 47 dollar ceiling.",
        "The 3,000 credits alone are roughly 81 full-length books with covers. At the current per-credit cost that is more writing than most publishers finish in a year.",
    ],
    "decision_lead": "Add the Full-Length engine, 30-book series, print wraps, Box Sets and 3,000 credits to your BookSaga account for a one-time $47.",
    "yes_label": "Yes, Unlock Unlimited!",
    "yes_cap": "Yes, I want full-length novels, 30-book series and box sets",
    "no_label": "No Thanks, I'll Stay At 5 Books",
    "no_cap": "I want to keep my series capped at five",
    "no_url": "ds1.html",
})

# ============================================================== OTO 2 · Done-For-You
PAGES.append({
    "slug": "oto2.html",
    "kind": "oto",
    "num": 2,
    "title": "BookSaga Done-For-You — 120 Proven Series Templates + 500 Ideas",
    "desc": "Skip the blank page. 120 tested series templates across 12 categories, 500+ DFY series ideas, blurb templates and keyword packs — one click to prefill.",
    "name": "Done-For-You",
    "hl": "Done-For-You",
    "price": "$37",
    "price_num": "37",
    "regular": "$197",
    "pill": "Step 3 of 6 · Your order is confirmed",
    "h1_pre": "The Most Expensive Mistake Is",
    "h1_hl": "The Wrong Idea.",
    "lead": "A five-book Standard series with covers costs 110 credits — more than a third of the 300 you own. Burn that on an idea that does not sell and the credits are gone. Done-For-You hands you 120 tested series concepts, 500 more ideas, blurbs and keyword packs, all one click away.",
    "hero_img": "images/amazonseries_b050ec.png",
    "hero_alt": "Amazon series page showing a completed multi-book series",
    "video_note": "90 seconds: picking a template and going from blank screen to a prefilled series",
    "stops_head": "Where your current plan stops",
    "stops_lead": "Basic gives you a powerful engine and an empty room. Done-For-You puts a tested shelf in it.",
    "stops": [
        ("Series templates", "0", "120"),
        ("DFY series ideas", "0", "500+"),
        ("Blurb templates by genre", "0", "Full library"),
        ("KDP keyword packs", "0", "By genre"),
        ("Sample cover per template", "0", "120"),
        ("One-click prefill", "Not included", "Included"),
    ],
    "problems": [
        ("target", "You are guessing the genre.", "Every niche looks profitable from the outside. The ones that actually hold a series together are the ones with built-in read-through — and you find that out after book one."),
        ("clock", "Research eats the first week.", "Category browsing, competitor blurb reading, keyword digging. Days spent before a single word exists."),
        ("copy", "Blurbs are their own craft.", "The description sells the click. Most first-time publishers write a synopsis instead of a sales page and watch the conversion rate flatline."),
        ("chart", "Keywords decide who finds you.", "Seven KDP keyword slots. Fill them with guesses and you are invisible; fill them with tested phrases and you are on the first page."),
    ],
    "intro_head": "Introducing BookSaga Done-For-You",
    "intro_lead": "120 series that already work — ready to prefill your workspace.",
    "intro_body": "Twelve categories, ten templates each. Every template carries a concept and hook, a core cast, a complete five-book arc, the tone, the target audience and a sample cover. One click prefills the Create Series form with all of it — every field still fully editable before you generate anything.",
    "unlocks": [
        ("grid", "120 Series Templates", "12 categories × 10 templates: Fantasy, Romance, Mystery & Thriller, Historical, YA, Children's, Sci-Fi, Horror, Business & Money, Health & Wellness, Faith, Self-Help."),
        ("bolt", "One-Click 'Use This Template'", "The Create Series form arrives prefilled with the concept, cast, five-book arc, tone and audience. Nothing is locked."),
        ("book", "500+ DFY Series Ideas", "Title, premise and hook by niche — for when you want to go sideways from a template."),
        ("copy", "Blurb Templates By Genre", "Descriptions written the way the genre expects, ready to adapt rather than invent."),
        ("chart", "Keyword Packs By Genre", "Tested starting phrases for the seven KDP slots, instead of guessing in an empty box."),
        ("image", "A Sample Cover For Every Template", "See the visual promise before you commit a single credit."),
        ("star", "Badges That Save Time", "Bestseller / Popular / New on each template so you can start where the market already leans."),
        ("wand", "Grows Over Time", "New templates are added as the catalogue is managed — your library is not frozen at purchase."),
    ],
    "how": [
        ("Open the template library", "Browse by category or sort by badge. Every card shows the sample cover and the hook."),
        ("Click Use This Template", "The Create Series form opens prefilled. Change the genre, the length, the names, the arc — it is all yours."),
        ("Generate as normal", "Same engine, same Series Bible, same continuity checks. The template just removed the blank page."),
        ("Adapt the listing", "Pull the matching blurb template and keyword pack, then publish."),
    ],
    "deep": [
        ("What is actually inside a template", "It is not a title and a paragraph. Each one is a small production brief you could hand to a ghostwriter — which is exactly what the engine needs to keep five books coherent.", ["Concept and hook", "Core cast with roles", "Complete 5-book arc", "Tone and voice", "Target audience", "Sample cover", "Bestseller / Popular / New badge"]),
        ("The twelve categories", "Chosen because they support series read-through, not because they were easy to write. Fantasy, Romance, Mystery & Thriller, Historical, YA, Children's, Sci-Fi, Horror, Business & Money, Health & Wellness, Faith, Self-Help.", ["10 templates in every category", "Fiction and non-fiction both covered", "Each with its own blurb and keyword pack"]),
        ("Credit maths, so the risk is visible", "A five-book Standard series with covers is 110 credits. On 300 credits that is a third of your entire budget on one guess. A tested template does not guarantee sales — but it removes the most avoidable reason a series fails.", ["5 books × 20 credits = 100", "5 covers × 2 credits = 10", "Total 110 of your 300"]),
    ],
    "math_head": "What a wrong guess actually costs",
    "math_lead": "Illustrative. Assumes a five-book Standard series with matching covers.",
    "math": [
        ("Wrong niche, five books, covers", "110 credits", "gone"),
        ("Right niche, five books, covers", "110 credits", "same spend, better odds"),
        ("Your 300 credits buy", "2 full series", "or 27 single books"),
        ("Templates in Done-For-You", "120", "before you write a word"),
    ],
    "compare_head": "Without Done-For-You vs With Done-For-You",
    "compare": [
        ("Starting point", "Blank form", "120 prefilled templates"),
        ("Idea research", "Days of browsing", "Browsable library"),
        ("Five-book arc", "You invent it", "Included per template"),
        ("Blurb", "From scratch", "Genre template to adapt"),
        ("Keywords", "Guesses", "Tested packs by genre"),
        ("Cover direction", "Undecided", "Sample cover per template"),
    ],
    "uses_head": "How publishers use the library",
    "uses": [
        ("De-risk a first series", "Start from a Bestseller-badged template in a category you understand."),
        ("Break a plateau", "Your genre stopped converting — test a template from an adjacent category."),
        ("Speed up a pen name", "Prefill a whole series in one click instead of an afternoon of planning."),
        ("Brief a collaborator", "Templates double as a clean brief if someone else writes or edits."),
        ("Build a niche shortlist", "Read 20 templates in a category before committing credits anywhere."),
    ],
    "whofor": [
        "You are about to spend 110 credits on a series and want the idea de-risked first.",
        "You keep stalling on what to write next.",
        "Blurbs and keywords are the part you dread.",
        "You want a browsable catalogue of proven shapes, not a blank prompt.",
    ],
    "notfor": [
        "You already have a tested idea and a clear five-book arc.",
        "You write only in a niche no template covers and do not want to adapt.",
        "You enjoy the research phase and want to do it yourself.",
    ],
    "elsewhere": [
        ("Niche research service", "$300 - $900", "per niche, one-off"),
        ("Blurb copywriter", "$50 - $150", "per book"),
        ("Keyword research tool", "$30 - $99", "per month, forever"),
        ("Series outline from a developmental editor", "$400 - $1,200", "per series"),
        ("BookSaga Done-For-You, today", "$37", "one time, no monthly fee"),
    ],
    "stack": [
        ("120 Series Templates (12 categories)", "$1,997"),
        ("500+ DFY Series Ideas", "$997"),
        ("Blurb Templates By Genre", "$497"),
        ("KDP Keyword Packs By Genre", "$697"),
        ("Sample Cover Per Template", "$297"),
        ("One-Click Prefill", "$297"),
    ],
    "stack_total": "$4,782",
    "faq": [
        ("Are the templates locked to a genre?", "No. Every field prefills and every field is editable — genre, length, names, arc, tone. The template is a starting shape, not a cage."),
        ("Do templates come with Unlimited?", "No. Templates live only in Done-For-You (120) and Done-For-You Lite (40). Unlimited does not include them — these are separate offers."),
        ("Will my series look like everyone else's?", "Templates are shapes, not text. The engine writes from your prefilled arc, cast and tone, and you can change any of it before generating."),
        ("How many credits does a template cost?", "None. Templates are free to browse and prefill. You only spend credits when you actually generate books and covers."),
        ("What is the difference between Lite and full?", "Lite gives you 40 templates and a reduced ideas/blurb/keyword selection. Full gives you all 120 plus the complete library."),
        ("Guarantee?", "30 days, one email to softwarevh@gmail.com. Same on every offer."),
    ],
    "ps": [
        "You do not need more ideas. You need fewer bad ones. 120 tested shapes cost less than a single wrong five-book series.",
        "The 110 credits you would spend guessing are worth more than this entire offer.",
    ],
    "decision_lead": "Add 120 tested series templates, 500+ ideas, blurb templates and keyword packs to your BookSaga account for a one-time $37.",
    "yes_label": "Yes, Give Me The 120 Templates!",
    "yes_cap": "Yes, I want tested templates, blurbs and keyword packs",
    "no_label": "No Thanks, I'll Guess The Niche",
    "no_cap": "I'll spend my credits on an untested idea",
    "no_url": "ds2.html",
})

# ============================================================== OTO 3 · Audiobook
PAGES.append({
    "slug": "oto3.html",
    "kind": "oto",
    "num": 3,
    "title": "BookSaga Audiobook — Turn Every Finished Book Into Audio",
    "desc": "Narrate any finished BookSaga book: curated AI voices, per-chapter MP3 at ACX specs, square cover, in-app player and ZIP download. 1,000 audio credits.",
    "name": "Audiobook",
    "hl": "Audiobook",
    "price": "$47",
    "price_num": "47",
    "regular": "$297",
    "pill": "Step 4 of 6 · Your order is confirmed",
    "h1_pre": "You Wrote The Book. Now It Can",
    "h1_hl": "Talk.",
    "lead": "Audiobook turns any finished BookSaga book into per-chapter MP3s, mastered to ACX technical specs, with a square cover and an in-app player. 1,000 audio credits — roughly 66 audiobooks — added as a separate pool that never touches your main credits.",
    "hero_img": "images/inside1_949c81.png",
    "hero_alt": "Chapter opening page from a BookSaga series",
    "video_note": "90 seconds: picking a voice, previewing it, and exporting a full audiobook",
    "stops_head": "Where your current plan stops",
    "stops_lead": "Basic produces ebooks and print files. Audio is a different product entirely — and a different buyer.",
    "stops": [
        ("Audiobook module", "Not included", "Included"),
        ("Curated AI voices", "0", "US + UK, male + female"),
        ("Per-chapter MP3", "Not included", "192 kbps CBR"),
        ("ACX-spec mastering", "Not included", "Included"),
        ("Square cover 2400×2400", "Not included", "Included"),
        ("Audio credits", "0", "1,000"),
    ],
    "problems": [
        ("mic", "Professional narration is out of reach.", "A 55,000-word novel narrated by a pro runs into thousands of dollars and weeks of scheduling — before you know whether the book sells."),
        ("clock", "Audio listeners are a different market.", "Commuters, gym-goers and people who never open an ebook. Same manuscript, a whole audience you currently cannot reach."),
        ("download", "Formatting audio by hand is miserable.", "Chapter splits, loudness normalisation, peak limiting, room tone, opening and closing credits. Every one of those is a step you can get wrong."),
        ("star", "One format is one price point.", "Ebook, paperback and audiobook are three listings and three revenue streams from the same written work."),
    ],
    "intro_head": "Introducing BookSaga Audiobook",
    "intro_lead": "Any finished book, narrated, mastered and exported.",
    "intro_body": "Pick a book, pick a voice, preview it, set the speed. BookSaga produces one MP3 per chapter at 192 kbps CBR, 44.1 kHz mono, mastered to ACX technical specifications, with opening and closing credit files and a 2400×2400 square cover. Download the ZIP or listen in the app.",
    "unlocks": [
        ("mic", "Audiobook Series Module", "Narrate any finished book in any series. Runs as its own job queue, separate from writing."),
        ("users", "Curated Natural Voices", "US and UK English, male and female, each with a preview before you commit a credit."),
        ("clock", "Speed Control 0.8× - 1.2×", "Match the pacing to the genre. Cozy mystery and thriller do not read at the same tempo."),
        ("download", "One MP3 Per Chapter", "192 kbps CBR, 44.1 kHz, mono. Chapter boundaries already correct — no splitting by hand."),
        ("chart", "ACX-Spec Mastering", "RMS -23 to -18 dB, peak at or below -3 dB, noise floor at or below -60 dB, room tone, opening and closing credits."),
        ("image", "2400×2400 Square Cover", "The square format the audio stores actually want, generated from your existing cover art."),
        ("bolt", "In-App Player + ZIP", "Listen before you ship, then download everything as one archive."),
        ("layers", "1,000 Audio Credits", "A separate pool at 15 credits per book — roughly 66 audiobooks, and your main credits stay untouched."),
    ],
    "how": [
        ("Pick a finished book", "Only completed books can be narrated — the manuscript has to exist first."),
        ("Choose and preview a voice", "Browse US and UK voices, male and female, and hear a sample before spending anything."),
        ("Set the speed", "0.8× to 1.2×. Preview again if you want to be sure."),
        ("Generate and export", "Per-chapter MP3s, mastered, with credits files, square cover and a ZIP download."),
    ],
    "deep": [
        ("Where you can actually publish this", "This matters more than any feature list, so it is stated plainly: AI-narrated audio is not accepted by Audible through ACX today. BookSaga audio is not for ACX upload. It is for the stores and channels that do accept it.", ["Google Play Books — accepts AI-narrated audiobooks with disclosure", "Kobo — list the narrator as a synthetic voice", "Your own store — Payhip, Gumroad, Shopify, your site", "Reader magnet — a free audio prequel to grow your list", "Always re-check each store's current AI-narration policy before publishing"]),
        ("What 'mastered to ACX specs' means", "It means the technical envelope is already inside the range that professional audio platforms expect — so the files are not rejected on technical grounds, and they sound consistent from chapter one to chapter thirty.", ["RMS -23 to -18 dB", "True peak at or below -3 dB", "Noise floor at or below -60 dB", "Room tone between chapters", "Opening and closing credit files"]),
        ("The credit maths", "Audio credits are a separate pool, so narrating never eats your writing budget. At 15 credits per book, 1,000 credits is roughly 66 finished audiobooks.", ["15 audio credits per book", "1,000 credits ≈ 66 books", "Main credits untouched", "One-time, no expiry"]),
    ],
    "math_head": "Three listings from one manuscript",
    "math_lead": "Illustrative revenue shapes. Audio pricing is your call; these are typical indie ranges.",
    "math": [
        ("Ebook at $4.99 / 70%", "$3.49", "per sale"),
        ("Paperback at $12.99", "≈ $4.00", "per sale"),
        ("Audiobook at $9.99 / 70%", "≈ $6.99", "per sale"),
        ("KU full read (full-length)", "≈ $1.31", "per complete read"),
        ("All three, one reader", "≈ $14.48", "same written work"),
    ],
    "compare_head": "Without Audiobook vs With Audiobook",
    "compare": [
        ("Formats per book", "Ebook + print", "Ebook + print + audio"),
        ("Reaching audio-only listeners", "Not possible", "Full audiobook catalogue"),
        ("Narration cost", "$2,000+ per novel", "15 credits per book"),
        ("Chapter splitting", "By hand", "Automatic"),
        ("Loudness / peak / noise", "Your problem", "Mastered to spec"),
        ("Square cover", "You make it", "Generated"),
    ],
    "uses_head": "Ways publishers use audio",
    "uses": [
        ("A third listing on every book", "Same manuscript, an entirely new buyer who never opens an ebook."),
        ("Bundle audio with the ebook", "Sell both together on your own store at a higher price."),
        ("Free audio prequel as a list magnet", "Give away book one's audio to pull readers into the series."),
        ("Serve non-readers", "Commuters and gym listeners who would never buy the text."),
        ("Test a niche cheaply", "Narrate one book to see if the genre has audio appetite before committing."),
    ],
    "whofor": [
        "You have finished books sitting in your workspace with no audio version.",
        "You want a third revenue stream from work you already did.",
        "You are building a reader-magnet funnel and want audio in it.",
        "You sell on your own store where AI narration is fine.",
    ],
    "notfor": [
        "You want to upload to Audible through ACX — AI narration is not accepted there.",
        "You have no finished books yet.",
        "You need human narration for a specific reason.",
    ],
    "elsewhere": [
        ("Professional audiobook narration (per finished hour)", "$200 - $400", "a 55k novel is 6-8 hours"),
        ("Audio editing / mastering service", "$50 - $120", "per finished hour"),
        ("Audiobook cover design", "$75 - $250", "per title"),
        ("Full 5-book series narrated professionally", "$6,000 - $16,000", "and months of scheduling"),
        ("BookSaga Audiobook, today", "$47", "one time, 1,000 credits"),
    ],
    "stack": [
        ("Audiobook Series Module", "$1,497"),
        ("Curated Natural Voices + Speed Control", "$497"),
        ("ACX-Spec Mastering", "$697"),
        ("1,000 audio credits + square cover", "$997"),
        ("In-App Player + ZIP Download", "$197"),
        ("Opening & Closing Credit Files", "$297"),
    ],
    "stack_total": "$4,182",
    "faq": [
        ("Can I upload this to Audible / ACX?", "No. ACX requires human narration, and AI-narrated audio is not accepted there today. This is stated plainly so nobody buys expecting otherwise. Use it for Google Play Books, Kobo, your own store and reader magnets instead."),
        ("Which stores do accept AI-narrated audio?", "Google Play Books accepts it with disclosure, Kobo accepts it when the narrator is listed as a synthetic voice, and your own store accepts whatever you sell. Store policies change — verify before each launch."),
        ("Do audio credits come out of my main credits?", "No. Audio is a separate pool. 15 audio credits per book, and your main writing credits are untouched."),
        ("What files do I get?", "One MP3 per chapter at 192 kbps CBR, 44.1 kHz mono, plus opening and closing credit files, a 2400×2400 square cover, and a ZIP of everything."),
        ("Can I preview a voice first?", "Yes. Every voice has a preview sample, and you can re-preview at different speeds before committing credits."),
        ("What if the voice is not right?", "Re-generate with a different voice. Credits are only spent on actual generation, and exports are always free."),
        ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
    ],
    "ps": [
        "Your book already exists. The only thing missing is the version that plays in someone's ears on the way to work.",
        "Sixty-six audiobooks for less than the cost of narrating a single novel professionally — and the store policy reality is written right there in the FAQ, not buried.",
    ],
    "decision_lead": "Add the audiobook studio, curated voices, ACX-spec mastering and 1,000 audio credits to your BookSaga account for a one-time $47.",
    "yes_label": "Yes, Turn My Books Into Audio!",
    "yes_cap": "Yes, I want 1,000 audio credits and the full studio",
    "no_label": "No Thanks, Ebooks Are Enough",
    "no_cap": "I'll skip the audio-only audience",
    "no_url": "ds3.html",
})

# ============================================================== OTO 4 · Agency
PAGES.append({
    "slug": "oto4.html",
    "kind": "oto",
    "num": 4,
    "title": "BookSaga Agency — 100 Client Accounts, 5,000 Agency Credits",
    "desc": "Run BookSaga as a service. 100 client logins, a separate 5,000 credit pool, per-client allotments, suspension controls and a client licence PDF.",
    "name": "Agency",
    "hl": "Agency",
    "price": "$67",
    "price_num": "67",
    "regular": "$497",
    "pill": "Step 5 of 6 · Your order is confirmed",
    "h1_pre": "Stop Being The Only Person",
    "h1_hl": "Using This.",
    "lead": "Agency gives you 100 client accounts, each with its own login, drawing from a separate 5,000 credit pool. You set each client's allotment, you can suspend or reactivate them instantly, and your own main credits are never touched.",
    "hero_img": "images/booksaga-teamwork.png",
    "hero_alt": "BookSaga team working across multiple client accounts",
    "video_note": "2 minutes: creating a client, copying their login, setting an allotment",
    "stops_head": "Where your current plan stops",
    "stops_lead": "Right now every series in your workspace is yours. There is no way to hand work to a client, or to bill for it.",
    "stops": [
        ("Client accounts", "0", "100"),
        ("Agency credit pool", "0", "5,000"),
        ("Per-client allotments", "Not included", "Included"),
        ("Copy login details", "Not included", "One click"),
        ("Suspend / activate clients", "Not included", "Included"),
        ("Client commercial licence PDF", "Not included", "Included"),
    ],
    "problems": [
        ("users", "Clients cannot log in.", "There is no way to give someone their own workspace. Every project means you sitting in the chair."),
        ("lock", "You cannot meter usage.", "Without allotments, one client could burn your entire credit balance in a weekend and you would have no way to stop it."),
        ("copy", "Onboarding is manual.", "Writing out credentials, explaining the tool, chasing setup — per client, every time."),
        ("chart", "You are trading hours for money.", "The product is already built. The missing piece is a way to sell access to it repeatedly instead of doing the work yourself."),
    ],
    "intro_head": "Introducing BookSaga Agency",
    "intro_lead": "One workspace, one hundred client logins.",
    "intro_body": "Every client gets their own login and their own series. Their jobs draw from your separate agency pool — never from your main credits. You decide how much each client can spend, and you can copy their login details in one click, suspend them, or look into their workspace read-only whenever you want.",
    "unlocks": [
        ("users", "100 Client Accounts", "Each with an independent login and their own series list. No shared passwords, no shared workspace."),
        ("layers", "5,000 Agency Credits", "A completely separate pool. Client work never touches the credits you write with."),
        ("target", "Per-Client Allotments", "Default 100 credits each, changeable at any time. You decide who can spend what."),
        ("copy", "Copy Login Details", "One click copies email, password and login URL — ready to paste into your onboarding email."),
        ("lock", "Suspend / Activate", "Cut off a non-paying or over-spending client instantly, and restore them just as fast."),
        ("shield", "Read-Only Client View", "Look into any client's series without being able to change their work."),
        ("book", "Client Commercial Licence PDF", "A ready-made licence document you can hand over so the commercial rights are explicit."),
        ("star", "Clients Inherit Your Plan", "If you own Unlimited, your clients get full-length and 30-book series too. Your plan is the ceiling."),
    ],
    "how": [
        ("Create a client account", "Name, email, and an initial allotment. Login details are generated for you."),
        ("Copy and send the login", "One click puts email, password and URL on your clipboard."),
        ("Set the allotment", "Default 100 credits. Raise it for good clients, lower it for risky ones, change it whenever."),
        ("Monitor from the Clients page", "Pool balance, and every client's allotment, used and remaining, in one table."),
    ],
    "deep": [
        ("The economics of one client", "A five-book Standard series with covers is 110 credits. Your agency pool holds 5,000. That is roughly 45 complete five-book series before the pool runs dry — billable work you never write yourself.", ["5,000 agency credits", "110 credits per 5-book Standard series", "≈ 45 full series", "≈ 227 standard books with covers"]),
        ("What happens when credits run out", "It fails safely and in your favour. The client sees 'Not enough credits, contact your agency' — not a broken tool, and not a surprise invoice for you.", ["Client sees a clear contact-your-agency message", "Your main credits are never a fallback", "You top up the allotment or the pool when you choose"]),
        ("Clients inherit your plan, not a new one", "This is the detail most people miss. Your clients do not get a separate Basic plan — they work inside your entitlement. Own Unlimited and a client can produce full-length 30-book series.", ["Full-length if you own Unlimited", "30 books per series if you own Unlimited", "Their own credit allotment regardless"]),
    ],
    "math_head": "What 100 client accounts are worth",
    "math_lead": "Illustrative. Your pricing is your call — these are typical service rates in the niche.",
    "math": [
        ("One 5-book series, done for a client", "$500 - $2,500", "per project"),
        ("Monthly retainer, one client", "$200 - $800", "per month"),
        ("10 clients on retainer", "$2,000 - $8,000", "per month"),
        ("Your agency pool supports", "≈ 45 series", "before top-up"),
        ("BookSaga Agency, today", "$67", "one time"),
    ],
    "compare_head": "Without Agency vs With Agency",
    "compare": [
        ("Client logins you can create", "0", "100"),
        ("Credits clients can spend", "Your own 300", "Separate 5,000 pool"),
        ("Spend control", "None", "Per-client allotments"),
        ("Cut off a client", "Not possible", "Suspend instantly"),
        ("Oversight", "None", "Read-only view"),
        ("Commercial rights document", "You write it", "Licence PDF included"),
    ],
    "uses_head": "Five ways to run it as a business",
    "uses": [
        ("Done-for-you series service", "Charge per five-book series and hand over the KDP files."),
        ("Monthly publishing retainer", "Clients get a set number of books per month from their allotment."),
        ("White-label for other agencies", "Give a marketing agency client accounts they resell under their brand."),
        ("Ghostwriting with a portal", "The client logs in and watches their own series being built."),
        ("Author coaching, productised", "Teach the workflow and give each student an account to practise in."),
    ],
    "whofor": [
        "You already have people asking you to 'just do it for me'.",
        "You run a service business and want the writing automated.",
        "You want recurring revenue instead of one-off sales.",
        "You resell publishing services to other agencies.",
    ],
    "notfor": [
        "You only publish your own books and never want clients.",
        "You are not prepared to manage client relationships.",
        "You want a tool that bills your clients for you — this is not that.",
    ],
    "elsewhere": [
        ("Hire a ghostwriter per 5-book series", "$10,800 - $31,500", "per series"),
        ("White-label AI writing platform", "$500 - $2,000", "per month"),
        ("Client portal software", "$99 - $399", "per month"),
        ("Project management per client", "$50 - $150", "per month"),
        ("BookSaga Agency, today", "$67", "one time, 100 clients"),
    ],
    "stack": [
        ("100 Client Accounts", "$1,997"),
        ("5,000 Agency Credits (separate pool)", "$1,997"),
        ("Per-Client Allotment Controls", "$497"),
        ("Suspend / Activate + Read-Only Oversight", "$297"),
        ("Client Commercial Licence PDF", "$497"),
        ("One-Click Copy Login", "$197"),
    ],
    "stack_total": "$5,482",
    "faq": [
        ("Do clients need their own BookSaga subscription?", "No. Their login works inside your agency plan. They never buy anything."),
        ("Do client jobs use my main credits?", "No. Client work draws from the agency pool only. Your main credits are structurally protected."),
        ("What features do clients get?", "Whatever your own plan gives you. If you own Unlimited, your clients can produce full-length books and 30-book series. If you own Basic, they get Basic limits."),
        ("What if a client runs out of credits?", "They see 'Not enough credits, contact your agency'. You raise their allotment or the pool whenever you decide."),
        ("Can I revoke a client's access?", "Yes — suspend them instantly. Their work stays intact and you can reactivate them later."),
        ("Is there a client licence document?", "Yes, a commercial licence PDF is included so the rights between you and your client are written down."),
        ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
    ],
    "ps": [
        "You already own a machine that writes series. Agency is the part that lets other people pay to use it.",
        "One client on a 200 dollar retainer pays for this three times over in the first month.",
    ],
    "decision_lead": "Add 100 client accounts, a separate 5,000 credit pool and full agency controls to your BookSaga account for a one-time $67.",
    "yes_label": "Yes, I Want To Sell This As A Service!",
    "yes_cap": "Yes, I want 100 clients and 5,000 agency credits",
    "no_label": "No Thanks, I'll Keep It To Myself",
    "no_cap": "I only want to publish my own books",
    "no_url": "ds4.html",
})

# ============================================================== OTO 5 · Reseller
PAGES.append({
    "slug": "oto5.html",
    "kind": "oto",
    "num": 5,
    "title": "BookSaga Reseller + Franchise — 100 Licences, Keep 100%",
    "desc": "Sell BookSaga as your own product. 100 reseller licences, a dashboard to create/track/revoke, and a complete franchise kit. Keep 100% of what you charge.",
    "name": "Reseller + Franchise",
    "hl": "Reseller",
    "price": "$97",
    "price_num": "97",
    "regular": "$997",
    "pill": "Step 6 of 6 · Your order is confirmed",
    "h1_pre": "You Can Also Sell The",
    "h1_hl": "Product Itself.",
    "lead": "Reseller gives you 100 licences. Each one creates a working BookSaga Basic account for someone else. You set the price, you keep 100% of it, and the franchise kit gives you the sales page, emails, social posts, banners and demo video to sell with.",
    "hero_img": "images/Bundle_580ac5.png",
    "hero_alt": "BookSaga bundle of publishing products",
    "video_note": "2 minutes: creating a licence, sending it, tracking it, revoking it",
    "stops_head": "Where your current plan stops",
    "stops_lead": "You can publish with BookSaga. Right now you cannot sell BookSaga.",
    "stops": [
        ("Reseller licences", "0", "100"),
        ("Reseller dashboard", "Not included", "Create / track / revoke"),
        ("Revoke a licence", "Not possible", "Licence returns to you"),
        ("Sales page template", "Not included", "HTML download"),
        ("Email swipes + social posts", "Not included", "Included"),
        ("Banners + demo video", "Not included", "Included"),
    ],
    "problems": [
        ("rocket", "The product is already built.", "You are using it. The only thing missing is a way to let other people buy access to it through you."),
        ("copy", "Selling needs assets you do not have.", "A sales page, emails, social posts, banners, a demo. Building those takes longer than the selling does."),
        ("shield", "Refunds need a revoke switch.", "If a customer refunds, the licence has to come back. Without a dashboard you have no way to reclaim it."),
        ("chart", "One sale per customer is a dead end.", "Publishing is one business. Selling access to publishing is a second business on top of it."),
    ],
    "intro_head": "Introducing BookSaga Reseller + Franchise",
    "intro_lead": "Your own branded on-ramp to the product you already use.",
    "intro_body": "Create a licence, send it to a customer, and they get a working BookSaga Basic account. Track every licence from one dashboard. Revoke one and it returns to your pool. The franchise kit supplies the sales page HTML, promo email swipes, social posts, banners and demo video — so the marketing exists before you start.",
    "unlocks": [
        ("rocket", "100 Reseller Licences", "Each licence provisions a working BookSaga Basic account. You decide who gets one and what they pay."),
        ("chart", "Reseller Dashboard", "Create, track and revoke from one place. Every licence and its status, visible at a glance."),
        ("lock", "Revoke = Licence Back", "A refunded or abusive customer can be cut off, and the licence returns to your pool to be sold again."),
        ("copy", "Ready-Made Sales Page", "A downloadable HTML sales page you can host and point your traffic at."),
        ("bolt", "Promo Email Swipes", "Written emails for launch, follow-up and last-call — paste and send."),
        ("image", "Social Posts + Banners", "Ad graphics and post copy sized for the usual channels."),
        ("star", "Demo Video Link", "A ready demo you can show instead of explaining the tool yourself."),
        ("shield", "Keep 100% Of What You Charge", "No revenue share, no per-sale cut. You set the price and keep it."),
    ],
    "how": [
        ("Create a licence", "From the reseller dashboard. One licence, one account."),
        ("Send it to your customer", "They get a working BookSaga Basic account with 100 credits."),
        ("Track it", "The dashboard shows every licence, who holds it and its current state."),
        ("Revoke if needed", "Refund or abuse — revoke it, and the licence returns to your pool."),
    ],
    "deep": [
        ("What your customer actually gets", "Be clear about this before you sell, because it is not the same as a direct Basic purchase. It is a real Basic account — full series engine, Series Bible, continuity, covers, metadata, KDP exports — but with 100 credits and no upgrade path.", ["Short and Standard lengths", "3 active series, 5 books per series", "100 one-time credits (direct buyers get 300)", "No OTO upgrades available from that account"]),
        ("The economics, honestly", "This is the one offer where the maths deserves scrutiny rather than hype. Worst case: 100 customers each burn their 100 credits on short books. That is roughly 98 dollars of AI cost against 97 dollars of revenue — deliberately thin at the extreme.", ["100 customers × 100 credits = 10,000 credits", "≈ 1,000 short books at 10 credits each", "≈ $98 worst-case AI cost", "Typical usage is far lower — but monitor it after launch"]),
        ("Selling without being a marketer", "The kit exists because most people who own a good product are not copywriters. Everything you need to make the first offer is included — you are choosing the channel and the price, not writing the assets.", ["Host the HTML sales page anywhere", "Send the email swipes to your list", "Post the social copy and banners", "Link the demo video"]),
    ],
    "math_head": "What 100 licences can be worth",
    "math_lead": "Illustrative. You set the price — these are common reseller price points.",
    "math": [
        ("100 licences at $27", "$2,700", "your revenue"),
        ("100 licences at $47", "$4,700", "your revenue"),
        ("100 licences at $97", "$9,700", "your revenue"),
        ("Your cost for the licences", "$97", "one time"),
        ("Worst-case AI cost to you", "≈ $98", "if every credit is used"),
    ],
    "compare_head": "Without Reseller vs With Reseller",
    "compare": [
        ("Licences you can sell", "0", "100"),
        ("Sales page", "You build it", "HTML included"),
        ("Emails / social / banners", "You write them", "Included"),
        ("Demo video", "You record it", "Link included"),
        ("Revoke on refund", "Not possible", "One click"),
        ("Revenue share", "n/a", "You keep 100%"),
    ],
    "uses_head": "Five ways resellers use it",
    "uses": [
        ("Sell to your existing audience", "Your list, your socials — offer access at your own price."),
        ("Bundle with a course", "Include a licence as a bonus inside a publishing course."),
        ("Local and offline markets", "Sell to people who want to publish but will never find this tool themselves."),
        ("Recruit a small affiliate team", "Hand licences to affiliates who sell at a markup."),
        ("Test demand before scaling", "Sell 10 licences first, then decide whether to buy more."),
    ],
    "whofor": [
        "You already have an audience, a list or a community.",
        "You sell publishing, marketing or business courses.",
        "You want a product to resell without building one.",
        "You are comfortable setting your own price.",
    ],
    "notfor": [
        "You have no audience and no plan to get traffic.",
        "You expect the licences to sell themselves.",
        "You want your customers to have the full 300 credits and OTO upgrades — that is a direct sale, not a licence.",
    ],
    "elsewhere": [
        ("White-label SaaS reseller deal", "$1,000 - $5,000", "per year, plus revenue share"),
        ("Sales page copywriter", "$500 - $1,500", "per page"),
        ("Email sequence copywriter", "$300 - $800", "per sequence"),
        ("Ad creative + banners", "$200 - $600", "per set"),
        ("BookSaga Reseller + Franchise, today", "$97", "one time, keep 100%"),
    ],
    "stack": [
        ("100 Reseller Licences", "$2,997"),
        ("Reseller Dashboard (create / track / revoke)", "$497"),
        ("Ready-Made Sales Page (HTML)", "$997"),
        ("Promo Email Swipes", "$497"),
        ("Social Posts + Banners", "$497"),
        ("Demo Video Link", "$297"),
    ],
    "stack_total": "$5,782",
    "faq": [
        ("What exactly does my customer get?", "A working BookSaga Basic account: full series engine, Series Bible, continuity, covers, metadata and KDP exports. Short and Standard lengths, 3 active series, 5 books per series, and 100 one-time credits. No OTO upgrades from that account."),
        ("Do I keep all the money?", "Yes. You set the price and keep 100%. There is no revenue share and no per-sale cut."),
        ("Can I revoke a licence?", "Yes. Revoke it from the dashboard and it returns to your pool — useful for refunds or abuse."),
        ("Is there a limit on what I can charge?", "No. You set the price."),
        ("What if I sell all 100?", "Then you need more licences — that is a conversation, not a limitation of the dashboard."),
        ("Is this the same as Agency?", "No. Agency is for running client accounts yourself. Reseller is for selling licences so other people own their accounts."),
        ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
    ],
    "ps": [
        "You are already the customer. Reseller just makes you the supplier too.",
        "Even at 27 dollars a licence, selling all one hundred is 2,700 dollars from a 97 dollar purchase.",
    ],
    "decision_lead": "Add 100 reseller licences, the reseller dashboard and the complete franchise kit to your BookSaga account for a one-time $97.",
    "yes_label": "Yes, Let Me Sell BookSaga!",
    "yes_cap": "Yes, I want 100 licences and the franchise kit",
    "no_label": "No Thanks, I'll Just Publish",
    "no_cap": "I don't want to sell the product itself",
    "no_url": "ds5.html",
})

# ============================================================== DOWNSIDELLS
DS = [
    {
        "slug": "ds1.html", "num": 1,
        "title": "BookSaga Unlimited Lite — Full-Length, 25 Series, 1,000 Credits",
        "desc": "The lighter Unlimited. Full-length novels, 30 books per series, print wraps and Box Sets, with 25 active series and 1,000 credits — $27 instead of $47.",
        "name": "Unlimited Lite", "hl": "Lite", "price": "$27", "price_num": "27", "regular": "$147",
        "h1_pre": "Wait — You Don't Have To Go Back To",
        "h1_hl": "Five Books.",
        "lead": "You passed on full Unlimited. Fair enough. But the 5-book ceiling and the missing paperback are the two things that will actually stop you. Unlimited Lite keeps the full-length engine, the 30-book series cap, print-ready wraps and Box Sets — it just trims the active series and the credit stack.",
        "hero_img": "images/booksaga-product-mockup.png", "hero_alt": "BookSaga series workspace",
        "stops_head": "What Unlimited Lite still unlocks",
        "stops_lead": "Everything that changes what you can actually produce. Only the volume is trimmed.",
        "stops": [
            ("Books per series", "5", "30"),
            ("Length preset", "Short + Standard", "+ Full-Length"),
            ("Paperback full-wrap cover", "Not included", "Included"),
            ("Box Set Builder", "Not included", "Included"),
            ("Active series at once", "3", "25"),
            ("One-time credits", "300", "1,300"),
        ],
        "problems": [
            ("book", "Five books is still a ceiling.", "The series you are writing now ends at book five whether the arc needs it to or not."),
            ("image", "No wrap, no paperback.", "Without a print-ready spine there is no physical version of your book."),
            ("layers", "No box set, no second product.", "The highest-margin listing in any series stays out of reach."),
        ],
        "intro_head": "Introducing BookSaga Unlimited Lite",
        "intro_lead": "The ceilings come off. The volume is smaller.",
        "intro_body": "Full-Length novels. 30 books per series. Print-ready paperback wraps. Box Set Builder. 1,000 extra credits stacked on your existing 300. The only differences from full Unlimited are 25 active series instead of unlimited, and 1,000 credits instead of 3,000.",
        "unlocks": [
            ("book", "Full-Length Novels", "25-30 chapters, ~55,000 words. The length that supports premium pricing."),
            ("layers", "30 Books Per Series", "Six times your current runway."),
            ("grid", "25 Active Series", "Not unlimited, but far beyond the 3 you have now."),
            ("image", "Paperback Full-Wrap Cover PDF", "Front, spine and back at 300 DPI."),
            ("star", "Box Set Builder", "A second, higher-priced listing from the same books."),
            ("bolt", "1,000 Extra Credits", "1,300 total. Roughly 27 full-length books with covers."),
        ],
        "how": [
            ("Open a series", "Existing or new — nothing to migrate."),
            ("Pick Full-Length", "The preset appears in the create flow and on existing series."),
            ("Generate the run", "Sequential writing keeps the Series Bible accurate."),
            ("Export", "EPUB3, print interior, paperback wrap, Box Set, metadata."),
        ],
        "deep": [
            ("What you give up versus full Unlimited", "Two things only: active series goes from unlimited to 25, and credits from 3,000 to 1,000. Every format, cap and builder stays identical.", ["Full-Length engine — included", "30 books per series — included", "Print wrap + Box Sets — included", "25 active series vs unlimited", "1,000 credits vs 3,000"]),
            ("Is 25 active series actually a limit?", "For most publishers, no. Twenty-five concurrent series is a catalogue most people never reach. The realistic constraint is credits, not series slots.", ["1,000 credits ≈ 27 full-length books with covers", "1,300 total with your existing 300", "Credits are one-time and never expire"]),
        ],
        "math_head": "What the length change is worth",
        "math_lead": "Illustrative KU and list-price maths.",
        "math": [
            ("Short ~65 pages", "≈ $0.29", "per full read"),
            ("Standard ~160 pages", "≈ $0.72", "per full read"),
            ("Full-length ~290 pages", "≈ $1.31", "per full read"),
            ("Ebook at $4.99 / 70%", "$3.49", "per sale"),
            ("Box set at $9.99 / 70%", "≈ $6.99", "per sale"),
        ],
        "compare_head": "Unlimited Lite vs Full Unlimited",
        "compare": [
            ("Full-Length engine", "Included", "Included"),
            ("Books per series", "30", "30"),
            ("Print wrap + Box Sets", "Included", "Included"),
            ("Active series", "25", "Unlimited"),
            ("Extra credits", "1,000", "3,000"),
            ("Price", "$27", "$47"),
        ],
        "uses_head": "Who this is right for",
        "uses": [
            ("One serious series", "You want one long, full-length series done properly."),
            ("Adding paperbacks", "You want a physical edition of books you have already written."),
            ("A box set launch", "You want the higher-priced bundle without unlimited slots."),
            ("Testing the format", "Try full-length on a smaller credit budget before scaling."),
        ],
        "whofor": ["You passed on full Unlimited but still hit the 5-book wall.", "You want paperbacks and box sets.", "One or two long series is enough for you."],
        "notfor": ["You plan to run dozens of series in parallel.", "You need the full 3,000 credit stack."],
        "elsewhere": [
            ("Ghostwritten full-length novel", "$1,200 - $4,000", "per book"),
            ("Print-ready wrap design", "$150 - $400", "per book"),
            ("Box set formatting", "$100 - $300", "per set"),
            ("BookSaga Unlimited Lite, today", "$27", "one time"),
        ],
        "stack": [
            ("Full-Length Novel Engine", "$997"),
            ("30 Books Per Series + Add More Parts", "$697"),
            ("25 Active Series", "$497"),
            ("Paperback Full-Wrap Cover PDF", "$497"),
            ("Box Set Builder", "$697"),
            ("1,000 one-time credits", "$497"),
        ],
        "stack_total": "$3,882",
        "faq": [
            ("How is this different from full Unlimited?", "Two things: 25 active series instead of unlimited, and 1,000 credits instead of 3,000. Every format, cap and builder is identical."),
            ("Can I upgrade to full Unlimited later?", "This is a launch-price offer. If you want the full credit stack, full Unlimited is the one-time decision."),
            ("Do my existing 300 credits carry over?", "Yes. Credits stack — 1,300 total."),
            ("Does 'Lite' mean fewer formats?", "No. Full-Length, 30 books per series, print wraps and Box Sets are all included."),
            ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
        ],
        "ps": ["Full-length and paperbacks are not volume features. They change what you can sell. That is what 27 dollars is buying here."],
        "decision_lead": "Get the full-length engine, 30-book series, print wraps and Box Sets with 25 active series and 1,000 credits — one-time $27.",
        "yes_label": "Yes, Give Me Unlimited Lite!",
        "yes_cap": "Yes, I want full-length and paperbacks at $27",
        "no_label": "No Thanks, Move Me To The Next Step",
        "no_cap": "I'll stay at 5 books and keep going",
        "no_url": "oto2.html",
    },
    {
        "slug": "ds2.html", "num": 2,
        "title": "BookSaga Done-For-You Lite — 40 Series Templates + Ideas",
        "desc": "40 tested series templates, a lite selection of DFY ideas, blurbs and keyword packs, and one-click prefill — $17 instead of $37.",
        "name": "DFY Lite", "hl": "DFY Lite", "price": "$17", "price_num": "17", "regular": "$97",
        "h1_pre": "Before You Guess With",
        "h1_hl": "110 Credits.",
        "lead": "A five-book Standard series with covers costs 110 credits — over a third of everything you own. Done-For-You Lite gives you 40 tested series templates plus a lite selection of ideas, blurbs and keyword packs, so the first series you generate is not a guess.",
        "hero_img": "images/amazonseries_b050ec.png", "hero_alt": "Amazon series page",
        "stops_head": "What DFY Lite unlocks",
        "stops_lead": "The de-risking, at the smallest possible entry point.",
        "stops": [
            ("Series templates", "0", "40"),
            ("DFY series ideas", "0", "Lite selection"),
            ("Blurb templates", "0", "Lite selection"),
            ("Keyword packs", "0", "Lite selection"),
            ("Sample covers", "0", "Included"),
            ("One-click prefill", "Not included", "Included"),
        ],
        "problems": [
            ("target", "The wrong idea costs 110 credits.", "There is no refund on a series that does not sell."),
            ("clock", "Research eats your first week.", "Days of browsing before a single word exists."),
            ("copy", "Blurbs and keywords are a separate craft.", "Most first-time publishers write a synopsis instead of a sales page."),
        ],
        "intro_head": "Introducing BookSaga Done-For-You Lite",
        "intro_lead": "40 templates. One click. No blank page.",
        "intro_body": "Forty series templates across the twelve categories, each with a concept, hook, core cast, complete five-book arc, tone, audience and sample cover. Plus a lite selection of DFY ideas, blurb templates and keyword packs. Full Done-For-You adds 80 more templates and the complete library.",
        "unlocks": [
            ("grid", "40 Series Templates", "Across Fantasy, Romance, Mystery & Thriller, Historical, YA, Children's, Sci-Fi, Horror, Business, Health, Faith and Self-Help."),
            ("bolt", "One-Click Prefill", "The Create Series form arrives filled in — and fully editable."),
            ("book", "DFY Series Ideas (Lite)", "Title, premise and hook by niche."),
            ("copy", "Blurb Templates (Lite)", "Genre-appropriate descriptions to adapt."),
            ("chart", "Keyword Packs (Lite)", "Starting phrases for the seven KDP slots."),
            ("image", "Sample Cover Per Template", "See the promise before spending a credit."),
        ],
        "how": [
            ("Browse the library", "Sort by category or badge."),
            ("Click Use This Template", "The form prefills. Change anything."),
            ("Generate", "Same engine, same Bible, same continuity."),
            ("Publish", "Pull the matching blurb and keywords."),
        ],
        "deep": [
            ("Lite vs full Done-For-You", "Same engine, same one-click prefill, same sample covers. The difference is the size of the library: 40 templates and a lite selection, versus 120 templates and the complete ideas, blurbs and keyword library.", ["40 templates vs 120", "Lite ideas vs 500+", "Lite blurb/keyword selection vs full", "Identical prefill and sample covers"]),
            ("The credit maths", "110 credits for a five-book Standard series with covers. On 300 credits that is over a third of your budget on one guess.", ["5 books × 20 = 100 credits", "5 covers × 2 = 10 credits", "Total 110 of your 300"]),
        ],
        "math_head": "What a wrong guess costs",
        "math_lead": "Illustrative, five-book Standard series with covers.",
        "math": [
            ("One wrong five-book series", "110 credits", "gone"),
            ("Your total credits", "300", "≈ 2.7 series"),
            ("Templates in DFY Lite", "40", "before you write"),
            ("Cost of DFY Lite", "$17", "one time"),
        ],
        "compare_head": "DFY Lite vs Full DFY",
        "compare": [
            ("Series templates", "40", "120"),
            ("Series ideas", "Lite", "500+"),
            ("Blurb templates", "Lite", "Full library"),
            ("Keyword packs", "Lite", "Full library"),
            ("One-click prefill", "Included", "Included"),
            ("Price", "$17", "$37"),
        ],
        "uses_head": "Good fits for DFY Lite",
        "uses": [
            ("First series", "Start from a tested shape instead of a guess."),
            ("One category only", "You publish in a single genre and need shapes for it."),
            ("Small budget", "De-risk without spending 37 dollars."),
            ("Quick test", "Try the template workflow before committing to the full library."),
        ],
        "whofor": ["You want the idea de-risked at the lowest entry price.", "You publish in one or two categories.", "You are about to spend 110 credits."],
        "notfor": ["You want the complete 120-template library.", "You already have a tested idea and a clear arc."],
        "elsewhere": [
            ("Niche research", "$300 - $900", "per niche"),
            ("Blurb copywriter", "$50 - $150", "per book"),
            ("Keyword tool", "$30 - $99", "per month"),
            ("BookSaga DFY Lite, today", "$17", "one time"),
        ],
        "stack": [
            ("40 Series Templates", "$697"),
            ("DFY Series Ideas (Lite)", "$297"),
            ("Blurb Templates (Lite)", "$197"),
            ("Keyword Packs (Lite)", "$197"),
            ("Sample Covers", "$297"),
            ("One-Click Prefill", "$297"),
        ],
        "stack_total": "$1,982",
        "faq": [
            ("How is this different from full Done-For-You?", "40 templates instead of 120, and a lite selection of ideas, blurbs and keyword packs. One-click prefill and sample covers are identical."),
            ("Do templates cost credits?", "No. Browsing and prefilling are free. Credits are only spent on actual generation."),
            ("Are templates locked?", "No. Every prefilled field is editable."),
            ("Does this include Unlimited?", "No — these are separate offers. Templates live only in DFY Lite and DFY."),
            ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
        ],
        "ps": ["Seventeen dollars against 110 credits on a guess. That is the whole argument."],
        "decision_lead": "Get 40 tested series templates plus the lite ideas, blurb and keyword library for a one-time $17.",
        "yes_label": "Yes, Give Me 40 Templates!",
        "yes_cap": "Yes, de-risk my first series for $17",
        "no_label": "No Thanks, Move Me To The Next Step",
        "no_cap": "I'll take my chances with the credits",
        "no_url": "oto3.html",
    },
    {
        "slug": "ds3.html", "num": 3,
        "title": "BookSaga Audiobook Lite — 300 Audio Credits, Full Studio",
        "desc": "The full audiobook studio, curated voices and ACX-spec mastering with 300 audio credits — roughly 20 audiobooks — $27 instead of $47.",
        "name": "Audiobook Lite", "hl": "Audio Lite", "price": "$27", "price_num": "27", "regular": "$147",
        "h1_pre": "Your Books Can Still",
        "h1_hl": "Speak.",
        "lead": "You passed on the full audiobook offer. Audiobook Lite keeps the entire studio — the voices, the speed control, the ACX-spec mastering, the per-chapter MP3s, the square cover and the ZIP — with 300 audio credits instead of 1,000. Roughly 20 audiobooks.",
        "hero_img": "images/inside1_949c81.png", "hero_alt": "Chapter opening page",
        "stops_head": "What Audiobook Lite unlocks",
        "stops_lead": "Identical studio. Smaller credit pool.",
        "stops": [
            ("Audiobook module", "Not included", "Included"),
            ("Curated AI voices", "0", "US + UK, M/F"),
            ("ACX-spec mastering", "Not included", "Included"),
            ("Square cover 2400×2400", "Not included", "Included"),
            ("Audio credits", "0", "300"),
            ("Audiobooks you can produce", "0", "≈ 20"),
        ],
        "problems": [
            ("mic", "Audio listeners are unreachable.", "Commuters and gym-goers who never open an ebook."),
            ("download", "Manual audio formatting is miserable.", "Chapter splits, loudness, peaks, room tone, credits."),
            ("star", "One format, one price.", "Audio is a third listing from the same manuscript."),
        ],
        "intro_head": "Introducing BookSaga Audiobook Lite",
        "intro_lead": "The whole studio. Twenty books' worth of credits.",
        "intro_body": "Same voices, same previews, same speed control, same ACX-spec mastering, same per-chapter MP3s, same square cover and ZIP download. The only difference from full Audiobook is 300 audio credits instead of 1,000.",
        "unlocks": [
            ("mic", "Full Audiobook Studio", "Narrate any finished book in any series."),
            ("users", "Curated Natural Voices", "US and UK English, male and female, with previews."),
            ("clock", "Speed Control 0.8× - 1.2×", "Match pacing to genre."),
            ("download", "One MP3 Per Chapter", "192 kbps CBR, 44.1 kHz, mono."),
            ("chart", "ACX-Spec Mastering", "RMS, peak, noise floor, room tone, credits."),
            ("image", "2400×2400 Square Cover", "From your existing cover art."),
        ],
        "how": [
            ("Pick a finished book", "Completed manuscripts only."),
            ("Preview a voice", "Hear it before spending a credit."),
            ("Set speed and generate", "Per-chapter MP3s, mastered."),
            ("Download the ZIP", "Or listen in the app first."),
        ],
        "deep": [
            ("Where you can publish it", "Stated plainly, same as the full offer: not Audible through ACX. Google Play Books, Kobo and your own store accept AI-narrated audio with the right disclosure.", ["Google Play Books — with disclosure", "Kobo — narrator listed as synthetic", "Your own store — Payhip, Gumroad, Shopify", "Reader magnet — free audio prequel", "Verify store policy before publishing"]),
            ("Lite vs full Audiobook", "One difference only: 300 audio credits instead of 1,000. Every feature, voice, mastering step and export is identical.", ["300 credits ≈ 20 audiobooks", "1,000 credits ≈ 66 audiobooks", "15 credits per book", "Main credits untouched"]),
        ],
        "math_head": "Three listings, one manuscript",
        "math_lead": "Illustrative.",
        "math": [
            ("Ebook at $4.99 / 70%", "$3.49", "per sale"),
            ("Paperback at $12.99", "≈ $4.00", "per sale"),
            ("Audiobook at $9.99 / 70%", "≈ $6.99", "per sale"),
            ("Audiobooks on 300 credits", "≈ 20", "before top-up"),
        ],
        "compare_head": "Audiobook Lite vs Full Audiobook",
        "compare": [
            ("Studio, voices, mastering", "Included", "Included"),
            ("Per-chapter MP3 + cover + ZIP", "Included", "Included"),
            ("Audio credits", "300", "1,000"),
            ("Audiobooks", "≈ 20", "≈ 66"),
            ("Price", "$27", "$47"),
        ],
        "uses_head": "Good fits for Audio Lite",
        "uses": [
            ("Audio on one series", "Narrate a five-book series and test the market."),
            ("A free audio prequel", "Give book one away as audio."),
            ("Bundling on your own store", "Ebook plus audio at a higher price."),
            ("Trying before scaling", "Twenty books is enough to learn the workflow."),
        ],
        "whofor": ["You have finished books and want audio.", "You want to test audio demand first.", "You sell on your own store."],
        "notfor": ["You want to upload to Audible via ACX.", "You need 60+ audiobooks immediately."],
        "elsewhere": [
            ("Pro narration per finished hour", "$200 - $400", "6-8 hours per novel"),
            ("Audio mastering service", "$50 - $120", "per finished hour"),
            ("Audiobook cover", "$75 - $250", "per title"),
            ("BookSaga Audiobook Lite, today", "$27", "one time"),
        ],
        "stack": [
            ("Audiobook Studio", "$1,497"),
            ("Curated Voices + Speed", "$497"),
            ("ACX-Spec Mastering", "$697"),
            ("Square Cover + Player + ZIP", "$397"),
            ("300 audio credits", "$297"),
        ],
        "stack_total": "$3,385",
        "faq": [
            ("Can I upload to Audible?", "No. ACX requires human narration. Use Google Play Books, Kobo or your own store."),
            ("How is this different from full Audiobook?", "300 audio credits instead of 1,000. Everything else is identical."),
            ("Do audio credits touch my main credits?", "No, separate pool."),
            ("What files do I get?", "Per-chapter MP3 at 192 kbps, credit files, 2400×2400 cover, and a ZIP."),
            ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
        ],
        "ps": ["Twenty audiobooks for 27 dollars, from books that already exist."],
        "decision_lead": "Get the full audiobook studio and 300 audio credits for a one-time $27.",
        "yes_label": "Yes, Give Me Audio Lite!",
        "yes_cap": "Yes, I want ~20 audiobooks for $27",
        "no_label": "No Thanks, Move Me To The Next Step",
        "no_cap": "I'll skip audio for now",
        "no_url": "oto4.html",
    },
    {
        "slug": "ds4.html", "num": 4,
        "title": "BookSaga Agency Lite — 25 Client Accounts, 2,000 Credits",
        "desc": "Run BookSaga as a service with 25 client logins, a separate 2,000 credit pool, allotments, suspension and the client licence PDF — $47 instead of $67.",
        "name": "Agency Lite", "hl": "Agency Lite", "price": "$47", "price_num": "47", "regular": "$297",
        "h1_pre": "You Can Still Let Clients",
        "h1_hl": "Log In.",
        "lead": "You passed on full Agency. Agency Lite keeps everything that makes it a business — client logins, a separate credit pool, per-client allotments, suspension, read-only oversight and the licence PDF — with 25 clients and 2,000 credits.",
        "hero_img": "images/booksaga-teamwork.png", "hero_alt": "BookSaga team",
        "stops_head": "What Agency Lite unlocks",
        "stops_lead": "Identical controls. Smaller client roster.",
        "stops": [
            ("Client accounts", "0", "25"),
            ("Agency credit pool", "0", "2,000"),
            ("Per-client allotments", "Not included", "Included"),
            ("Suspend / activate", "Not included", "Included"),
            ("Read-only oversight", "Not included", "Included"),
            ("Client licence PDF", "Not included", "Included"),
        ],
        "problems": [
            ("users", "Clients cannot log in.", "Every project means you in the chair."),
            ("lock", "You cannot meter usage.", "One client could burn the whole balance."),
            ("chart", "You trade hours for money.", "The product is built — access to it is not."),
        ],
        "intro_head": "Introducing BookSaga Agency Lite",
        "intro_lead": "Twenty-five client logins, fully metered.",
        "intro_body": "Each client gets their own login and their own series, drawing from a separate 2,000 credit pool. You set allotments, copy login details in one click, suspend anyone instantly, and look in read-only whenever you want.",
        "unlocks": [
            ("users", "25 Client Accounts", "Independent logins and series."),
            ("layers", "2,000 Agency Credits", "Separate pool — main credits untouched."),
            ("target", "Per-Client Allotments", "Default 100, changeable any time."),
            ("copy", "Copy Login Details", "One click, ready to paste."),
            ("lock", "Suspend / Activate", "Cut off or restore instantly."),
            ("shield", "Client Licence PDF", "Commercial rights written down."),
        ],
        "how": [
            ("Create a client", "Name, email, allotment."),
            ("Copy and send the login", "One click to clipboard."),
            ("Set the allotment", "Default 100 credits."),
            ("Monitor", "Pool balance and every client's usage in one table."),
        ],
        "deep": [
            ("What 2,000 credits can deliver", "A five-book Standard series with covers is 110 credits. Two thousand credits is roughly 18 complete five-book series — billable work you never write yourself.", ["2,000 agency credits", "110 per 5-book Standard series", "≈ 18 full series", "≈ 90 standard books with covers"]),
            ("Lite vs full Agency", "Two differences: 25 clients instead of 100, and 2,000 credits instead of 5,000. Every control, view and document is identical.", ["25 vs 100 client accounts", "2,000 vs 5,000 credits", "Allotments, suspension, oversight — same", "Client licence PDF — same"]),
        ],
        "math_head": "What 25 clients are worth",
        "math_lead": "Illustrative service pricing.",
        "math": [
            ("One 5-book series for a client", "$500 - $2,500", "per project"),
            ("Monthly retainer, one client", "$200 - $800", "per month"),
            ("5 clients on retainer", "$1,000 - $4,000", "per month"),
            ("Your pool supports", "≈ 18 series", "before top-up"),
        ],
        "compare_head": "Agency Lite vs Full Agency",
        "compare": [
            ("Client accounts", "25", "100"),
            ("Agency credits", "2,000", "5,000"),
            ("Allotments + suspension", "Included", "Included"),
            ("Read-only oversight", "Included", "Included"),
            ("Client licence PDF", "Included", "Included"),
            ("Price", "$47", "$67"),
        ],
        "uses_head": "Good fits for Agency Lite",
        "uses": [
            ("Starting a service", "Test demand with a handful of clients."),
            ("One agency client", "Deliver a full series under one login."),
            ("Small coaching cohort", "Give each student an account."),
            ("Wholesale to a marketer", "Let them resell under their brand."),
        ],
        "whofor": ["People are already asking you to do it for them.", "You want recurring revenue.", "You are testing a service business."],
        "notfor": ["You only publish your own books.", "You need 100 client seats immediately."],
        "elsewhere": [
            ("Ghostwriter per 5-book series", "$10,800 - $31,500", "per series"),
            ("White-label AI platform", "$500 - $2,000", "per month"),
            ("Client portal software", "$99 - $399", "per month"),
            ("BookSaga Agency Lite, today", "$47", "one time"),
        ],
        "stack": [
            ("25 Client Accounts", "$697"),
            ("2,000 Agency Credits", "$797"),
            ("Allotment Controls", "$497"),
            ("Suspension + Read-Only Oversight", "$297"),
            ("Client Licence PDF", "$497"),
        ],
        "stack_total": "$2,785",
        "faq": [
            ("Do clients need their own subscription?", "No. They log in inside your plan."),
            ("Do client jobs use my main credits?", "No, separate agency pool."),
            ("What features do clients get?", "Whatever your own plan gives you."),
            ("Can I revoke access?", "Yes, suspend instantly."),
            ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
        ],
        "ps": ["One retainer client covers this in the first month."],
        "decision_lead": "Get 25 client accounts and a separate 2,000 credit pool for a one-time $47.",
        "yes_label": "Yes, Give Me Agency Lite!",
        "yes_cap": "Yes, I want 25 clients for $47",
        "no_label": "No Thanks, Move Me To The Last Step",
        "no_cap": "I'll keep it to myself",
        "no_url": "oto5.html",
    },
    {
        "slug": "ds5.html", "num": 5,
        "title": "BookSaga Reseller Lite — 50 Licences + Full Franchise Kit",
        "desc": "Sell BookSaga as your own product with 50 reseller licences, the reseller dashboard and the complete franchise kit — $67 instead of $97.",
        "name": "Reseller Lite", "hl": "Reseller Lite", "price": "$67", "price_num": "67", "regular": "$497",
        "h1_pre": "You Can Still Sell The",
        "h1_hl": "Product.",
        "lead": "You passed on full Reseller. Reseller Lite keeps the whole machine — the licences, the dashboard, the sales page, the email swipes, the social posts, the banners, the demo video — with 50 licences instead of 100.",
        "hero_img": "images/Bundle_580ac5.png", "hero_alt": "BookSaga bundle",
        "stops_head": "What Reseller Lite unlocks",
        "stops_lead": "Identical kit. Half the licences.",
        "stops": [
            ("Reseller licences", "0", "50"),
            ("Reseller dashboard", "Not included", "Create / track / revoke"),
            ("Sales page HTML", "Not included", "Included"),
            ("Email swipes + social", "Not included", "Included"),
            ("Banners + demo video", "Not included", "Included"),
            ("Revenue share", "n/a", "You keep 100%"),
        ],
        "problems": [
            ("rocket", "The product is already built.", "You just cannot sell access to it yet."),
            ("copy", "Selling needs assets.", "Sales page, emails, posts, banners, demo — all missing."),
            ("shield", "Refunds need a revoke switch.", "Without a dashboard you cannot reclaim a licence."),
        ],
        "intro_head": "Introducing BookSaga Reseller Lite",
        "intro_lead": "Fifty licences. The complete kit.",
        "intro_body": "Create a licence, send it, track it, revoke it. Fifty of them. The franchise kit — sales page HTML, promo email swipes, social posts, banners and demo video — is identical to the full offer.",
        "unlocks": [
            ("rocket", "50 Reseller Licences", "Each provisions a working BookSaga Basic account."),
            ("chart", "Reseller Dashboard", "Create, track, revoke."),
            ("lock", "Revoke = Licence Back", "Reclaim on refund."),
            ("copy", "Sales Page + Email Swipes", "Ready to host and send."),
            ("image", "Social Posts + Banners", "Ad creative included."),
            ("star", "Demo Video Link", "Show instead of explain."),
        ],
        "how": [
            ("Create a licence", "One licence, one account."),
            ("Send it", "Customer gets a Basic account with 100 credits."),
            ("Track it", "Every licence and its state in one place."),
            ("Revoke if needed", "Licence returns to your pool."),
        ],
        "deep": [
            ("What your customer gets", "A real Basic account — full series engine, Series Bible, continuity, covers, metadata, KDP exports — with 100 credits and no upgrade path.", ["Short and Standard lengths", "3 active series, 5 books per series", "100 one-time credits", "No OTO upgrades"]),
            ("Lite vs full Reseller", "One difference: 50 licences instead of 100. The dashboard and the entire franchise kit are identical.", ["50 vs 100 licences", "Same dashboard", "Same sales page, emails, socials, banners", "Same 100% keep"]),
        ],
        "math_head": "What 50 licences can be worth",
        "math_lead": "Illustrative. You set the price.",
        "math": [
            ("50 licences at $27", "$1,350", "your revenue"),
            ("50 licences at $47", "$2,350", "your revenue"),
            ("50 licences at $97", "$4,850", "your revenue"),
            ("Your cost", "$67", "one time"),
        ],
        "compare_head": "Reseller Lite vs Full Reseller",
        "compare": [
            ("Licences", "50", "100"),
            ("Dashboard", "Included", "Included"),
            ("Franchise kit", "Included", "Included"),
            ("Keep 100%", "Yes", "Yes"),
            ("Price", "$67", "$97"),
        ],
        "uses_head": "Good fits for Reseller Lite",
        "uses": [
            ("Selling to a warm list", "Fifty is plenty for a first launch."),
            ("Bundling with a course", "Include a licence as a bonus."),
            ("Offline and local markets", "People who will never find the tool themselves."),
            ("Testing reseller demand", "Prove it works, then scale."),
        ],
        "whofor": ["You have an audience or a list.", "You sell courses or services.", "You want a product to resell without building one."],
        "notfor": ["You have no traffic and no plan for it.", "You need 100 licences immediately."],
        "elsewhere": [
            ("White-label SaaS reseller deal", "$1,000 - $5,000", "per year plus rev share"),
            ("Sales page copywriter", "$500 - $1,500", "per page"),
            ("Email sequence", "$300 - $800", "per sequence"),
            ("BookSaga Reseller Lite, today", "$67", "one time"),
        ],
        "stack": [
            ("50 Reseller Licences", "$1,497"),
            ("Reseller Dashboard", "$497"),
            ("Sales Page (HTML)", "$997"),
            ("Email Swipes + Social + Banners", "$794"),
            ("Demo Video Link", "$297"),
        ],
        "stack_total": "$4,082",
        "faq": [
            ("What does my customer get?", "A Basic account: short and standard, 3 active series, 5 books per series, 100 credits, no upgrades."),
            ("Do I keep the money?", "Yes, 100%. No revenue share."),
            ("Can I revoke?", "Yes, and the licence returns to your pool."),
            ("How is this different from Agency?", "Agency is you running client accounts. Reseller is selling licences so others own their accounts."),
            ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
        ],
        "ps": ["Fifty licences at 27 dollars is 1,350 dollars from a 67 dollar purchase."],
        "decision_lead": "Get 50 reseller licences and the complete franchise kit for a one-time $67.",
        "yes_label": "Yes, Give Me 50 Licences!",
        "yes_cap": "Yes, I want to sell BookSaga for $67",
        "no_label": "No Thanks, I'm Done",
        "no_cap": "Finish my order and take me to my account",
        "no_url": "index.html",
    },
]

for d in DS:
    d["kind"] = "ds"
    d["pill"] = "Wait — one-time decision · Your order is confirmed"
    d["video_note"] = "A short walkthrough of what is included"
PAGES.extend(DS)


# --------------------------------------------------------------------------- render helpers
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             if "&" in s or "<" in s else s)


def steps_html(current, kind):
    labels = ["FE"] + ["OTO %d" % i for i in range(1, 6)]
    out = []
    for i, lab in enumerate(labels, start=0):
        if i < current:
            cls = "bs-step is-done"
        elif i == current:
            cls = "bs-step is-now"
        else:
            cls = "bs-step"
        out.append('<span class="%s" data-step="%d"><i class="bs-step-dot"></i><span>%s</span></span>' % (cls, i, lab))
    return '<div class="bs-steps">%s</div>' % "".join(out)


def stops_html(page):
    rows = "".join(
        "<tr><td>%s</td><td>%s</td><td class=\"is-hi\">%s</td></tr>" % (a, b, c)
        for a, b, c in page["stops"]
    )
    return """
<section class="bs-sec bs-sec--alt" id="where-it-stops">
  <div class="bs-wrap">
    <div class="bs-center"><span class="bs-pill bs-pill--pink">Your current plan</span>
      <h2 class="bs-h2 bs-mt-16">%s</h2>
      <p class="bs-lead bs-narrow">%s</p>
    </div>
    <div class="bs-table-wrap">
      <table class="bs-table">
        <thead><tr><th>Feature</th><th>BookSaga Basic</th><th>%s</th></tr></thead>
        <tbody>%s</tbody>
      </table>
    </div>
  </div>
</section>""" % (page["stops_head"], page["stops_lead"], page["name"], rows)


def cards_html(items, cols=3, reveal=True):
    cls = "bs-grid bs-grid--%d" % cols
    rv = ' data-reveal' if reveal else ''
    out = []
    for icon, title, text in items:
        out.append('<article class="bs-card"%s>%s<h3>%s</h3><p>%s</p></article>' % (rv, ico(icon), title, text))
    return '<div class="%s">%s</div>' % (cls, "".join(out))


def how_html(steps):
    out = []
    for i, (title, text) in enumerate(steps, start=1):
        out.append("""
      <article class="bs-card" data-reveal>
        <span class="bs-card-ico" style="background:linear-gradient(135deg,#ffd400,#ff7a1a)"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v20M2 12h20" stroke="none"/><text x="12" y="17" text-anchor="middle" font-size="13" font-family="Bricolage Grotesque,sans-serif" font-weight="800" fill="#14082e">%d</text></svg></span>
        <h3>%s</h3><p>%s</p>
      </article>""" % (i, title, text))
    return '<div class="bs-grid bs-grid--4">%s</div>' % "".join(out)


def deep_html(deep):
    out = []
    for title, text, bullets in deep:
        lis = "".join("<li>%s</li>" % b for b in bullets)
        out.append("""
      <article class="bs-card" data-reveal>
        <h3>%s</h3><p>%s</p>
        <ul class="bs-check-list">%s</ul>
      </article>""" % (title, text, lis))
    return '<div class="bs-grid bs-grid--%d">%s</div>' % (min(len(deep), 3), "".join(out))


def math_html(page):
    rows = "".join("<tr><td>%s</td><td>%s</td><td class=\"is-hi\">%s</td></tr>" % (a, b, c) for a, b, c in page["math"])
    return """
<section class="bs-sec" id="numbers">
  <div class="bs-wrap">
    <div class="bs-center"><span class="bs-pill bs-pill--green">The numbers</span>
      <h2 class="bs-h2 bs-mt-16">%s</h2>
      <p class="bs-lead bs-narrow">%s</p>
    </div>
    <div class="bs-table-wrap">
      <table class="bs-table"><thead><tr><th>Scenario</th><th>Maths</th><th>Per reader / value</th></tr></thead><tbody>%s</tbody></table>
    </div>
    <p class="bs-note"><strong>Illustrative only.</strong> These are royalty and pricing examples, not income promises. Actual results depend on your genre, your listings and the market.</p>
  </div>
</section>""" % (page["math_head"], page["math_lead"], rows)


def compare_html(page):
    rows = "".join("<tr><td>%s</td><td class=\"is-no\">%s</td><td class=\"is-yes\">%s</td></tr>" % (a, b, c) for a, b, c in page["compare"])
    return """
<section class="bs-sec bs-sec--alt" id="compare">
  <div class="bs-wrap">
    <div class="bs-center"><h2 class="bs-h2">%s</h2></div>
    <div class="bs-table-wrap">
      <table class="bs-table"><thead><tr><th>What changes</th><th>Without</th><th>With %s</th></tr></thead><tbody>%s</tbody></table>
    </div>
  </div>
</section>""" % (page["compare_head"], page["name"], rows)


def uses_html(page):
    return """
<section class="bs-sec" id="ways-to-use">
  <div class="bs-wrap">
    <div class="bs-center"><span class="bs-eyebrow">In practice</span><h2 class="bs-h2">%s</h2></div>
    %s
  </div>
</section>""" % (page["uses_head"], cards_html([("star", a, b) for a, b in page["uses"]], cols=3))


def whofor_html(page):
    yes = "".join("<li>%s</li>" % x for x in page["whofor"])
    no = "".join("<li>%s</li>" % x for x in page["notfor"])
    return """
<section class="bs-sec bs-sec--alt" id="who-for">
  <div class="bs-wrap">
    <div class="bs-center"><h2 class="bs-h2">Who this is for</h2><p class="bs-sub">And who should honestly skip it.</p></div>
    <div class="bs-grid bs-grid--2">
      <article class="bs-card" data-reveal>
        <h3 style="color:#7ee2a1">This is for you if…</h3>
        <ul class="bs-check-list">%s</ul>
      </article>
      <article class="bs-card" data-reveal>
        <h3 style="color:#ff8f92">Skip it if…</h3>
        <ul class="bs-check-list">%s</ul>
      </article>
    </div>
  </div>
</section>""" % (yes, no)


def elsewhere_html(page):
    rows = "".join("<tr><td>%s</td><td>%s</td><td class=\"is-hi\">%s</td></tr>" % (a, b, c) for a, b, c in page["elsewhere"])
    return """
<section class="bs-sec" id="cost-elsewhere">
  <div class="bs-wrap">
    <div class="bs-center"><span class="bs-pill">What this costs any other way</span>
      <h2 class="bs-h2 bs-mt-16">Priced against the alternatives</h2>
      <p class="bs-lead bs-narrow">Not against a competitor's feature list — against what the same outcome costs if you pay someone else to produce it.</p>
    </div>
    <div class="bs-table-wrap">
      <table class="bs-table"><thead><tr><th>Option</th><th>Typical cost</th><th>Note</th></tr></thead><tbody>%s</tbody></table>
    </div>
  </div>
</section>""" % rows


def stack_html(page):
    rows = "".join('<div class="bs-stack-row"><span>%s</span><span>%s</span></div>' % (a, b) for a, b in page["stack"])
    return """
<section class="bs-sec bs-sec--alt" id="value-stack">
  <div class="bs-wrap">
    <div class="bs-center"><span class="bs-eyebrow">Value stack</span>
      <h2 class="bs-h2">Everything included in %s</h2>
      <p class="bs-sub">Valued at what each piece would cost separately — not a guaranteed worth.</p>
    </div>
    <div class="bs-stack">
      %s
      <div class="bs-stack-total"><span>Total value</span><span>%s</span></div>
      <div class="bs-stack-total" style="background:rgba(255,212,0,.06)"><span>Your price today</span><span>%s</span></div>
    </div>
  </div>
</section>""" % (page["name"], rows, page["stack_total"], page["price"])


def price_html(page):
    return """
<section class="bs-sec" id="price">
  <div class="bs-wrap bs-center">
    <span class="bs-pill bs-pill--green">One-time payment</span>
    <h2 class="bs-h2 bs-mt-16">%s — today only</h2>
    <div class="bs-price-card">
      <p class="bs-price-old">Regular price %s</p>
      <p class="bs-price-now"><small>$</small>%s</p>
      <p class="bs-price-once">One-time · Lifetime access · No monthly fee</p>
      <div class="bs-cta">
        <a class="bs-btn" data-buy href="#">
          <span class="bs-btn-main">%s</span>
          <span class="bs-btn-sub">Instant access · Secure checkout</span>
        </a>
        <p class="bs-cta-note">30-day money-back guarantee · Support: softwarevh@gmail.com</p>
      </div>
    </div>
  </div>
</section>""" % (page["name"], page["regular"], page["price_num"], page["yes_label"])


def faq_html(page):
    items = "".join("<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in page["faq"])
    return """
<section class="bs-sec bs-sec--alt" id="faq">
  <div class="bs-wrap bs-narrow">
    <div class="bs-center"><h2 class="bs-h2">Questions people actually ask</h2></div>
    <div class="bs-faq">%s</div>
  </div>
</section>""" % items


def ps_html(page):
    items = "".join("<p>%s</p>" % p for p in page["ps"])
    return """
<section class="bs-sec bs-sec--tight">
  <div class="bs-wrap bs-narrow">
    <div class="bs-ps">%s</div>
  </div>
</section>""" % items


def decision_html(page):
    return """
<section class="bs-decision" id="decision">
  <div class="bs-wrap bs-center">
    <span class="bs-pill">Your One-Time Decision</span>
    <h2 class="bs-h1">Ready To Unlock The <span class="bs-hl">%s</span>?</h2>
    <p class="bs-lead bs-narrow">%s</p>
    <div class="bs-decision-grid">
      <div class="bs-choice bs-choice--yes">
        <a class="bs-choice-btn" data-buy href="#">%s</a>
        <span class="bs-choice-cap">%s</span>
      </div>
      <div class="bs-choice bs-choice--no">
        <a class="bs-choice-btn" data-no href="%s">%s</a>
        <span class="bs-choice-cap bs-choice-cap--muted">%s</span>
      </div>
    </div>
    <p class="bs-cta-note bs-mt-24">Both buttons are safe. The guarantee is 30 days either way — one email to softwarevh@gmail.com.</p>
  </div>
</section>""" % (page["name"], page["decision_lead"], page["yes_label"], page["yes_cap"], page["no_url"], page["no_label"], page["no_cap"])


def footer_html(page):
    return """
<footer class="bs-footer">
  <div class="bs-wrap">
    <div class="bs-footer-links">
      <a href="index.html">BookSaga home</a>
      <a href="jv.html">JV &amp; affiliate page</a>
      <a href="mailto:softwarevh@gmail.com">Support</a>
    </div>
    <p><strong>Earnings disclaimer:</strong> royalty and revenue figures on this page are illustrations, not promises. BookSaga does not guarantee sales, income or results of any kind.</p>
    <p><strong>Trademark notice:</strong> Amazon, Kindle, Kindle Unlimited, KDP and Audible are trademarks of Amazon.com, Inc. or its affiliates. BookSaga is not affiliated with, endorsed by or sponsored by Amazon.</p>
    <p><strong>AI disclosure:</strong> BookSaga generates content with AI. Disclosing AI-generated content on KDP is your responsibility as the publisher.</p>
    <p>30-day money-back guarantee on every offer. Refunds: one email to <a href="mailto:softwarevh@gmail.com">softwarevh@gmail.com</a>.</p>
  </div>
</footer>"""


PAGE_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}}</title>
<meta name="description" content="{{desc}}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0b1033">
<link rel="icon" href="images/booksaga-logo.png">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Inter+Tight:ital,wght@0,400;0,500;0,600;0,700;0,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/oto.css">

<!-- ==========================================================================
     CHECKOUT CONFIG — this is the only place a link needs to be set.
     buy : paste this offer's Launchpad checkout URL
     no  : where the "no thanks" button goes (already wired into the funnel)
     ========================================================================== -->
<script>
window.BS_CFG = {
  buy: "",
  no: "{{no_url}}",
  step: {{num}}
};
</script>
</head>

<body class="bs-oto">

<!-- ===================================================== 1 · TOP BAR + PROGRESS -->
<div class="bs-topbar">
  <div class="bs-topbar-in">
    <a class="bs-brand" href="index.html">
      <img src="images/booksaga-logo.png" alt="BookSaga">
      <span>BookSaga</span>
    </a>
    {{steps}}
    <span class="bs-secure">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 11V7a5 5 0 0 1 10 0v4"/><path d="M5 11h14v10a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2z"/></svg>
      <span>Secure checkout</span>
    </span>
  </div>
</div>

<!-- ===================================================== 2 · CONGRATULATIONS -->
<section class="bs-sec bs-sec--tight">
  <div class="bs-wrap bs-center">
    <span class="bs-pill bs-pill--green">Order confirmed</span>
    <p class="bs-sub bs-mt-16">{{pill}}</p>
  </div>
</section>

<!-- ===================================================== 3 · HEADLINE / HERO -->
<section class="bs-sec bs-sec--tight" style="padding-top:0">
  <div class="bs-wrap bs-center">
    <h1 class="bs-h1">{{h1_pre}} <span class="bs-hl">{{h1_hl}}</span></h1>
    <p class="bs-lead bs-narrow">{{lead}}</p>
    <div class="bs-cta">
      <a class="bs-btn" data-buy href="#">
        <span class="bs-btn-main">{{yes_label}}</span>
        <span class="bs-btn-sub">One-time {{price}} · Instant access</span>
      </a>
      <p class="bs-cta-note" id="bs-checkout-notice" hidden><strong>Checkout link not configured yet.</strong> Set <code>window.BS_CFG.buy</code> in this page's &lt;head&gt;.</p>
      <div class="bs-trust">
        <span><svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>One-time payment</span>
        <span><svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>No monthly fee</span>
        <span><svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>30-day guarantee</span>
      </div>
    </div>
  </div>
</section>

<!-- ===================================================== 4 · VIDEO -->
<section class="bs-sec bs-sec--tight" style="padding-top:0">
  <div class="bs-wrap">
    <div class="bs-video">
      <div class="bs-video-in">
        <span class="bs-play"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span>
        <p>{{video_note}}</p>
      </div>
    </div>
  </div>
</section>

<!-- ===================================================== 5 · CTA #1 -->
<section class="bs-sec bs-sec--tight">
  <div class="bs-wrap bs-center">
    <a class="bs-btn" data-buy href="#">
      <span class="bs-btn-main">Yes — Add {{name}} For {{price}}</span>
      <span class="bs-btn-sub">Instant access · Secure checkout</span>
    </a>
    <p class="bs-cta-note bs-mt-16">30-day money-back guarantee · Support: softwarevh@gmail.com</p>
  </div>
</section>

<!-- ===================================================== 6 · WHERE YOUR PLAN STOPS -->
{{stops}}

<!-- ===================================================== 7 · THE PROBLEM -->
<section class="bs-sec" id="problem">
  <div class="bs-wrap">
    <div class="bs-center">
      <span class="bs-eyebrow">The problem</span>
      <h2 class="bs-h2">Why this matters right now</h2>
    </div>
    {{problems}}
  </div>
</section>

<!-- ===================================================== 8 · INTRODUCING -->
<section class="bs-sec bs-sec--alt" id="introducing">
  <div class="bs-wrap bs-narrow bs-center">
    <span class="bs-pill bs-pill--pink">Introducing</span>
    <h2 class="bs-h1 bs-mt-16">{{intro_head}}</h2>
    <p class="bs-lead">{{intro_lead}}</p>
    <p class="bs-sub">{{intro_body}}</p>
  </div>
  <div class="bs-wrap">
    <div class="bs-media"><img src="{{hero_img}}" alt="{{hero_alt}}" loading="lazy" decoding="async"></div>
  </div>
</section>

<!-- ===================================================== 9 · EVERYTHING IT UNLOCKS -->
<section class="bs-sec" id="unlocks">
  <div class="bs-wrap">
    <div class="bs-center">
      <span class="bs-eyebrow">Everything it unlocks</span>
      <h2 class="bs-h2">What you get with {{name}}</h2>
    </div>
    {{unlocks}}
  </div>
</section>

<!-- ===================================================== 10 · HOW IT WORKS -->
<section class="bs-sec bs-sec--alt" id="how-it-works">
  <div class="bs-wrap">
    <div class="bs-center"><h2 class="bs-h2">How it works</h2><p class="bs-sub">Four steps. Nothing to install, nothing to migrate.</p></div>
    {{how}}
  </div>
</section>

<!-- ===================================================== 11 · DEEP DIVES -->
<section class="bs-sec" id="deep-dive">
  <div class="bs-wrap">
    <div class="bs-center"><span class="bs-eyebrow">The detail</span><h2 class="bs-h2">The parts that actually matter</h2></div>
    {{deep}}
  </div>
</section>

<!-- ===================================================== 12 · NUMBERS -->
{{math}}

<!-- ===================================================== 13 · WITHOUT VS WITH -->
{{compare}}

<!-- ===================================================== 14 · WAYS TO USE -->
{{uses}}

<!-- ===================================================== 15 · WHO IT'S FOR -->
{{whofor}}

<!-- ===================================================== 16 · COST ELSEWHERE -->
{{elsewhere}}

<!-- ===================================================== 17 · VALUE STACK -->
{{stack}}

<!-- ===================================================== 18 · PRICE + CTA -->
{{price_section}}

<!-- ===================================================== 19 · GUARANTEE -->
<section class="bs-sec bs-sec--alt" id="guarantee">
  <div class="bs-wrap bs-narrow bs-center">
    <span class="bs-pill bs-pill--green">Zero risk</span>
    <h2 class="bs-h2 bs-mt-16">30 days to change your mind</h2>
    <p class="bs-lead">Use it. Publish with it. If it is not what this page says it is, send one email to <strong>softwarevh@gmail.com</strong> within 30 days and you get your money back. No forms, no hoops, no interrogation.</p>
    <div class="bs-trust bs-mt-24">
      <span><svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>One email</span>
      <span><svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>30 calendar days</span>
      <span><svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></svg>Every offer, same terms</span>
    </div>
  </div>
</section>

<!-- ===================================================== 20 · LAUNCH PRICING -->
<section class="bs-sec bs-sec--tight" id="launch-pricing">
  <div class="bs-wrap bs-narrow bs-center">
    <h2 class="bs-h3">Why the price is lower right now</h2>
    <p class="bs-sub">{{price}} is the launch price for this offer. The regular price shown on the price card is where it goes afterwards. We are not claiming this disappears forever — it stays available from inside the app at the regular price. The discount is real; the scarcity is about the discount, not the product.</p>
  </div>
</section>

<!-- ===================================================== 21 · FAQ -->
{{faq}}

<!-- ===================================================== 22 · P.S. -->
{{ps}}

<!-- ===================================================== 23 · DECISION (LAST) -->
{{decision}}

{{footer}}

<script src="js/oto.js"></script>
</body>
</html>
"""


def build(page):
    ctx = dict(page)
    ctx["steps"] = steps_html(page["num"], page["kind"])
    ctx["problems"] = cards_html(page["problems"], cols=4)
    ctx["unlocks"] = cards_html(page["unlocks"], cols=4)
    ctx["how"] = how_html(page["how"])
    ctx["deep"] = deep_html(page["deep"])
    ctx["math"] = math_html(page)
    ctx["compare"] = compare_html(page)
    ctx["uses"] = uses_html(page)
    ctx["whofor"] = whofor_html(page)
    ctx["elsewhere"] = elsewhere_html(page)
    ctx["stack"] = stack_html(page)
    ctx["price_section"] = price_html(page)
    ctx["faq"] = faq_html(page)
    ctx["ps"] = ps_html(page)
    ctx["decision"] = decision_html(page)
    ctx["stops"] = stops_html(page)
    ctx["footer"] = footer_html(page)

    html = PAGE_TMPL
    for k, v in ctx.items():
        html = html.replace("{{%s}}" % k, v if isinstance(v, str) else str(v))

    left = html.count("{{")
    if left:
        raise SystemExit("Unreplaced placeholders in %s: %d" % (page["slug"], left))

    out = os.path.join(OUT_DIR, page["slug"])
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return out, html.count("<section")


if __name__ == "__main__":
    total = 0
    for p in PAGES:
        path, sections = build(p)
        total += 1
        print("%-12s sections=%2d  %s" % (p["slug"], sections, path))
    print("\n%d pages generated." % total)
