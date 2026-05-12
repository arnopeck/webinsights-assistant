# WebInsights Assistant — Product Decisions

This document records the current product decisions before rewriting code.

## Product target

WebInsights Assistant should become a real, easy-to-install analytics product for users who are not necessarily programmers.

The preferred product shape is:

- uploadable folder on a normal PHP-capable server;
- browser-based interface;
- no terminal required for the final user;
- direct GA4 connection from the application;
- HTML report shown in the browser;
- JSON export/report model where useful;
- local persistence where the application is installed;
- possible future evolution into a WordPress plugin.

## User and usage assumptions

The first target user is a non-technical or semi-technical user who wants to connect GA4 and generate readable reports without using the GA4 interface directly.

The user flow should be:

1. Upload the application folder to a PHP server.
2. Open the setup page in the browser.
3. Configure Google access.
4. Connect/select a GA4 property.
5. Generate an HTML report.
6. Save report history locally on the installation.

## Installation requirement

The product should be installable without terminal commands.

Preferred installation mode:

- upload folder by FTP/file manager;
- open setup URL;
- complete browser-based setup.

Acceptable later alternatives:

- packaged ZIP release;
- WordPress plugin;
- hosted/cloud edition.

Avoid for the first product:

- requiring `npm install`;
- requiring Python installation;
- requiring Composer from the final user;
- requiring command-line setup.

## Stack decision

Chosen stack for the first real product:

- **Backend:** PHP.
- **Frontend:** vanilla HTML/CSS/JavaScript.
- **Persistence:** SQLite by default, if supported; fallback to JSON files only if SQLite is unavailable.
- **Charts:** lightweight browser-side charts using vanilla JS or a small bundled chart library.
- **Authentication to Google:** OAuth Google, because it is more user-friendly than asking non-technical users to create service-account JSON credentials.
- **Future path:** WordPress plugin wrapper can reuse much of the PHP/domain logic if the code is kept framework-light.

## Why PHP + vanilla JS

This stack matches the installation requirement better than Next.js, Node.js, or Python:

- typical shared hosting supports PHP;
- users can upload a folder without terminal access;
- credentials and tokens can stay server-side;
- frontend can stay simple and understandable;
- future WordPress plugin path remains realistic;
- no build step is required for the final user;
- no server process manager is required.

## Why not static-only HTML/CSS/JS

A purely static app would be simpler, but it is not enough for the chosen product because direct GA4 connection and OAuth require server-side handling.

Static-only can still be used for:

- demo mode;
- local fixture reports;
- exported report pages;
- documentation examples.

But the real product needs a server-side component.

## Google Analytics access

Decision:

- GA4 direct connection should be included from the beginning.
- OAuth Google should be preferred over service-account setup for ease of use.
- The setup flow should guide the user through Google configuration as clearly as possible.

Open implementation detail:

- Whether the first MVP uses the user's own Google OAuth app credentials, a centrally managed OAuth app, or both.

For a simple uploadable product, requiring the user to create Google OAuth credentials is still a friction point. A hosted/managed OAuth bridge may eventually be needed if the product is intended for very non-technical users.

## Data location and privacy

Decision:

- Data should remain local to the installation by default.
- In a self-hosted PHP folder, “local” means stored on that server.
- A hosted/cloud edition may later store data centrally, but should be a separate product mode.

Saved data should include:

- connected property metadata;
- generated report history;
- previous metrics needed for comparisons;
- data quality warnings;
- insight/recommendation history.

Sensitive data such as OAuth tokens must be stored carefully and never committed to the repository.

## First output

Decision:

- The first output is an HTML report in the browser.
- JSON export/report model should exist because it keeps the report structured and testable.

PDF can come later.

## AI policy

Decision:

- AI can be used for explanations and recommendations.
- Deterministic analytics and evidence extraction must happen first.
- The system must not invent metrics or conclusions.
- Insight/recommendation text should be traceable to source metrics.

Practical first version:

- deterministic rules generate structured insights;
- optional AI layer rewrites/explains them in clearer language;
- later, AI can help with deeper recommendations, still constrained by evidence.

## MVP scope

The first MVP should include:

- browser setup page;
- OAuth configuration/status;
- GA4 connection;
- property/date-range form;
- demo mode for testing without Google;
- report generation from GA4 or explicit demo data;
- HTML report view;
- saved report history;
- basic comparison with previous period;
- data quality warnings;
- evidence-backed insights;
- recommendations linked to insights.

## MVP non-goals

Not included in the first MVP:

- SaaS multi-tenant account system;
- payments/billing;
- public cloud hosting;
- full WordPress plugin packaging;
- PDF export;
- BigQuery;
- Search Console;
- advanced scheduled reports;
- complex frontend framework;
- CLI-only usage.

## Proposed repository structure

```text
webinsights-assistant/
├── public/
│   ├── index.php
│   ├── setup.php
│   ├── report.php
│   ├── assets/
│   │   ├── app.css
│   │   └── app.js
│   └── api/
│       ├── connect-google.php
│       ├── oauth-callback.php
│       ├── properties.php
│       ├── generate-report.php
│       └── reports.php
├── app/
│   ├── Bootstrap.php
│   ├── Config.php
│   ├── Security/
│   ├── Storage/
│   ├── Google/
│   ├── Analytics/
│   ├── Insights/
│   ├── Reports/
│   └── Support/
├── storage/
│   ├── .gitkeep
│   └── README.md
├── fixtures/
│   └── ga4-demo.json
├── tests/
├── docs/
├── .env.example
└── README.md
```

## Open technical questions

Before implementation, decide:

1. Should the app support SQLite only, or SQLite plus JSON fallback?
2. Should OAuth credentials be entered by the installer, or should there eventually be a managed OAuth app?
3. Should the first PHP code avoid Composer entirely, or can release ZIPs include `vendor/` dependencies?
4. Which minimum PHP version should be required?
5. Should the app be single-site only in MVP?
6. Should the WordPress plugin be a later wrapper around the same core, or a separate build?

## Recommended answers

Initial recommendation:

1. Use SQLite first; add JSON fallback only if necessary.
2. MVP may allow user-provided OAuth credentials; document the friction clearly.
3. Use Composer during development, but release ZIP should include dependencies so final users do not need Composer.
4. Require PHP 8.1+ or 8.2+.
5. Keep MVP single-site/single-GA4-property.
6. Keep PHP core framework-light so a WordPress plugin wrapper can be added later.
