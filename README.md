# WebInsights Assistant

WebInsights Assistant is being rebuilt as a simple self-hosted web app for turning GA4 analytics data into clear, readable reports.

The goal is a product that can be installed by copying a folder to a PHP-capable server, opening it in a browser, connecting Google Analytics, and generating reports without using a command line.

## Current rewrite branch

Active rewrite branch:

```text
rewrite/self-hosted-webapp
```

## Product direction

The product is designed to be:

- easy to install on common PHP hosting;
- usable from a browser;
- free from Node/Python build steps for final users;
- able to save report history locally on the installation;
- structured so it can later become a WordPress plugin.

## Chosen stack

- PHP 8.2+
- HTML, CSS, and JavaScript without a frontend framework
- SQLite for local report history
- JSON fixtures for explicit demo mode
- Composer may be used during development, but release packages should include dependencies if/when dependencies are added

## First MVP

The first MVP focuses on:

- setup/status screen;
- demo report generation;
- report history;
- HTML report view;
- JSON report model;
- deterministic metrics, insights, and recommendations;
- later GA4 connection through the same internal report pipeline.

## Local or server installation

For development or local usage, put the repository behind a PHP-capable local server and point the document root to `public/`.

For shared hosting, the final release should be uploadable as a folder. The `storage/` folder must be writable by PHP.

## Repository layout

```text
public/      Browser entrypoints, assets, and small API endpoints
app/         PHP application code
fixtures/    Demo data
storage/     Local database/report storage, excluded from Git except placeholders
docs/        Product and architecture decisions
legacy/      Optional area for old prototype material during migration
```

## Status

This branch is a rewrite in progress. The current priority is building a minimal self-hosted PHP application before integrating real GA4 access.
