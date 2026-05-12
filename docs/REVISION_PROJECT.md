# WebInsights Assistant — Revision Project

## Executive summary

This repository should be treated as a hackathon-era prototype, not as a working production system. The README and technical documentation describe a strong product idea: a multi-agent assistant that makes GA4 data understandable and actionable for non-technical users. The current implementation, however, is largely simulated: authentication can succeed without real credentials, Google Analytics queries return hard-coded sample data, the ADK workflow is bypassed by a local simulation, and most agents produce canned outputs rather than computed insights.

The correct revision strategy is therefore not a cosmetic refactor. The project needs a controlled rewrite around a smaller, testable MVP:

1. Real GA4 data extraction.
2. Typed analytics contracts between agents.
3. Deterministic processing and validation before any LLM reasoning.
4. Evidence-based insight generation.
5. Report output that clearly distinguishes facts, computed metrics, and recommendations.
6. Tests that fail when the system falls back to fake data unexpectedly.

## Current-state assessment

### Product promise

The intended product is valuable and still coherent:

- Make GA4 analytics easier to query and interpret.
- Provide role-friendly reports for owners, marketers, developers, and content teams.
- Coordinate specialist agents for extraction, processing, insight generation, visualization, and recommendations.
- Produce reports that are clear, shareable, and action-oriented.

### Implementation reality

The implementation does not yet deliver that promise.

Observed issues:

- The dependency list includes analytics/data/visualization packages but does not represent a complete modern ADK application setup.
- `src/adk_compatibility.py` implements a fake compatibility layer that simulates an ADK-like interface instead of relying consistently on the real ADK runtime.
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
4. No agent output without schema validation.
5. No chart using hard-coded sample data when real data was requested.
6. No tests that merely check placeholder structures.

### MVP scope

The first credible version should support:

- CLI execution.
- Service-account authentication to GA4.
- A single GA4 property ID.
- Date-range selection.
- Four core reports:
  - traffic overview;
  - acquisition channels;
  - top pages / landing pages;
  - device breakdown.
- Period-over-period comparison.
- HTML and JSON output.
- Transparent metadata showing property, date range, queried metrics, queried dimensions, and data freshness.

### Out of scope for MVP

- BigQuery warehouse integration.
- Scheduled reports.
- Multi-property dashboards.
- Multi-user authentication.
- Public web UI.
- Industry benchmarks unless an explicit, maintained benchmark source is added.
- Generic technology trend recommendations not grounded in the site data.

## Target architecture

```text
User request
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
   +--> Visualization / Report Agent
           |
           v
        HTML / JSON / Markdown report
```

## Proposed package structure

```text
webinsights_assistant/
├── pyproject.toml
├── README.md
├── .env.example
├── src/
│   └── webinsights_assistant/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── logging.py
│       ├── models/
│       │   ├── requests.py
│       │   ├── analytics.py
│       │   ├── insights.py
│       │   └── reports.py
│       ├── integrations/
│       │   └── ga4.py
│       ├── agents/
│       │   ├── orchestrator.py
│       │   ├── query_planner.py
│       │   ├── data_quality.py
│       │   ├── metrics_processor.py
│       │   ├── insight_generator.py
│       │   ├── recommendation_generator.py
│       │   └── report_generator.py
│       ├── reporting/
│       │   ├── html.py
│       │   ├── json.py
│       │   └── charts.py
│       └── fixtures/
│           └── ga4_sample_response.json
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── docs/
    ├── REVISION_PROJECT.md
    └── AGENTS_REWRITE_PLAYBOOK.md
```

## Data contracts

All agent boundaries should use typed models. Suggested core contracts:

### AnalyticsRequest

Required fields:

- `property_id`
- `start_date`
- `end_date`
- `comparison_mode`: `none`, `previous_period`, `previous_year`
- `requested_reports`: list of report identifiers
- `audience`: `owner`, `marketing`, `developer`, `content`, `executive`
- `language`: `en`, `it`

### AnalyticsDataset

Required fields:

- `source`: `ga4`
- `property_id`
- `date_range`
- `rows`
- `metric_names`
- `dimension_names`
- `query_metadata`
- `is_sampled`
- `warnings`

### ComputedMetrics

Required fields:

- `overview`
- `timeseries`
- `acquisition`
- `pages`
- `devices`
- `comparisons`
- `data_quality`

### Insight

Required fields:

- `title`
- `severity`: `info`, `opportunity`, `warning`, `critical`
- `evidence`: list of metric references
- `explanation`
- `confidence`: numeric score from 0 to 1
- `recommended_followup`

### Recommendation

Required fields:

- `action`
- `why`
- `expected_impact`
- `effort`: `low`, `medium`, `high`
- `priority`: `low`, `medium`, `high`
- `evidence`
- `owner_role`

## Agent collaboration model

The rewrite should not use six isolated classes that return canned dictionaries. It should use agents as collaborative specialists with strict input/output contracts.

### 1. Orchestrator Agent

Responsibilities:

- Parse the user request into an `AnalyticsRequest`.
- Select the required reports and date ranges.
- Call specialist agents in the correct order.
- Stop the workflow if data quality is insufficient.
- Assemble the final response.

Must not:

- Invent metrics.
- Generate business recommendations directly.
- Bypass validation.

### 2. Query Planner Agent

Responsibilities:

- Translate `AnalyticsRequest` into GA4 query specs.
- Choose dimensions and metrics.
- Define comparison queries.
- Keep a query manifest for report provenance.

Must not:

- Call GA4 directly.
- Interpret results.

### 3. GA4 Extraction Agent

Responsibilities:

- Authenticate with Google Analytics Data API.
- Execute query specs.
- Normalize raw API responses into `AnalyticsDataset`.
- Return explicit errors for missing credentials, missing property access, invalid metrics, quota issues, and empty results.

Must not:

- Fall back to fake data unless `--demo` or an explicit test fixture mode is enabled.

### 4. Data Quality Agent

Responsibilities:

- Validate date ranges, row counts, missing values, impossible values, and empty dimensions.
- Detect likely configuration problems, for example zero events or no conversions.
- Add warnings and block unsafe insight generation when data is not trustworthy.

### 5. Metrics Processor Agent

Responsibilities:

- Compute derived metrics.
- Calculate period-over-period deltas.
- Sort top pages and channels.
- Prepare chart-ready data.

Must remain deterministic and testable.

### 6. Insight Generator Agent

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

### 8. Report Generator Agent

Responsibilities:

- Generate HTML, JSON, and optionally Markdown reports.
- Render charts from computed data only.
- Include methodology and data-source metadata.
- Make reports shareable and readable by non-technical users.

## Rewrite phases

### Phase 0 — Stabilize the repository

Deliverables:

- Add `pyproject.toml`.
- Move code from `src/*.py` into a proper package.
- Remove `.bak` files.
- Add `.env.example`.
- Add linting and formatting configuration.
- Add CI that runs tests.

Acceptance criteria:

- `python -m webinsights_assistant --help` works.
- Tests run without modifying `sys.path` manually.
- No production module imports test or compatibility code.

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

- HTML report template.
- JSON report output.
- Optional Markdown summary.
- Clear language profiles for owner, marketing, developer, and content audiences.

Acceptance criteria:

- HTML and JSON outputs are generated from the same report model.
- Report includes query manifest and data quality warnings.
- Charts use real computed data.

### Phase 5 — Modern agent runtime

Deliverables:

- Replace fake compatibility layer with real current ADK abstractions or a deliberately framework-neutral workflow engine.
- Implement observability for agent steps.
- Add tracing of inputs/outputs per step.

Acceptance criteria:

- There is one runtime model, not a mix of fake ADK and real ADK imports.
- Every workflow step has logged inputs, outputs, timing, and errors.

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

- Agent input/output schemas.
- Report schema.
- GA4 fixture compatibility.

### Integration tests

- Fixture-based full workflow.
- Optional real GA4 smoke test gated by environment variables.

### Regression tests

Add a test for each bug fixed during the rewrite. Never fix behavior without a test that proves it.

## Migration strategy

1. Keep the current prototype in place temporarily.
2. Build the new package next to it.
3. Add a new CLI entrypoint.
4. Reproduce the current demo behavior using explicit fixture mode.
5. Switch documentation to the new CLI only when MVP works.
6. Remove or archive the old prototype modules.

## First implementation backlog

High priority:

- Create `pyproject.toml`.
- Add `src/webinsights_assistant/` package.
- Add `AnalyticsRequest`, `AnalyticsDataset`, `ComputedMetrics`, `Insight`, `Recommendation`, and `Report` models.
- Implement fixture-mode GA4 extractor.
- Implement production-mode credential validation.
- Replace hard-coded chart/report data with report-model data.
- Add tests for missing credentials and explicit demo mode.

Medium priority:

- Add role-specific summaries.
- Add Markdown output.
- Add report templates.
- Add local cache for GA4 query results.

Low priority:

- Add web interface.
- Add scheduled reports.
- Add multi-property analysis.
- Add BigQuery support.

## Definition of done for the rewrite

The rewrite is credible when this command works without fake data:

```bash
webinsights analyze \
  --property-id 123456789 \
  --start-date 2026-04-01 \
  --end-date 2026-04-30 \
  --compare previous_period \
  --audience owner \
  --format html
```

And when this command works with explicit fixtures:

```bash
webinsights analyze \
  --demo \
  --start-date 2026-04-01 \
  --end-date 2026-04-30 \
  --format json
```

The first command must fail clearly if credentials or GA4 access are missing. The second command may use fixture data, but the output must clearly say it is demo data.

## Notes for future implementation

This document intentionally does not claim the rewrite has already been implemented. It defines the revision project, target architecture, agent collaboration model, backlog, and acceptance criteria. The next commit should start Phase 0 by adding packaging, typed models, fixture-mode extraction, and tests.
