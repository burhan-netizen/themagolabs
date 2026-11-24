# Daily guide routine (themagolabs.com/guides/)

One new guide a day for contractors and trades in the USA, UK, Canada, Australia and New Zealand. It goes live automatically after the checks pass. The owner (Burhan) gets a notification with the link.

## Steps

1. `git pull` on `main`.
2. Open `BLOG-TOPICS.md`. Take the first `todo` row whose group is different from the latest daily post (see `src/posts_src/daily/`). If that topic is already covered by a live guide, mark it `skip` and take the next one.
3. **Research before writing.** Search the main term and close variants. Read the top results and Reddit or forum threads where owners discuss it, and note the questions people actually ask (these become headings and FAQs). For any price, fee, rule or statistic, find a current source from this year and prefer the official page. Figures from forums are presented as "trades report…", never as fact.
4. Copy `src/posts_src/TEMPLATE.py` to `src/posts_src/daily/YYYY-MM-DD-slug.py` (today's date, the slug from the topic row) and write the post.
5. Build and check from `src/`:
   ```
   python3 posts_src/gen.py && python3 build.py && python3 posts_src/check.py
   ```
   Fix every ERROR and rerun until it passes. Fix warnings unless there is a good reason.
6. In `BLOG-TOPICS.md`, set the row's status to today's date. If research turned up two or three good new questions, add them as new `todo` rows at the bottom.
7. Commit `Daily guide: <title>` and push to `main`. Vercel deploys automatically.

## Writing rules

- **Answer first.** The lede and the first section answer the search directly; the rest explains how.
- **Headings are the questions people search,** written plainly ("How much does X cost in 2026?"). Use at least 6 `<h2 id="...">` sections. Use `<h3>` only inside a section.
- **At least 900 words** in the article, plus 4 to 6 FAQs and a 6 to 8 item checklist. Include a table or a worked example with numbers when the topic allows.
- **Solve the problem.** Include scripts, texts to copy, sums, steps and checklists the reader can use today.
- **Voice:** "we" for the Mago Labs, plain English, short sentences, friendly and direct, like a trade owner talking to another.
- **Never use em dashes or en dashes.** Use full stops, commas, colons or slashes.
- **No hyphenated words.** Write "follow up", "call out", "word of mouth", "pay per lead".
- **"Tradie" only in Australia or New Zealand posts.** Otherwise say contractors, trades or tradespeople.
- **Never mention the Mago Labs' own prices.** Market price ranges from sources are fine.
- **Never invent** quotes, statistics, people, reviews or results. No real person's name unless a public figure is quoted from a source.
- **Legal, tax, licensing or employment topics** get general information only, plus the line `<p><em>This guide is general information, not legal or financial advice.</em></p>`.
- **Fair to platforms:** say when a paid platform *is* worth it, not only when it isn't.
- **Link two to four existing guides or services** inside the article where they genuinely help (for example `/guides/local-seo-for-trades/`, `/guides/google-business-profile-checklist/`, `/guides/what-a-trade-website-needs/`, `/services/google-business-profile/`). Put four related guides in `links`.
- **Selling stays soft:** the website and Google Business Profile are presented as the fix where they truly are. Every page already ends with the "send us your Instagram" call to action.
- **Spelling:** international English, plain enough for US readers. Where the US word differs, use both once ("tyre kickers, or tire kickers in the USA").

## SEO checklist (check.py enforces the starred items)

- \* Title 30 to 60 characters, the main search term near the start.
- \* Description 120 to 158 characters, the search term first.
- \* The h1 has an *italic* second half, marked with `*...*`.
- The slug is the main search term, short, with no stop words where possible.
- The main term appears in the title, h1, lede and first section; variants appear naturally in headings and FAQs.
- FAQs match "People also ask" style questions.
