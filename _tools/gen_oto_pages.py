#!/usr/bin/env python3
"""
BookSaga · OTO page generator (5 offers, no downsells, no video).

Source of truth for every claim: PRODUCT_OFFER_BONUS_GUIDE.md
(funnel §4, per-offer detail §5, value stacks §7.1, guarantee §8).

Output (repo root, same asset paths as index.html):
    oto1.html .. oto5.html

Rules baked into this generator:
  * No downsell pages. "No thanks" on an OTO goes straight to the next OTO;
    the last one goes back to the members area.
  * No video blocks anywhere.
  * The internal accounting unit is never named. Capacity is expressed as
    what it produces (novels, audiobooks, client series) instead.

Checkout URLs are not hardcoded in the markup. Each page carries one
window.BS_CFG block in <head>; paste the Launchpad checkout URL there.
"""

import os
import re

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
    "num": 1,
    "title": "BookSaga Unlimited — Full-Length Novels, 30 Books Per Series, Box Sets",
    "desc": "Unlock the Full-Length engine, 30 books per series, unlimited active series, print-ready paperback wraps and the Box Set Builder.",
    "name": "Unlimited",
    "hl": "Unlimited",
    "price": "$47",
    "price_num": "47",
    "regular": "$297",
    "pill": "Step 2 of 6 · Your order is confirmed",
    "h1_pre": "Your BookSaga Plan Stops At",
    "h1_hl": "Book 5.",
    "lead": "BookSaga Basic writes up to 5 books per series in Short and Standard. Unlimited removes that ceiling: full-length novels, up to 30 books per series, unlimited active series, print-ready paperback wraps, Box Sets — and enough room to produce 81 more full-length novels, covers included.",
    "hero_img": "images/booksaga-product-mockup.png",
    "hero_alt": "BookSaga series workspace showing a multi-book series",
    "stops_head": "Where your current plan stops",
    "stops_lead": "Basic is a real product — it is just deliberately capped. These are the exact walls you are standing in front of right now.",
    "stops": [
        ("Books per series", "5", "30"),
        ("Active series at once", "3", "Unlimited"),
        ("Length preset", "Short + Standard", "+ Full-Length"),
        ("Paperback full-wrap cover", "Not included", "Included"),
        ("Box Set Builder", "Not included", "Included"),
        ("Novels you can produce, covers included", "About 13 standard", "About 81 full-length"),
    ],
    "problems": [
        ("clock", "Book 5 is a cliff, not a finish line.", "A five-book series ends exactly where read-through starts compounding. Readers who wanted more have nowhere to go — so they go to another author."),
        ("book", "Short and Standard cap your price point.", "At ~12,000 and ~30,000 words you are competing in the crowded cheap end. Full-length novels (~55,000 words) support the $4.99-$6.99 price you actually want."),
        ("grid", "No wrap means no paperback.", "Amazon's paperback is where the physical-looking product lives. Without a print-ready spine, you cannot ship the version readers photograph and share."),
        ("layers", "Three series is not a catalogue.", "Three active series is a test. A catalogue is twenty series, each with a box set and a paperback, all feeding each other."),
    ],
    "intro_head": "Introducing BookSaga Unlimited",
    "intro_lead": "Same app you already own. The ceilings come off.",
    "intro_body": "Unlimited is not a new tool you have to learn. It is the same workspace you just bought, with the limits you hit in week one removed: a Full-Length engine, 30 books per series, unlimited active series, print-ready paperback wraps, Box Set Builder, and room for 81 more full-length novels on top of what Basic already gives you.",
    "unlocks": [
        ("book", "Full-Length Novels", "25-30 chapters, ~55,000 words per book. The length that supports premium pricing and real KU page reads."),
        ("layers", "30 Books Per Series", "Six times the runway. Arc-level planning that actually pays off across a long series instead of resetting every five books."),
        ("grid", "Unlimited Active Series", "Run as many series in parallel as your catalogue needs — across as many pen names as you like."),
        ("image", "Paperback Full-Wrap Cover PDF", "Front, spine and back at 300 DPI, built to KDP print specs. Spine width calculated for you."),
        ("star", "Box Set Builder", "Combine 2+ books into one higher-priced listing with a combined TOC, dividers and its own cover."),
        ("bolt", "Room For 81 More Full-Length Novels", "Covers included. It is added to what Basic gives you rather than replacing it — one time, no renewals, no monthly fee."),
        ("wand", "Add More Parts", "Extend a series past its planned count, up to the 30-book system cap, whenever you want."),
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
        ("A real catalogue, not a test", "Unlimited active series is what turns three experiments into a catalogue: different genres, different pen names, all cross-promoting. Ten full-length books is roughly 2,900 KENP pages of surface area against roughly 325 for a five-book short series.", ["Per user: 10 book generations per day", "1 book job + 3 cover jobs at a time", "One-time purchase — nothing renews"]),
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
        ("Novels you can produce", "About 13 standard", "About 81 full-length"),
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
        ("Room For 81 More Full-Length Novels (covers included)", "$1,497"),
    ],
    "stack_total": "$5,082",
    "faq": [
        ("Is 'Unlimited' really unlimited books?", "No — and we will not pretend otherwise. Unlimited means unlimited <em>active series</em>. Books per series has a hard system cap of 30 on every plan. There is also a daily cap of 10 book generations per user."),
        ("Does what I already have get replaced?", "No. It is added on top. Everything Basic gives you stays exactly as it is, and room for 81 more full-length novels sits beside it — one time, no renewals, no monthly fee."),
        ("Do I have to rewrite my existing series?", "No. Your series, bible, chapters and covers stay exactly where they are. Full-Length and the higher caps simply become available on them."),
        ("What exactly is a full-wrap cover PDF?", "A single print-ready file containing back cover, spine and front cover at 300 DPI, with spine width calculated from page count and paper stock. It is what KDP wants for a paperback."),
        ("Does this replace my Basic plan?", "It adds to it. Basic stays as your baseline; Unlimited removes its limits and adds a much larger production runway on top."),
        ("What if I do not like it?", "30 days, one email to softwarevh@gmail.com. No forms, no hoops. Every offer carries the same guarantee."),
    ],
    "ps": [
        "You have already paid for the hard part — the engine, the Series Bible, the continuity checks. The only thing standing between you and a 30-book full-length catalogue is a 47 dollar ceiling.",
        "The extra runway alone is roughly 81 full-length novels with covers. That is more finished writing than most publishers complete in a year.",
    ],
    "decision_lead": "Add the Full-Length engine, 30-book series, print wraps, Box Sets and room for 81 more full-length novels for a one-time $47.",
    "yes_label": "Yes, Unlock Unlimited!",
    "yes_cap": "Yes, I want full-length novels, 30-book series and box sets",
    "no_label": "No Thanks, Show Me The Next Step",
    "no_cap": "I'll keep my series capped at five",
    "no_url": "oto2.html",
})

# ============================================================== OTO 2 · Done-For-You
PAGES.append({
    "slug": "oto2.html",
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
    "lead": "A five-book Standard series with covers uses more than a third of everything Basic can produce. Burn that on an idea that does not sell and it is simply gone. Done-For-You hands you 120 tested series concepts, 500 more ideas, blurbs and keyword packs, all one click away.",
    "hero_img": "images/amazonseries_b050ec.png",
    "hero_alt": "Amazon series page showing a completed multi-book series",
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
        ("image", "A Sample Cover For Every Template", "See the visual promise before you commit to a whole series."),
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
        ("The maths, so the risk is visible", "A five-book Standard series with covers takes more than a third of what Basic can produce. A tested template does not guarantee sales — but it removes the most avoidable reason a series fails.", ["Five books plus five covers", "More than a third of Basic's output", "All of it riding on one unproven idea"]),
    ],
    "math_head": "What a wrong guess actually costs",
    "math_lead": "Illustrative. Assumes a five-book Standard series with matching covers.",
    "math": [
        ("Wrong niche, five books, covers", "A third of your output", "gone"),
        ("Right niche, five books, covers", "The same output", "same spend, better odds"),
        ("What Basic can produce", "About 2 full series", "or 27 single books"),
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
        ("Build a niche shortlist", "Read 20 templates in a category before committing to a series anywhere."),
    ],
    "whofor": [
        "You are about to start a five-book series and want the idea de-risked first.",
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
        ("Does using a template use anything up?", "No. Templates are free to browse and prefill. Nothing is consumed until you actually generate books and covers."),
        ("What is the difference between Lite and full?", "Lite gives you 40 templates and a reduced ideas/blurb/keyword selection. Full gives you all 120 plus the complete library."),
        ("Guarantee?", "30 days, one email to softwarevh@gmail.com. Same on every offer."),
    ],
    "ps": [
        "You do not need more ideas. You need fewer bad ones. 120 tested shapes cost less than a single wrong five-book series.",
        "The output you would burn guessing is worth more than this entire offer.",
    ],
    "decision_lead": "Add 120 tested series templates, 500+ ideas, blurb templates and keyword packs to your BookSaga account for a one-time $37.",
    "yes_label": "Yes, Give Me The 120 Templates!",
    "yes_cap": "Yes, I want tested templates, blurbs and keyword packs",
    "no_label": "No Thanks, Show Me The Next Step",
    "no_cap": "I'll guess the niche myself",
    "no_url": "oto3.html",
})

# ============================================================== OTO 3 · Audiobook
PAGES.append({
    "slug": "oto3.html",
    "num": 3,
    "title": "BookSaga Audiobook — Turn Every Finished Book Into Audio",
    "desc": "Narrate any finished BookSaga book: curated AI voices, per-chapter MP3 at ACX specs, square cover, in-app player and ZIP download.",
    "name": "Audiobook",
    "hl": "Audiobook",
    "price": "$47",
    "price_num": "47",
    "regular": "$297",
    "pill": "Step 4 of 6 · Your order is confirmed",
    "h1_pre": "You Wrote The Book. Now It Can",
    "h1_hl": "Talk.",
    "lead": "Audiobook turns any finished BookSaga book into per-chapter MP3s, mastered to ACX technical specs, with a square cover and an in-app player. Narration runs on its own separate budget, so making audiobooks never takes a single novel away from your writing queue.",
    "hero_img": "images/inside1_949c81.png",
    "hero_alt": "Chapter opening page from a BookSaga series",
    "stops_head": "Where your current plan stops",
    "stops_lead": "Basic produces ebooks and print files. Audio is a different product entirely — and a different buyer.",
    "stops": [
        ("Audiobook module", "Not included", "Included"),
        ("Curated AI voices", "0", "US + UK, male + female"),
        ("Per-chapter MP3", "Not included", "192 kbps CBR"),
        ("ACX-spec mastering", "Not included", "Included"),
        ("Square cover 2400×2400", "Not included", "Included"),
        ("Audiobooks you can produce", "0", "About 66"),
    ],
    "problems": [
        ("mic", "Professional narration is out of reach.", "A 55,000-word novel narrated by a pro runs into thousands of dollars and weeks of scheduling — before you know whether the book sells."),
        ("clock", "Audio listeners are a different market.", "Commuters, gym-goers and people who never open an ebook. Same manuscript, a whole audience you currently cannot reach."),
        ("download", "Formatting audio by hand is miserable.", "Chapter splits, loudness normalisation, peak limiting, room tone, opening and closing announcements. Every one of those is a step you can get wrong."),
        ("star", "One format is one price point.", "Ebook, paperback and audiobook are three listings and three revenue streams from the same written work."),
    ],
    "intro_head": "Introducing BookSaga Audiobook",
    "intro_lead": "Any finished book, narrated, mastered and exported.",
    "intro_body": "Pick a book, pick a voice, preview it, set the speed. BookSaga produces one MP3 per chapter at 192 kbps CBR, 44.1 kHz mono, mastered to ACX technical specifications, with opening and closing announcement files and a 2400×2400 square cover. Download the ZIP or listen in the app.",
    "unlocks": [
        ("mic", "Audiobook Series Module", "Narrate any finished book in any series. Runs as its own job queue, separate from writing."),
        ("users", "Curated Natural Voices", "US and UK English, male and female, each with a preview you can hear before generating anything."),
        ("clock", "Speed Control 0.8× - 1.2×", "Match the pacing to the genre. Cozy mystery and thriller do not read at the same tempo."),
        ("download", "One MP3 Per Chapter", "192 kbps CBR, 44.1 kHz, mono. Chapter boundaries already correct — no splitting by hand."),
        ("chart", "ACX-Spec Mastering", "RMS -23 to -18 dB, peak at or below -3 dB, noise floor at or below -60 dB, room tone, opening and closing announcements."),
        ("image", "2400×2400 Square Cover", "The square format the audio stores actually want, generated from your existing cover art."),
        ("bolt", "In-App Player + ZIP", "Listen before you ship, then download everything as one archive."),
        ("layers", "Narration For 66 Audiobooks", "A completely separate budget from your writing. Narrating never takes a novel away from your writing queue."),
    ],
    "how": [
        ("Pick a finished book", "Only completed books can be narrated — the manuscript has to exist first."),
        ("Choose and preview a voice", "Browse US and UK voices, male and female, and hear a sample before generating anything."),
        ("Set the speed", "0.8× to 1.2×. Preview again if you want to be sure."),
        ("Generate and export", "Per-chapter MP3s, mastered, with opening and closing announcements, square cover and a ZIP download."),
    ],
    "deep": [
        ("Where you can actually publish this", "This matters more than any feature list, so it is stated plainly: AI-narrated audio is not accepted by Audible through ACX today. BookSaga audio is not for ACX upload. It is for the stores and channels that do accept it.", ["Google Play Books — accepts AI-narrated audiobooks with disclosure", "Kobo — list the narrator as a synthetic voice", "Your own store — Payhip, Gumroad, Shopify, your site", "Reader magnet — a free audio prequel to grow your list", "Always re-check each store's current AI-narration policy before publishing"]),
        ("What 'mastered to ACX specs' means", "It means the technical envelope is already inside the range that professional audio platforms expect — so the files are not rejected on technical grounds, and they sound consistent from chapter one to chapter thirty.", ["RMS -23 to -18 dB", "True peak at or below -3 dB", "Noise floor at or below -60 dB", "Room tone between chapters", "Opening and closing announcement files"]),
        ("What 66 audiobooks is worth", "Narration has its own budget, so it never competes with your writing. Sixty-six finished audiobooks is a catalogue most indie authors never build in a decade of paying narrators.", ["66 finished audiobooks", "Your writing queue untouched", "One-time purchase, no renewals"]),
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
        ("Narration cost", "$2,000+ per novel", "Included for 66 books"),
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
        ("BookSaga Audiobook, today", "$47", "one time, 66 audiobooks"),
    ],
    "stack": [
        ("Audiobook Series Module", "$1,497"),
        ("Curated Natural Voices + Speed Control", "$497"),
        ("ACX-Spec Mastering", "$697"),
        ("Narration For 66 Audiobooks + Square Cover", "$997"),
        ("In-App Player + ZIP Download", "$197"),
        ("Opening & Closing Announcement Files", "$297"),
    ],
    "stack_total": "$4,182",
    "faq": [
        ("Can I upload this to Audible / ACX?", "No. ACX requires human narration, and AI-narrated audio is not accepted there today. This is stated plainly so nobody buys expecting otherwise. Use it for Google Play Books, Kobo, your own store and reader magnets instead."),
        ("Which stores do accept AI-narrated audio?", "Google Play Books accepts it with disclosure, Kobo accepts it when the narrator is listed as a synthetic voice, and your own store accepts whatever you sell. Store policies change — verify before each launch."),
        ("Does narrating take away from my writing?", "No. Narration has its own completely separate budget. Sixty-six audiobooks, and your writing queue is untouched."),
        ("What files do I get?", "One MP3 per chapter at 192 kbps CBR, 44.1 kHz mono, plus opening and closing announcement files, a 2400×2400 square cover, and a ZIP of everything."),
        ("Can I preview a voice first?", "Yes. Every voice has a preview sample, and you can re-preview at different speeds before generating."),
        ("What if the voice is not right?", "Re-generate with a different voice. Re-exports are always free."),
        ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
    ],
    "ps": [
        "Your book already exists. The only thing missing is the version that plays in someone's ears on the way to work.",
        "Sixty-six audiobooks for less than the cost of narrating a single novel professionally — and the store policy reality is written right there in the FAQ, not buried.",
    ],
    "decision_lead": "Add the audiobook studio, curated voices, ACX-spec mastering and narration for 66 audiobooks for a one-time $47.",
    "yes_label": "Yes, Turn My Books Into Audio!",
    "yes_cap": "Yes, I want 66 audiobooks and the full studio",
    "no_label": "No Thanks, Show Me The Next Step",
    "no_cap": "I'll skip the audio-only audience",
    "no_url": "oto4.html",
})

# ============================================================== OTO 4 · Agency
PAGES.append({
    "slug": "oto4.html",
    "num": 4,
    "title": "BookSaga Agency — 100 Client Accounts, Separate Client Budget",
    "desc": "Run BookSaga as a service. 100 client logins, a separate budget that only client work touches, per-client allotments, suspension controls and a client licence PDF.",
    "name": "Agency",
    "hl": "Agency",
    "price": "$67",
    "price_num": "67",
    "regular": "$497",
    "pill": "Step 5 of 6 · Your order is confirmed",
    "h1_pre": "Stop Being The Only Person",
    "h1_hl": "Using This.",
    "lead": "Agency gives you 100 client accounts, each with its own login, drawing from a separate budget that only client work touches. You set each client's allowance, you can suspend or reactivate them instantly, and your own writing is never touched.",
    "hero_img": "images/booksaga-teamwork.png",
    "hero_alt": "BookSaga team working across multiple client accounts",
    "stops_head": "Where your current plan stops",
    "stops_lead": "Right now every series in your workspace is yours. There is no way to hand work to a client, or to bill for it.",
    "stops": [
        ("Client accounts", "0", "100"),
        ("Separate budget for client work", "None", "≈ 45 complete series"),
        ("Per-client allotments", "Not included", "Included"),
        ("Copy login details", "Not included", "One click"),
        ("Suspend / activate clients", "Not included", "Included"),
        ("Client commercial licence PDF", "Not included", "Included"),
    ],
    "problems": [
        ("users", "Clients cannot log in.", "There is no way to give someone their own workspace. Every project means you sitting in the chair."),
        ("lock", "You cannot meter usage.", "Without allotments, one client could burn everything in a weekend and you would have no way to stop it."),
        ("copy", "Onboarding is manual.", "Writing out credentials, explaining the tool, chasing setup — per client, every time."),
        ("chart", "You are trading hours for money.", "The product is already built. The missing piece is a way to sell access to it repeatedly instead of doing the work yourself."),
    ],
    "intro_head": "Introducing BookSaga Agency",
    "intro_lead": "One workspace, one hundred client logins.",
    "intro_body": "Every client gets their own login and their own series. Their work draws from a separate budget that only client jobs touch — never from what you write with. You decide how much each client can use, and you can copy their login details in one click, suspend them, or look into their workspace read-only whenever you want.",
    "unlocks": [
        ("users", "100 Client Accounts", "Each with an independent login and their own series list. No shared passwords, no shared workspace."),
        ("layers", "A Separate Budget For Client Work", "Enough for roughly 45 complete five-book client series. Client work never touches what you write with."),
        ("target", "Per-Client Allotments", "Default 100 each, changeable at any time. You decide who can spend what."),
        ("copy", "Copy Login Details", "One click copies email, password and login URL — ready to paste into your onboarding email."),
        ("lock", "Suspend / Activate", "Cut off a non-paying or over-spending client instantly, and restore them just as fast."),
        ("shield", "Read-Only Client View", "Look into any client's series without being able to change their work."),
        ("book", "Client Commercial Licence PDF", "A ready-made licence document you can hand over so the commercial rights are explicit."),
        ("star", "Clients Inherit Your Plan", "If you own Unlimited, your clients get full-length and 30-book series too. Your plan is the ceiling."),
    ],
    "how": [
        ("Create a client account", "Name, email, and an initial allowance. Login details are generated for you."),
        ("Copy and send the login", "One click puts email, password and URL on your clipboard."),
        ("Set the allowance", "Default 100. Raise it for good clients, lower it for risky ones, change it whenever."),
        ("Monitor from the Clients page", "Budget remaining, and every client's allowance, used and remaining, in one table."),
    ],
    "deep": [
        ("The economics of one client", "A complete five-book Standard series with covers is more than a third of what a Basic buyer can produce. Your client budget covers roughly 45 of them — billable work you never write yourself.", ["≈ 45 complete five-book series", "≈ 227 standard books with covers", "All of it separate from your own writing"]),
        ("What happens when the budget runs out", "It fails safely and in your favour. The client sees a clear contact-your-agency message — not a broken tool, and not a surprise bill for you.", ["Client sees a clear contact-your-agency message", "Your own writing is never a fallback", "You top up the allowance when you choose"]),
        ("Clients inherit your plan, not a new one", "This is the detail most people miss. Your clients do not get a separate Basic plan — they work inside your entitlement. Own Unlimited and a client can produce full-length 30-book series.", ["Full-length if you own Unlimited", "30 books per series if you own Unlimited", "Their own allowance regardless"]),
    ],
    "math_head": "What 100 client accounts are worth",
    "math_lead": "Illustrative. Your pricing is your call — these are typical service rates in the niche.",
    "math": [
        ("One 5-book series, done for a client", "$500 - $2,500", "per project"),
        ("Monthly retainer, one client", "$200 - $800", "per month"),
        ("10 clients on retainer", "$2,000 - $8,000", "per month"),
        ("Your client budget covers", "≈ 45 series", "before you top up"),
        ("BookSaga Agency, today", "$67", "one time"),
    ],
    "compare_head": "Without Agency vs With Agency",
    "compare": [
        ("Client logins you can create", "0", "100"),
        ("What clients can use", "Your own output", "A separate budget"),
        ("Spend control", "None", "Per-client allotments"),
        ("Cut off a client", "Not possible", "Suspend instantly"),
        ("Oversight", "None", "Read-only view"),
        ("Commercial rights document", "You write it", "Licence PDF included"),
    ],
    "uses_head": "Five ways to run it as a business",
    "uses": [
        ("Done-for-you series service", "Charge per five-book series and hand over the KDP files."),
        ("Monthly publishing retainer", "Clients get a set number of books per month from their allowance."),
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
        ("A Separate Budget For Client Work (≈45 series)", "$1,997"),
        ("Per-Client Allotment Controls", "$497"),
        ("Suspend / Activate + Read-Only Oversight", "$297"),
        ("Client Commercial Licence PDF", "$497"),
        ("One-Click Copy Login", "$197"),
    ],
    "stack_total": "$5,482",
    "faq": [
        ("Do clients need their own BookSaga subscription?", "No. Their login works inside your agency plan. They never buy anything."),
        ("Do client jobs eat into my own writing?", "No. Client work draws from a completely separate budget. Your own writing is structurally protected."),
        ("What features do clients get?", "Whatever your own plan gives you. If you own Unlimited, your clients can produce full-length books and 30-book series. If you own Basic, they get Basic limits."),
        ("What if a client uses up their allowance?", "They see a clear contact-your-agency message. You raise their allowance whenever you decide."),
        ("Can I revoke a client's access?", "Yes — suspend them instantly. Their work stays intact and you can reactivate them later."),
        ("Is there a client licence document?", "Yes, a commercial licence PDF is included so the rights between you and your client are written down."),
        ("Guarantee?", "30 days, one email to softwarevh@gmail.com."),
    ],
    "ps": [
        "You already own a machine that writes series. Agency is the part that lets other people pay to use it.",
        "One client on a 200 dollar retainer pays for this three times over in the first month.",
    ],
    "decision_lead": "Add 100 client accounts, a separate budget for client work and full agency controls for a one-time $67.",
    "yes_label": "Yes, I Want To Sell This As A Service!",
    "yes_cap": "Yes, I want 100 clients and a separate client budget",
    "no_label": "No Thanks, Show Me The Next Step",
    "no_cap": "I only want to publish my own books",
    "no_url": "oto5.html",
})

# ============================================================== OTO 5 · Reseller
PAGES.append({
    "slug": "oto5.html",
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
        ("Send it to your customer", "They get a working BookSaga Basic account of their own."),
        ("Track it", "The dashboard shows every licence, who holds it and its current state."),
        ("Revoke if needed", "Refund or abuse — revoke it, and the licence returns to your pool."),
    ],
    "deep": [
        ("What your customer actually gets", "Be clear about this before you sell, because it is not the same as a direct Basic purchase. It is a real Basic account — full series engine, Series Bible, continuity, covers, metadata, KDP exports — but with a smaller starter allowance and no upgrade path.", ["Short and Standard lengths", "3 active series, 5 books per series", "A smaller starter allowance than a direct buyer gets", "No OTO upgrades available from that account"]),
        ("The economics, honestly", "This is the one offer where the maths deserves scrutiny rather than hype. Worst case: 100 customers each use their full starter allowance on short books. That is roughly 98 dollars of AI cost against 97 dollars of revenue — deliberately thin at the extreme.", ["100 customers, each using their full allowance", "Roughly a thousand short books of AI work", "≈ $98 worst-case AI cost", "Typical usage is far lower — but monitor it after launch"]),
        ("Selling without being a marketer", "The kit exists because most people who own a good product are not copywriters. Everything you need to make the first offer is included — you are choosing the channel and the price, not writing the assets.", ["Host the HTML sales page anywhere", "Send the email swipes to your list", "Post the social copy and banners", "Link the demo video"]),
    ],
    "math_head": "What 100 licences can be worth",
    "math_lead": "Illustrative. You set the price — these are common reseller price points.",
    "math": [
        ("100 licences at $27", "$2,700", "your revenue"),
        ("100 licences at $47", "$4,700", "your revenue"),
        ("100 licences at $97", "$9,700", "your revenue"),
        ("Your cost for the licences", "$97", "one time"),
        ("Worst-case AI cost to you", "≈ $98", "if every customer maxes out"),
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
        "You want your customers to get everything a direct buyer gets — that is a direct sale, not a licence.",
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
        ("What exactly does my customer get?", "A working BookSaga Basic account: full series engine, Series Bible, continuity, covers, metadata and KDP exports. Short and Standard lengths, 3 active series, 5 books per series, and a smaller starter allowance than a direct buyer. No OTO upgrades from that account."),
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
    "no_label": "No Thanks, I'm Done",
    "no_cap": "Finish my order and take me to my account",
    "no_url": "index.html",
})


# --------------------------------------------------------------------------- render helpers
def stops_html(page):
    rows = "".join(
        '<tr><td>%s</td><td>%s</td><td class="is-hi">%s</td></tr>' % (a, b, c)
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


def cards_html(items, cols=3):
    out = ['<article class="bs-card" data-reveal>%s<h3>%s</h3><p>%s</p></article>' % (ico(i), t, x) for i, t, x in items]
    return '<div class="bs-grid bs-grid--%d">%s</div>' % (cols, "".join(out))


def how_html(steps):
    out = []
    for i, (title, text) in enumerate(steps, start=1):
        out.append("""
      <article class="bs-card" data-reveal>
        <span class="bs-card-ico" style="background:linear-gradient(135deg,#ffd400,#ff7a1a)"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="#14082e"/><text x="12" y="16.5" text-anchor="middle" font-size="12" font-family="Bricolage Grotesque,sans-serif" font-weight="800" fill="#ffd400">%d</text></svg></span>
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
    rows = "".join('<tr><td>%s</td><td>%s</td><td class="is-hi">%s</td></tr>' % (a, b, c) for a, b, c in page["math"])
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
    rows = "".join('<tr><td>%s</td><td class="is-no">%s</td><td class="is-yes">%s</td></tr>' % (a, b, c) for a, b, c in page["compare"])
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
    rows = "".join('<tr><td>%s</td><td>%s</td><td class="is-hi">%s</td></tr>' % (a, b, c) for a, b, c in page["elsewhere"])
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


def footer_html():
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
     no  : the next offer in the funnel (already wired)
     ========================================================================== -->
<script>
window.BS_CFG = {
  buy: "",
  no: "{{no_url}}"
};
</script>
</head>

<body class="bs-oto">

<!-- ===================================================== 1 · HEADER (centred logo, light) -->
<header class="bs-header">
  <a class="bs-header__logo" href="index.html" aria-label="BookSaga home">
    <img src="images/booksaga-lockup.svg" alt="BookSaga" width="152" height="38">
  </a>
</header>

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

<!-- ===================================================== 4 · WHERE YOUR PLAN STOPS -->
{{stops}}

<!-- ===================================================== 6 · THE PROBLEM -->
<section class="bs-sec" id="problem">
  <div class="bs-wrap">
    <div class="bs-center">
      <span class="bs-eyebrow">The problem</span>
      <h2 class="bs-h2">Why this matters right now</h2>
    </div>
    {{problems}}
  </div>
</section>

<!-- ===================================================== 7 · INTRODUCING -->
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

<!-- ===================================================== 8 · EVERYTHING IT UNLOCKS -->
<section class="bs-sec" id="unlocks">
  <div class="bs-wrap">
    <div class="bs-center">
      <span class="bs-eyebrow">Everything it unlocks</span>
      <h2 class="bs-h2">What you get with {{name}}</h2>
    </div>
    {{unlocks}}
  </div>
</section>

<!-- ===================================================== 9 · HOW IT WORKS -->
<section class="bs-sec bs-sec--alt" id="how-it-works">
  <div class="bs-wrap">
    <div class="bs-center"><h2 class="bs-h2">How it works</h2><p class="bs-sub">Four steps. Nothing to install, nothing to migrate.</p></div>
    {{how}}
  </div>
</section>

<!-- ===================================================== 10 · DEEP DIVES -->
<section class="bs-sec" id="deep-dive">
  <div class="bs-wrap">
    <div class="bs-center"><span class="bs-eyebrow">The detail</span><h2 class="bs-h2">The parts that actually matter</h2></div>
    {{deep}}
  </div>
</section>

<!-- ===================================================== 11 · NUMBERS -->
{{math}}

<!-- ===================================================== 12 · WITHOUT VS WITH -->
{{compare}}

<!-- ===================================================== 13 · WAYS TO USE -->
{{uses}}

<!-- ===================================================== 14 · WHO IT'S FOR -->
{{whofor}}

<!-- ===================================================== 15 · COST ELSEWHERE -->
{{elsewhere}}

<!-- ===================================================== 16 · VALUE STACK -->
{{stack}}

<!-- ===================================================== 17 · PRICE + CTA -->
{{price_section}}

<!-- ===================================================== 18 · GUARANTEE -->
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

<!-- ===================================================== 19 · LAUNCH PRICING -->
<section class="bs-sec bs-sec--tight" id="launch-pricing">
  <div class="bs-wrap bs-narrow bs-center">
    <h2 class="bs-h3">Why the price is lower right now</h2>
    <p class="bs-sub">{{price}} is the launch price for this offer. The regular price shown on the price card is where it goes afterwards. We are not claiming this disappears forever — it stays available from inside the app at the regular price. The discount is real; the scarcity is about the discount, not the product.</p>
  </div>
</section>

<!-- ===================================================== 20 · FAQ -->
{{faq}}

<!-- ===================================================== 21 · P.S. -->
{{ps}}

<!-- ===================================================== 22 · DECISION (LAST) -->
{{decision}}

{{footer}}

<script src="js/oto.js"></script>
</body>
</html>
"""


# --------------------------------------------------------------------------- backgrounds
# Every booksaga-bg-* artwork, split by how light the plate is. The light ones
# only work behind dark text, the dark ones only behind white text, so the page
# alternates themes down its length (which is also how the FE page uses them).
# Served from images/bg/*.webp — the source PNGs are ~1.6 MB each, the WebP
# derivatives are ~15 KB, so all seventeen cost about 300 KB in total.
LIGHT_BGS = [
    "33897742", "342f524c", "3664a8dc", "94759be5", "95a9f497",
    "a2516077", "bacb810f", "bc629c1c", "e36283e1",
]

DARK_BGS = [
    "4af93e7d", "4fb0e65a", "8d92763c", "983a9dc1",
    "9fcb1f03", "a0802078", "d3fae72c", "e867b41b",
]

SECTION_RE = re.compile(r"<section\b[^>]*>")


def apply_backgrounds(html, page_index):
    """Give every section its own background artwork.

    The first two sections (order confirmed + hero) stay dark so the page opens
    the way it always did. After that themes alternate: paper, dark, paper...
    which uses each of the nine light plates exactly once per page.
    A per-page rotation keeps two OTOs from looking identical.

    The artwork is attached as a .bs-bg-<hash> class rather than an inline
    style: a relative url() inside a custom property resolves against the
    stylesheet that declares it, so the paths live in css/oto.css.
    """
    light_i = (page_index * 2) % len(LIGHT_BGS)
    dark_i = (page_index * 3) % len(DARK_BGS)

    out = []
    pos = 0
    for idx, m in enumerate(SECTION_RE.finditer(html)):
        out.append(html[pos:m.start()])
        tag = m.group(0)

        paper = idx >= 2 and idx % 2 == 0 and "bs-decision" not in tag
        if paper:
            art = LIGHT_BGS[light_i % len(LIGHT_BGS)]
            light_i += 1
        else:
            art = DARK_BGS[dark_i % len(DARK_BGS)]
            dark_i += 1

        classes = "bs-has-bg bs-bg-%s%s" % (art, " bs-sec--paper" if paper else "")
        if 'class="' in tag:
            tag = tag.replace('class="', 'class="%s ' % classes, 1)
        else:
            tag = tag[:-1] + ' class="%s">' % classes

        out.append(tag)
        pos = m.end()

    out.append(html[pos:])
    return "".join(out)


def build(page):
    ctx = dict(page)
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
    ctx["footer"] = footer_html()

    html = PAGE_TMPL
    for k, v in ctx.items():
        html = html.replace("{{%s}}" % k, v if isinstance(v, str) else str(v))

    if "{{" in html:
        raise SystemExit("unreplaced placeholder in %s" % page["slug"])

    html = apply_backgrounds(html, page["num"] - 1)

    # Hard content rules for these pages.
    if re.search(r"credit", html, re.I):
        raise SystemExit("%s mentions the internal unit (rule: never name it)" % page["slug"])
    if re.search(r"<video|\.mp4|youtube\.com|youtu\.be|vimeo\.com|wistia", html, re.I):
        raise SystemExit("%s contains a video reference (rule: no video)" % page["slug"])
    if re.search(r"downsell|ds\d\.html", html, re.I):
        raise SystemExit("%s links to a downsell (rule: no downsell pages)" % page["slug"])

    out = os.path.join(OUT_DIR, page["slug"])
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return out, html.count("<section")


if __name__ == "__main__":
    for p in PAGES:
        path, sections = build(p)
        print("%-12s sections=%2d  %s" % (p["slug"], sections, path))
    print("\n%d pages generated." % len(PAGES))
