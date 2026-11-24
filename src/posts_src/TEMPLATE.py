# Copy to posts_src/daily/YYYY-MM-DD-slug.py and fill in. The file name sets the date and the slug.
# Rules are in BLOG.md. check.py enforces most of them.
POST = dict(
 kicker="Getting work",          # one of the groups in BLOG-TOPICS.md
 card="One or two sentences for the guide card: what the reader gets from this post.",
 title="Main Search Term as a Clear Title (30 to 60 characters)",
 desc="120 to 158 characters. Start with the search term, promise the answer, mention 2026 when it matters.",
 h1="Plain question or promise, *italic second half.*",
 lede="The short answer in two or three sentences. Someone who reads only this should know what to do.",
 ticks=["What the post covers, point 1", "Point 2", "Point 3"],
 html="""<h2 id="short-answer">The exact question people search?</h2><p>Direct answer first.</p>
<h2 id="section-two">Second question</h2><p>...</p>""",
 checklist=["Six to eight concrete actions", "...", "...", "...", "...", "..."],
 faq=[("Question people also ask?", "Answer in one to three sentences."),
      ("...", "..."), ("...", "..."), ("...", "...")],
 links=["how-to-get-more-customers", "/guides/local-seo-for-trades/", "how-to-get-google-reviews", "/guides/what-a-trade-website-needs/"],
)
