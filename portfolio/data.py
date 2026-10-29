"""
Starter content for the portfolio page.

load_initial_data copies this into an empty database once; after that the
content lives in the database and is edited in /admin, so changing this file
does not change a running site. The profile and its links come from
migration 0003 instead.
"""

FOCUS_AREAS = [
    "Data Infrastructure",
    "Research Software",
    "Behavioral Data",
    "Leadership",
]

# Career since 2017, oldest first. "when" is the field, not a date: the page
# deliberately shows no years, durations or locations.
TIMELINE = [
    {
        "when": "Energy research",
        "title": "Research Associate, Applied Geophysics & Geothermal Energy",
        "org": "E.ON Energy Research Center",
        "body": (
            "Monitored geothermal wells with fibre-optic temperature sensing, built the "
            "PostgreSQL databases behind it, and turned the data into predictive models and "
            "numerical reservoir simulations."
        ),
    },
    {
        "when": "Legal tech",
        "title": "Head of Software Development & Data Science",
        "org": "GeoLegalTech GmbH",
        "body": (
            "Joined as a senior full-stack and data science developer, then led the "
            "company's software development and data science."
        ),
    },
    {
        "when": "Open finance",
        "title": "Senior Full Stack & Data Developer",
        "org": "Finerio Connect",
        "body": (
            "Built and secured data connections to banks' APIs with Python on AWS Lambda, "
            "keeping open-finance data accurate, current and protected."
        ),
    },
    {
        "when": "Research",
        "title": "Senior Research Software Engineer",
        "org": "GESIS – Leibniz Institute for the Social Sciences",
        "body": (
            "Building the software and algorithms that collect and model digital behavioural "
            "data from web and mobile, and supporting researchers from study design to "
            "publication, with open science as the default."
        ),
    },
    {
        "when": "Behavioral analytics",
        "title": "Doctoral Researcher, IT & Business Analytics",
        "org": "University of Cologne",
        "body": (
            "Shoppers don't stay in one segment. Using GESIS Surf data, I model how people move "
            "between behaviours across retailers, with dynamic clusters and Markov chains, and "
            "measure the instability of those moves with Fisher information, to tell seasonal "
            "effects from real shifts in behaviour."
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
