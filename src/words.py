"""All marketing copy for themagolabs.com, written in The Mago Labs brand voice:
outcome first, numbers beat adjectives, plain and direct, confident never cocky.
One italic phrase per headline (*like this*). No em dashes."""

HOME = dict(
    title="The Mago Labs | Website Design Studio for Small Businesses",
    desc="Custom websites built to bring in calls, bookings and jobs. A dental clinic went from 25 to 58 patients a day. Get a free site audit.",
    h1="Websites that *pay for* themselves.",
    lede="Your customers are already searching. Most land on a slow, forgettable site and call someone else. We build the one that gets the call.",
    orbit_label="The pull",
    orbit="Every day, people circle your business. They search your trade, find your name, check your site and decide in eight seconds. Most drift off to someone else. Pretty doesn't fix that. A website built to convert does.",
    proof_h="Numbers beat *adjectives.*",
    work_h="Real businesses. *Real numbers.*",
    split_l="Pretty doesn't pay the bills.",
    split_r="Booked jobs *do.*",
    build_h="What we *build.*",
    concepts_h="What we'd build *for your trade.*",
    method_h="We start with *your numbers.*",
    voices_h="In their *own words.*",
    pay_h="Pay once. *Own it.*",
    final_h="Your hardest working hire *never sleeps.*",
    final_p="Send us your website. We'll tell you, in plain English, exactly where it loses customers and what it would take to fix. Free. No strings.",
)

BUILD = [  # stacked cards on the homepage, each links to a service page
    ("website-design", "enquiry", "Websites that *convert.*", "Designed around the one action that pays you: the call, the booking, the quote. Built for a stranger on a phone with eight seconds to spare."),
    ("website-development", "code", "Fast. Coded by hand. *Yours.*", "No page builders, no pile of plugins, no monthly rent. Your domain and your code, in your name, with hosting included."),
    ("website-redesign", "growth", "Redesigns that *rescue.*", "Your site gets visitors and nobody calls. We find exactly why, then rebuild it around what makes people pick up the phone."),
    ("local-seo", "local", "Found by people *already searching.*", "Someone near you is searching for exactly what you sell, right now. We make sure your name comes up first."),
]

METHOD = [
    ("Day 1", "Your numbers first.", "How many calls, bookings or quotes do you get today? That's the number the whole site is planned to move."),
    ("Day 2", "A fixed quote.", "Exactly what we'll build, what each page says and what it costs. In writing. It doesn't move after you sign."),
    ("Week 1", "You see it first.", "We design from a blank page and write every word. You approve the design before a line of code exists."),
    ("Days 5 to 28", "Live. Then measured.", "Launched on your domain, tested on every phone, wired for Google. Then we watch the numbers with you."),
]

FAQ = [
    ("What does the free audit actually include?", "We go through your site the way a customer does: on a phone, in a hurry. Speed, clarity, trust, how easy it is to call you, how you show up on Google. You get a short, plain English list of what's costing you enquiries, in order of what to fix first."),
    ("No website yet. Is this still for me?", "Yes. Tell us what you do and who you do it for, and we'll send back a working preview of your new site within 48 hours. Free."),
    ("How much does it cost?", "It depends on what your business needs. After a free call you get a fixed quote in writing before any work starts, and it doesn't change. Hosting is included and you own everything."),
    ("How fast can it be live?", "Between 5 and 28 days, depending on the size of the site. You'll know the date before you sign."),
    ("Can you promise I'll rank first on Google?", "No, and be wary of anyone who does. We build every site the way Google rewards: fast, clean, properly structured, with local schema. Then we track what happens."),
    ("What happens after launch?", "The first year of changes and fixes is on us. After that, leave it running as it is, send us changes whenever you need them, or edit it yourself."),
]

SERVICES = {
    "website-design": dict(name="Website design", title="Custom Website Design That Converts",
        h1="Design that *sells.*",
        intro="Most websites are built to be admired. Ours are built to be used: by a stranger, on a phone, deciding in eight seconds whether to call you.",
        included=["A design made for your business from a blank page", "Every word written for your buyers, not filler", "A clear next step on every screen: call, book or quote", "Proof where people look first: results, reviews, credentials", "Phone first, then desktop", "You approve the design before we build"],
        cases=["smile-care-clinic", "jaymo-civil"],
        faq=[("Why not just use a template?", "A template is built for everyone, so it sells for no one. Yours is built around how your customers decide."),
             ("Do you write the words?", "Every one of them, for your business, by a person. You review and approve all of it."),
             ("Will I see it before it's built?", "Yes. You approve the design first. Nothing gets coded until you're happy.")]),
    "website-development": dict(name="Website development", title="Fast Custom Websites, Coded by Hand",
        h1="Fast. Coded by hand. *Yours.*",
        intro="A slow site loses customers before the page even loads. We code every site by hand so it's fast on any phone, secure, simple to run, and yours to keep.",
        included=["Coded by hand, no heavy page builders", "Fast on any phone and any network", "SSL, speed and security set up", "Simple editing for text, photos and prices", "Hosting included for life, fair use", "Domain and code registered in your name"],
        cases=["prabhakar-processors", "centurion-strategic-ventures"],
        faq=[("Who owns the site?", "You do. Domain in your name, code in your hands. No strings attached."),
             ("Is hosting really included?", "Yes, for standard business websites under fair use. No monthly fee."),
             ("Can you build custom features?", "Calculators, booking flows, separate enquiry paths, CRM hookups. We've built all of them for clients.")]),
    "website-redesign": dict(name="Website redesign", title="Website Redesign For More Enquiries",
        h1="Your site gets visitors. *Let's make them call.*",
        intro="A website that looks fine and does nothing is costing you work you never hear about. We find out why people leave, then rebuild around what makes them stay and call.",
        included=["A free audit of exactly what's losing you enquiries", "A rebuild with a clearer structure", "Copy rewritten around your buyers' real questions", "Faster load times on every phone", "Shorter, clearer enquiry forms", "Your Google rankings carried over, not lost"],
        cases=["mnp-co", "jay-mehta-co"],
        faq=[("How do I know I need one?", "If people visit but rarely call, book or enquire, something on the site is stopping them. The free audit tells you what."),
             ("Will I lose my rankings?", "No. We keep what ranks and redirect old pages so the trust you've built carries over."),
             ("Can you keep my content?", "We keep what works, rewrite what doesn't, and tell you which is which.")]),
    "local-seo": dict(name="Local SEO", title="Local SEO That Gets You Found",
        h1="Found by people *already searching.*",
        intro="Right now, someone near you is searching for exactly what you sell. Either your name comes up, or a competitor's does. We make it yours.",
        included=["Pages built around searches that turn into enquiries", "Clean structure and schema Google can read", "Google Business Profile set up and linked", "A simple plan for collecting reviews", "Speed, which Google rewards", "Search Console set up so you see the results"],
        cases=["darshan-galani-co", "ladson-concrete"],
        faq=[("Can you guarantee the top spot?", "Nobody honestly can. We build for how Google ranks, then track what happens."),
             ("How long until it works?", "It depends on your market. One CA firm signed 34 new clients in three months, from Google enquiries."),
             ("What's a Google Business Profile?", "Your listing on Maps and in local results. We set it up properly and link it to your site.")]),
}

INDUSTRIES = {
    "clinics": dict(name="Clinics and healthcare", title="Websites For Clinics and Dentists",
        h1="More patients. *Fewer empty chairs.*",
        intro="Patients pick a clinic online long before they call. We build clinic websites that earn trust in seconds and make booking effortless.",
        points=[("Booking first", "An appointment path on every page, built for a thumb."), ("Trust in seconds", "Experience, qualifications and reviews where patients look first."), ("Found nearby", "Local SEO so you show up when someone nearby searches.")],
        cases=["smile-care-clinic"]),
    "professional-services": dict(name="Professional services", title="Websites For Accountants, Consultants and Advisors",
        h1="As sharp online as you are *in the room.*",
        intro="Clients check a firm online before the first meeting. We've built websites for chartered accountants, consultants and finance firms that bring in enquiries and make that first meeting easier.",
        points=[("Credibility", "A site that reflects the quality of your work."), ("Clarity", "Every service explained plainly, so clients arrive informed."), ("Enquiries", "Simple forms and booking that turn interest into a call.")],
        cases=["darshan-galani-co", "mnp-co", "jay-mehta-co", "kd-mayani-co", "astrabizz", "centurion-strategic-ventures"]),
    "home-services": dict(name="Trades and home services", title="Websites For Contractors and Trades",
        h1="Quotes in. *Phone ringing.*",
        intro="Homeowners and builders search, check your photos and call the contractor who looks the real deal. We build trade websites with real jobs, tap to call buttons and quote forms that take a minute.",
        points=[("Real work", "Your jobs, your crew. No stock photos."), ("One tap away", "Call and quote buttons on every screen."), ("On the map", "Google Business Profile and local SEO for every area you cover.")],
        cases=["jaymo-civil", "ladson-concrete"]),
}

ABOUT = [
    ("The day job", "Eight years inside banks, fintech and insurance taught one thing: people don't buy the best. *They buy the one they trust first.*"),
    ("The nights", "Two of those years were spent building websites after hours, because the work wouldn't leave him alone. Then it stopped being a side thing."),
    ("The studio", "Today it's a studio that has helped 75+ businesses, from dental clinics in India to civil crews in Sydney. Every site still starts on a blank page."),
    ("The point", "Good businesses lose work every day to competitors with half their skill and a better website. *That's the problem we fix.*"),
]

# overview cards on /services/ and /industries/ (slug empty = no dedicated page yet, card opens the contact form)
INDUSTRY_CARDS = [('/trades/', 'Contractors and trades', 'Concrete · Civil · Roofing · Landscaping', 'Homeowners and builders check your photos and call the crew that looks the real deal. Real jobs, call buttons and quote forms that take a minute.'), ('clinics', 'Clinics and healthcare', 'Dental · Medical · Specialists', 'Patients pick a clinic online long before they call. Sites that earn trust in seconds and make booking effortless.'), ('professional-services', 'Professional services', 'Accountants · Consultants · Finance', 'Clients check a firm online before the first meeting. Clear services, real credentials and an easy way to get in touch.'), ('', 'Manufacturers and B2B', 'Textiles · Industrial · Exporters', 'Buyers vet a supplier online before they send an enquiry. Capacity, range and certifications shown so the right buyers reach out.'), ('', 'Real estate', 'Agents · Brokers · Developers', 'Buyers and sellers judge an agent by their website. Listings, local knowledge and a viewing booked in a few taps.'), ('', 'Online stores', 'Brands · Retail · Digital products', 'A product page has no salesperson. Stores that explain, earn trust and take the order on their own.')]

# SEO: keyword label above each H1, page title and a full meta description (no truncation)
SEO_SERVICES = {
    "website-design": ("Custom website design", "Custom Website Design Services",
        "Custom website design for small businesses in India, Australia, the USA, the UK and Canada. Built from a blank page to turn visitors into calls."),
    "website-development": ("Website development", "Website Development, Coded by Hand",
        "Hand coded websites that load fast on any phone, stay secure and belong to you. No page builders, hosting included, domain in your name."),
    "website-redesign": ("Website redesign", "Website Redesign Services for More Enquiries",
        "We find out why visitors leave your site without calling, then rebuild it around what makes them stay. Your Google rankings carried over, not lost."),
    "local-seo": ("Local SEO services", "Local SEO Services for Small Businesses",
        "Local SEO that puts you in front of people already searching nearby: search led pages, clean schema, Google Business Profile and a review plan."),
}
SEO_INDUSTRIES = {
    "clinics": ("Websites for clinics and dentists", "Website Design for Clinics and Dentists",
        "Clinic and dental websites that earn a patient's trust in seconds and make booking easy on any phone. Built with local SEO so nearby patients find you."),
    "professional-services": ("Websites for accountants and consultants", "Website Design for Accountants and Consultants",
        "Websites for chartered accountants, consultants and finance firms that explain your services plainly and turn a first visit into an enquiry."),
}
for _k, (_kw, _t, _d) in SEO_SERVICES.items(): SERVICES[_k].update(kw=_kw, title=_t, desc=_d)
for _k, (_kw, _t, _d) in SEO_INDUSTRIES.items(): INDUSTRIES[_k].update(kw=_kw, title=_t, desc=_d)
INDUSTRIES.pop("home-services")  # now /trades/, redirected in vercel.json

# where each service page sends readers next (extra services and guides)
SERVICE_MORE = {
    "website-design": [("/services/copywriting/", "Copywriting"), ("/guides/what-a-trade-website-needs/", "Guide: what a trade website needs")],
    "website-development": [("/services/google-business-profile/", "Google Business Profile"), ("/guides/what-a-trade-website-needs/", "Guide: what a trade website needs")],
    "website-redesign": [("/free-audit/", "Free website audit"), ("/services/copywriting/", "Copywriting")],
    "local-seo": [("/services/google-business-profile/", "Google Business Profile"), ("/guides/local-seo-for-trades/", "Guide: local SEO for trades"), ("/guides/google-business-profile-checklist/", "Guide: Google Business Profile checklist")],
}

# "who we build for" links on the home and services pages
TRADE_LINKS = [("/trades/concreters/", "Concreters"), ("/trades/excavation/", "Excavation and civil"), ("/trades/roofers/", "Roofers"),
    ("/trades/builders/", "Builders"), ("/trades/landscapers/", "Landscapers"), ("/trades/plumbers/", "Plumbers"),
    ("/trades/electricians/", "Electricians"), ("/trades/hvac/", "HVAC")]
COUNTRY_LINKS = [("/usa/", "USA"), ("/canada/", "Canada"), ("/australia/", "Australia"), ("/uk/", "UK"), ("/new-zealand/", "New Zealand")]
