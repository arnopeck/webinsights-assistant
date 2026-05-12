# WebInsights Assistant — Product Rewrite Project

## Executive summary

WebInsights Assistant should be rebuilt as a real product. The product idea is strong: an assistant that makes GA4 and related web analytics data understandable, actionable, and useful for people who do not want to fight with raw analytics interfaces.

The current implementation does not yet deliver that product. It is mostly a scaffold: authentication can succeed without real credentials, Google Analytics queries return hard-coded sample data, the agent workflow is bypassed by local simulation, and most agent outputs are canned rather than computed from real analytics data.

The correct revision strategy is therefore not cosmetic refactoring. The project needs a deliberate product rewrite around a smaller, credible MVP:

1. Real analytics data extraction.
2. Explicit demo/fixture mode only when requested.
3. Typed contracts between workflow stages/agents.
4. Deterministic processing and validation before any LLM reasoning.
5. Evidence-based insight generation.
6. Reports that clearly distinguish facts, computed metrics, interpretation, recommendations, and uncertainty.
7. Tests that fail when the system silently falls back to fake data.

## Product direction

The goal is to build a useful analytics product, not a technical demo. The product should eventually help users answer questions such as:

- What changed on my website during this period?
- Which traffic channels are improving or declining?
- Which pages deserve attention?
- Are mobile users behaving differently from desktop users?
- Are conversions/events configured well enough to trust the data?
- What should I do next, and why?

The first version should be narrow but real. It is better to generate one honest report from real or explicitly labelled fixture data than many impressive-looking reports built from placeholders.

## Chosen stack

The product should be rebuilt as a **web-first TypeScript product**.

Chosen stack for the rewrite:

- **Language:** TypeScript.
- **Application framework:** Next.js.
- **Runtime:** Node.js.
- **UI:** React.
- **Validation/contracts:** Zod.
- **Database for saved reports/configuration:** PostgreSQL, preferably through Prisma.
- **Charts:** Recharts or Tremor-style React components for the web UI; server-side chart export can be added later only if PDF/static reporting requires it.
- **Testing:** Vitest for unit tests, Playwright later for end-to-end UI tests.
- **Lint/format:** ESLint + Prettier.
- **Deployment target:** Vercel or another simple Node-compatible platform.

Reasoning:

- The desired product must be easy to use, so a browser-based interface is more appropriate than a CLI-first Python tool.
- TypeScript gives one language for UI, API routes, domain models, validation schemas, and tests.
- Next.js makes it easy to start with a local/product UI and grow into a hosted product.
- Zod keeps agent/workflow contracts explicit and testable.
- PostgreSQL/Prisma keeps room for saved properties, report history, accounts, and scheduled reports.
- Python can still be added later as a separate analytics worker if a specific data-science workload justifies it, but it should not be the foundation by inertia.

## Current-state assessment

### Product promise

The intended product is valuable and coherent:

- Make GA4 analytics easier to query and interpret.
- Provide role-friendly reports for owners, marketers, developers, and content teams.
- Coordinate specialist workflow stages for extraction, processing, insight generation, visualization, and recommendations.
- Produce reports that are clear, shareable, and action-oriented.

### Implementation reality

The implementation does not yet deliver that promise.

Observed issues:

- The dependency list includes analytics/data/visualization packages but does not represent a complete, reliable product setup.
- `src/adk_compatibility.py` implements a local compatibility layer that simulates an ADK-like interface instead of relying consistently on a real runtime.
- Multiple source files import `google.adk`, while other parts of the repository fall back to local simulated behavior. This makes runtime behavior ambiguous.
- `src/google_analytics_integration.py` authenticates successfully even when the credentials file is missing and explicitly uses simulated data.
- `src/data_extraction_agent.py`, `src/data_processing_agent.py`, `src/insight_generation_agent.py`, `src/visualization_agent.py`, and `src/recommendation_agent.py` return mostly canned values.
- `src/webinsights_integration.py` constructs an ADK `Runner`, then bypasses it through `_simulate_workflow()`.
- The generated HTML report contains hard-coded metric cards and hard-coded Chart.js datasets.
- The tests mostly assert that dictionaries contain expected keys, so they can pass while the system is still fake.
- The README says to run `python main.py`, but the actual CLI entrypoint is `src/main.py`.
- A backup test file remains in `src/test_webinsights.py.bak`, suggesting incomplete cleanup.

## Revision goals

### Non-negotiable goals

1. No silent fake data in production paths.
2. No insight without traceable source metrics.
3. No recommendation without explicit evidence and confidence.
4. No workflow output without schema validation.
5. No chart using hard-coded sample data when real data was requested.
6. No tests that merely check placeholder structures.
7. No technology decision made only because of the old implementation.

### MVP scope

The first credible version should support:

- Web UI for entering a GA4 property/date range and generating a report.
- Explicit demo mode using labelled fixture data.
- Production mode that fails clearly if GA4 credentials/access are missing.
- A single GA4 property ID.
- Date-range selection.
- Four core report sections:
  - traffic overview;
  - acquisition channels;
  - top pages / landing pages;
  - device breakdown.
- Period-over-period comparison.
- HTML/web report and JSON report model.
- Transparent metadata showing property, date range, queried metrics, queried dimensions, data mode, and data freshness.

### Out of scope for MVP

- BigQuery warehouse integration.
- Scheduled reports.
- Multi-property dashboards.
- Multi-user authentication.
- Public SaaS billing/subscriptions.
- Industry benchmarks unless an explicit, maintained benchmark source is added.
- Generic technology trend recommendations not grounded in the site data.

## Target architecture

```text
Browser UI
   |
   v
Next.js Server Action / API Route
   |
   v
Request Parser / Orchestrator
   |
   +--> Analytics Query Planner
   |       |
   |       v
   |   GA4 Extractor
   |       |
   |       v
   |   Raw Analytics Dataset
   |
   +--> Data Quality Agent
   |       |
   |       v
   |   Validated Analytics Dataset
   |
   +--> Metrics Processor
   |       |
   |       v
   |   Computed Metrics + Comparisons
   |
   +--> Insight Agent
   |       |
   |       v
   |   Evidence-backed Insights
   |
   +--> Recommendation Agent
   |       |
   |       v
   |   Prioritized Actions
   |
   +--> Visualization / Report Builder
           |
           v
        Web report / JSON report model
```

## Proposed repository structure

```text
webinsights-assistant/
├── package.json
├── next.config.ts
├── tsconfig.json
├── .env.example
├── src/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── reports/
│   │   └── api/
│   ├── components/
│   │   ├── report/
│   │   └── ui/
│   ├── domain/
│   │   ├── schemas/
│   │   ├── analytics/
│   │   ├── insights/
│   │   └── reports/
│   ├── agents/
│   │   ├── orchestrator.ts
│   │   ├── query-planner.ts
│   │   ├── data-quality.ts
│   │   ├── metrics-processor.ts
│   │   ├── insight-generator.ts
│   │   ├── recommendation-generator.ts
│   │   └── report-builder.ts
│   ├── integrations/
│   │   └── ga4.ts
│   ├── fixtures/
│   │   └── ga4-demo-response.json
│   └── lib/
│       ├── env.ts
│       └── logger.ts
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── docs/
    ├── REVISION_PROJECT.md
    ├── STACK_DECISION.md
    └── AGENTS_REWRITE_PLAYBOOK.md
```

## Data contracts

All workflow boundaries should use TypeScript types plus Zod schemas. Suggested core contracts:

### AnalyticsRequest

Required fields:

- `propertyId`
- `startDate`
- `endDate`
- `comparisonMode`: `none`, `previous_period`, `previous_year`
- `requestedReports`: list of report identifiers
- `audience`: `owner`, `marketing`, `developer`, `content`, `executive`
- `language`: `en`, `it`
- `dataMode`: `production`, `demo`, `fixture`

### AnalyticsDataset

Required fields:

- `source`: `ga4`, later optionally `search_console`, `bigquery`, etc.
- `propertyId`
- `dateRange`
- `rows`
- `metricNames`
- `dimensionNames`
- `queryMetadata`
- `isSampled`
- `warnings`

### ComputedMetrics

Required fields:

- `overview`
- `timeseries`
- `acquisition`
- `pages`
- `devices`
- `comparisons`
- `dataQuality`

### Insight

Required fields:

- `title`
- `severity`: `info`, `opportunity`, `warning`, `critical`
- `evidence`: list of metric references
- `explanation`
- `confidence`: numeric score from 0 to 1
- `recommendedFollowup`

### Recommendation

Required fields:

- `action`
- `why`
- `expectedImpact`
- `effort`: `low`, `medium`, `high`
- `priority`: `low`, `medium`, `high`
- `evidence`
- `ownerRole`

## Agent collaboration model

The rewrite should not use isolated classes that return canned dictionaries. It should use collaborative workflow stages with strict input/output contracts.

### 1. Orchestrator

Responsibilities:

- Parse the user request into an `AnalyticsRequest`.
- Select the required reports and date ranges.
- Call specialist stages in the correct order.
- Stop the workflow if data quality is insufficient.
- Assemble the final response.

Must not:

- Invent metrics.
- Generate business recommendations directly.
- Bypass validation.

### 2. Query Planner

Responsibilities:

- Translate `AnalyticsRequest` into GA4 query specs.
- Choose dimensions and metrics.
- Define comparison queries.
- Keep a query manifest for report provenance.

Must not:

- Call GA4 directly.
- Interpret results.

### 3. GA4 Extractor

Responsibilities:

- Authenticate with GA4.
- Execute query specs.
- Normalize raw API responses into `AnalyticsDataset`.
- Return explicit errors for missing credentials, missing property access, invalid metrics, quota issues, and empty results.

Must not:

- Fall back to fake data unless demo or fixture mode is enabled explicitly.

### 4. Data Quality Agent

Responsibilities:

- Validate date ranges, row counts, missing values, impossible values, and empty dimensions.
- Detect likely configuration problems, for example zero events or no conversions.
- Add warnings and block unsafe insight generation when data is not trustworthy.

### 5. Metrics Processor

Responsibilities:

- Compute derived metrics.
- Calculate period-over-period deltas.
- Sort top pages and channels.
- Prepare chart-ready data.

Must remain deterministic and testable.

### 6. Insight Generator

Responsibilities:

- Generate explanations from validated/computed metrics.
- Attach evidence to every insight.
- Explain uncertainty.
- Produce role-specific language without changing the underlying facts.

### 7. Recommendation Agent

Responsibilities:

- Convert insights into prioritized actions.
- Estimate effort and likely impact.
- Distinguish analytics-backed recommendations from hypotheses.
- Avoid generic advice when evidence is weak.

### 8. Report Builder

Responsibilities:

- Generate the report model used by the web UI and JSON export.
- Render charts from computed data only.
- Include methodology and data-source metadata.
- Make reports shareable and readable by non-technical users.

## Rewrite phases

### Phase 0 — Product foundation

Deliverables:

- Add Next.js/TypeScript project foundation.
- Add Zod schemas for core contracts.
- Add demo mode and fixture data.
- Add Vitest.
- Add ESLint/Prettier.
- Add CI that runs tests.

Acceptance criteria:

- `npm run dev` starts the app.
- The home page shows a simple report-generation form.
- `npm test` runs cleanly.
- No production path imports old Python simulation code.

### Phase 1 — Real GA4 integration

Deliverables:

- Implement credential loading.
- Implement GA4 query execution.
- Implement explicit demo mode using fixtures.
- Implement extraction errors.

Acceptance criteria:

- Missing credentials fail in production mode.
- Demo mode loads fixture data only when explicitly requested.
- Integration tests can run against fixtures without real credentials.

### Phase 2 — Deterministic analytics pipeline

Deliverables:

- Typed contracts.
- Data quality checks.
- Period-over-period comparison.
- Metric calculations.

Acceptance criteria:

- Processor tests verify exact calculations.
- Empty datasets produce clear warnings.
- No generated report uses hard-coded metrics.

### Phase 3 — Evidence-backed insights

Deliverables:

- Insight model with evidence references.
- Rule-based insight generation for MVP.
- Optional LLM narrative layer after deterministic insight selection.

Acceptance criteria:

- Every insight links to one or more metrics.
- Confidence is explicit.
- The same input dataset produces stable insight IDs.

### Phase 4 — Reports and UX

Deliverables:

- Web report UI.
- JSON export.
- Clear language profiles for owner, marketing, developer, and content audiences.

Acceptance criteria:

- Outputs are generated from the same report model.
- Report includes query manifest and data quality warnings.
- Charts use real computed data.

### Phase 5 — Persistence and productization

Deliverables:

- Store generated reports.
- Store property configuration.
- Add report history.
- Prepare authentication/user accounts if needed.

Acceptance criteria:

- A user can generate and revisit at least one saved report.
- Sensitive credentials are not stored insecurely.

## Testing strategy

### Unit tests

- Query planning.
- Date range logic.
- GA4 response normalization.
- Metric calculations.
- Data quality warnings.
- Insight rules.
- Recommendation prioritization.

### Contract tests

- Agent/workflow input-output schemas.
- Report schema.
- GA4 fixture compatibility.

### Integration tests

- Fixture-based full workflow.
- Optional real GA4 smoke test gated by environment variables.

### Regression tests

Add a test for each bug fixed during the rewrite. Never fix behavior without a test that proves it.

## Migration strategy

1. Keep the current Python implementation in place temporarily.
2. Build the new Next.js product foundation next to it.
3. Add a new web entrypoint.
4. Reproduce demo behavior using explicit fixture mode.
5. Switch documentation to the new product only when MVP works.
6. Remove or archive old simulated Python modules when replaced.

## First implementation backlog

High priority:

- Add Next.js/TypeScript foundation.
- Add core Zod schemas.
- Add web form for report generation.
- Add fixture-mode extractor.
- Add production-mode credential validation.
- Add report model and simple report page.
- Add tests for missing credentials and explicit demo mode.

Medium priority:

- Add role-specific summaries.
- Add JSON export.
- Add report history.
- Add local cache for GA4 query results.

Low priority:

- Add scheduled reports.
- Add multi-property analysis.
- Add BigQuery support.
- Add a Python analytics worker only if TypeScript becomes limiting for analytics processing.

## Definition of done for the first product slice

A credible first product slice must satisfy both production and demo paths.

Demo path:

- User opens the web app.
- User selects demo mode.
- User chooses a date range and audience.
- App generates a labelled demo report.
- Report uses fixture data through the same pipeline used by production.

Production path:

- User enters a GA4 property ID.
- Server validates credentials/access.
- App queries GA4.
- App generates a report with real metrics, data quality warnings, evidence-backed insights, and recommendations.
- App fails clearly if credentials or GA4 access are missing.

## Notes for future implementation

This document intentionally does not claim the rewrite has already been implemented. It defines the product rewrite, chosen stack, target architecture, workflow model, backlog, and acceptance criteria. The next step is to create the Next.js/TypeScript foundation in a dedicated branch or direct commit, after reviewing the scaffold before saving it.
