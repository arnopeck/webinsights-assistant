# WebInsights Assistant — Technical Documentation

## Overview

WebInsights Assistant is being rebuilt as a self-hosted PHP web application for generating readable analytics reports.

The current rewrite focuses on a minimal, working product foundation:

- uploadable PHP application;
- browser interface;
- local SQLite storage;
- explicit demo data mode;
- report history;
- HTML report rendering;
- future GA4 connection using the same report pipeline.

## Architecture

```text
Browser
  |
  v
public/*.php
  |
  v
app/ domain services
  |
  +--> Storage
  +--> Analytics data source
  +--> Report builder
  +--> Insights/recommendations
  |
  v
SQLite + HTML report view
```

## Current implemented foundation

- `public/index.php`: dashboard and demo report form.
- `public/report.php`: report detail view.
- `public/api/generate-demo-report.php`: endpoint that builds and saves a demo report.
- `app/Bootstrap.php`: path helpers and application bootstrapping.
- `app/autoload.php`: lightweight PSR-style autoloader.
- `app/Storage/Storage.php`: SQLite report storage.
- `app/Reports/DemoReportBuilder.php`: deterministic demo report builder.
- `fixtures/ga4-demo.json`: explicit demo analytics data.

## Next implementation steps

1. Add setup/status screen.
2. Add environment and installation checks.
3. Add GA4 connection layer.
4. Add analytics query planner.
5. Add deterministic metrics processor.
6. Add data quality checks.
7. Replace demo-only reporting with GA4-backed reporting.
8. Add tests for storage, report builder, and validation.

## Design rules

- No fake data in production paths.
- Demo data must always be explicit and labelled.
- Report history is stored locally on the installation.
- The frontend remains vanilla HTML/CSS/JS unless a real need appears.
- The PHP core should remain framework-light for a possible future WordPress plugin wrapper.
