"""
Content for the portfolio page.

This is the Django equivalent of the TIMELINE / PROJECTS / WRITING /
FOCUS_AREAS arrays in the React version — plain Python data, rendered
by portfolio/templates/portfolio/index.html.

For an MVP this is enough. If you outgrow hand-editing this file, the
natural next step is to turn these into Django models (Project, Post,
TimelineEntry) and manage them from /admin instead — the templates
would not need to change, since they already just loop over lists of
dicts with these same keys.
"""

FOCUS_AREAS = [
    "Data Infrastructure",
    "Research Software",
    "Behavioral Data",
    "Leadership",
]

TIMELINE = [
    {
        "when": "Earlier",
        "title": "Geosciences → self-taught engineering",
        "org": "Independent transition",
        "body": (
            "Started in the geosciences, then taught myself full-stack development "
            "from first principles — no formal CS degree, learned by shipping."
        ),
    },
    {
        "when": "Industry",
        "title": "Engineering leadership",
        "org": "Head of Engineering, industry",
        "body": (
            "Led an engineering team before moving into academic research — the kind "
            "of role that makes you care about maintainability, not just features."
        ),
    },
    {
        "when": "Transition",
        "title": "Visiting researcher",
        "org": "Self-funded, Germany",
        "body": (
            "Relocated to Germany as a visiting researcher, funded independently, "
            "before taking up a permanent academic post."
        ),
    },
    {
        "when": "Now",
        "title": "Software Research Engineer & PhD Candidate",
        "org": "GESIS – Leibniz Institute for the Social Sciences · DDD Team",
        "body": (
            "Building and operating the data infrastructure behind large-scale "
            "computational social science research, based in Aachen."
        ),
    },
]

PROJECTS = [
    {
        "name": "GESISSurfMobile",
        "tag": "Behavioral Data",
        "desc": (
            "Cross-platform React Native tracker performing VPN-based packet "
            "inspection on Android and iOS, feeding the panel's web-journey data."
        ),
        "stack": ["React Native", "VPN/packet inspection", "TypeScript"],
    },
    {
        "name": "mcp-server-gesis-surf",
        "tag": "Research Software",
        "desc": (
            "A TypeScript MCP server exposing the panel's PostgreSQL data to LLM "
            "tooling, built with Spec-Driven Development."
        ),
        "stack": ["TypeScript", "MCP", "PostgreSQL"],
    },
    {
        "name": "PreisRe",
        "tag": "Data Infrastructure",
        "desc": (
            "A price-comparison platform for the Mexican grocery retail market — "
            "scraping, normalizing, and serving pricing data at scale."
        ),
        "stack": ["Python", "Scrapy", "Django"],
    },
    {
        "name": "Cross-Retailer Behavioural Clustering",
        "tag": "Research Software",
        "desc": (
            "Academic paper building a verified taxonomy of German online grocery "
            "and retail categories from panel behavior."
        ),
        "stack": ["Verified taxonomy", "WZ 2008", "Academic writing"],
    },
]

# "span" controls the mesh tile shape: "feature" (2x2), "wide" (2x1),
# "tall" (1x2), or "" for a plain 1x1 square.
WRITING = [
    {
        "title": "Why Big Data is important?",
        "date": "Jun 2022",
        "source": "Medium",
        "url": "https://geomario1984.medium.com/why-big-data-is-important-4a9cc4230218",
        "excerpt": (
            "Big Data is a large dataset — a look at Volume, Velocity, and Variety "
            "as the core characteristics that drive modern economies."
        ),
        "span": "feature",
    },
    {
        "title": "How to install Selenium in Linux",
        "date": "Nov 2021",
        "source": "FAUN.dev() · Medium",
        "url": "https://geomario1984.medium.com/how-to-install-selenium-in-linux-e8928b2b709",
        "excerpt": (
            "Running automation tests hosted on Linux servers: installing the "
            "Chrome binary, ChromeDriver, and running headless, GUI-free tests."
        ),
        "span": "wide",
    },
    {
        "title": "Where is Machine Learning not used?",
        "date": "May 2021",
        "source": "Medium",
        "url": "https://geomario1984.medium.com/where-is-machine-learning-not-used-fde3d06879f7",
        "excerpt": (
            "Supervised, unsupervised, and reinforcement learning in practice — "
            "from facial recognition to image analysis."
        ),
        "span": "tall",
    },
    {
        "title": "Why GIT is used. (Git cheatsheet)",
        "date": "Feb 2021",
        "source": "Medium",
        "url": "https://geomario1984.medium.com/why-git-is-used-git-cheatsheet-c2caf5ff2188",
        "excerpt": (
            "A quick-reference guide to managing software development better — "
            "clone, status, add, commit, push."
        ),
        "span": "",
    },
    {
        "title": "How to Kibana?",
        "date": "Feb 2021",
        "source": "Medium",
        "url": "https://geomario1984.medium.com/how-to-kibana-b3518bf07161",
        "excerpt": (
            "Data science works closely with databases — an introduction to "
            "visualizing indexed data with Kibana and Elasticsearch."
        ),
        "span": "",
    },
    {
        "title": "How Elastic search works",
        "date": "Feb 2021",
        "source": "Medium",
        "url": "https://geomario1984.medium.com/how-elastic-search-works-dd8ccc7ee2a1",
        "excerpt": (
            "Documents, indices, and types — Elasticsearch's core terminology, "
            "mapped against familiar SQL concepts."
        ),
        "span": "wide",
    },
    {
        "title": "How Scrapy Python Works? Tutorial (Part 1)",
        "date": "Feb 2021",
        "source": "Medium",
        "url": "https://geomario1984.medium.com/how-scrapy-python-works-fdc539f07967",
        "excerpt": (
            "Web scraping for beginners — using Scrapy to extract and structure "
            "data from websites."
        ),
        "span": "",
    },
    {
        "title": "How to rename columns in Pandas",
        "date": "Jan 2021",
        "source": "Medium",
        "url": "https://geomario1984.medium.com/how-rename-columns-in-pandas-ac1566def47",
        "excerpt": (
            "A basic but powerful Pandas manipulation: renaming DataFrame columns "
            "via the `.columns` property."
        ),
        "span": "",
    },
    {
        "title": "How to print variables in Python",
        "date": "Oct 2020",
        "source": "Medium",
        "url": "https://geomario1984.medium.com/how-to-print-variables-python-b05518962fb0",
        "excerpt": (
            "Variables are the names you assign to data — a beginner-level look "
            "at Python's print function."
        ),
        "span": "",
    },
    {
        "title": "How to create a Pandas DataFrame",
        "date": "Oct 2020",
        "source": "Medium",
        "url": "https://geomario1984.medium.com/how-to-create-pandas-dataframe-feac460ce1f8",
        "excerpt": (
            "Constructing DataFrames by combining multiple Pandas Series into "
            "dictionary-based structures."
        ),
        "span": "tall",
    },
]
