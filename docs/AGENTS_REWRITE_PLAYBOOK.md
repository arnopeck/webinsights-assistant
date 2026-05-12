# WebInsights Assistant — Agents Rewrite Playbook

This playbook defines the collaborative agent system to build during the rewrite. It is intentionally implementation-oriented: each agent has a clear contract, responsibilities, forbidden behaviors, and test requirements.

## Core principle

Agents are not decorative classes. An agent exists only when it owns a distinct decision boundary and produces a validated artifact that another part of the system consumes.

In the current prototype, several agents mainly add canned dictionaries to a shared state. In the rewrite, each agent must produce typed outputs with traceable evidence.

## Shared workflow state

The orchestrator should pass a structured state object, not an unbounded dictionary.

Recommended state sections:

- `request`: parsed user request.
- `query_plan`: GA4 query plan.
- `datasets`: extracted raw datasets.
- `quality`: data quality findings.
- `metrics`: computed metrics and comparisons.
- `insights`: evidence-backed insights.
- `recommendations`: prioritized actions.
- `report`: final report model.
- `trace`: step timings, warnings, errors, and provenance.

No agent should write arbitrary keys into the state. Every state transition should be schema-validated.

## Agent 1 — Orchestrator

### Mission

Turn a user request into a complete, validated analytics workflow.

### Inputs

- Raw user request.
- CLI/API arguments.
- Runtime configuration.

### Outputs

- `AnalyticsRequest`.
- Final `Report`.
- Workflow trace.

### Responsibilities

- Validate required parameters.
- Resolve defaults for date range, comparison mode, audience, language, and output format.
- Select the reports to generate.
- Invoke specialist agents in order.
- Stop or degrade gracefully when a step fails.
- Preserve warnings and provenance.

### Forbidden behaviors

- Inventing analytics values.
- Calling GA4 directly.
- Creating insights directly from raw user text.
- Swallowing errors and continuing with fake data.

### Tests

- Missing property ID.
- Invalid date range.
- Unsupported output format.
- Demo mode explicitly enabled.
- Production mode with missing credentials.

## Agent 2 — Query Planner

### Mission

Translate report requests into exact GA4 Data API query specifications.

### Inputs

- `AnalyticsRequest`.

### Outputs

- `QueryPlan` with one or more `QuerySpec` objects.

### Responsibilities

- Define metric and dimension combinations.
- Define date ranges and comparison ranges.
- Detect impossible combinations before calling GA4.
- Preserve a query manifest for the final report.

### Query groups for MVP

#### Traffic overview

Suggested metrics:

- `activeUsers`
- `newUsers`
- `sessions`
- `screenPageViews`
- `engagementRate`
- `averageSessionDuration`

Suggested dimensions:

- `date`

#### Acquisition

Suggested metrics:

- `sessions`
- `activeUsers`
- `engagementRate`

Suggested dimensions:

- `sessionDefaultChannelGroup`
- `sessionSourceMedium`

#### Pages

Suggested metrics:

- `screenPageViews`
- `activeUsers`
- `averageSessionDuration`
- `engagementRate`

Suggested dimensions:

- `pagePath`
- `pageTitle`

#### Devices

Suggested metrics:

- `sessions`
- `activeUsers`
- `engagementRate`

Suggested dimensions:

- `deviceCategory`
- `browser`
- `operatingSystem`

### Forbidden behaviors

- Returning hard-coded analytics data.
- Hiding invalid query definitions.
- Generating recommendations.

### Tests

- Correct query specs per report type.
- Correct previous-period comparison range.
- Invalid metric/dimension combinations blocked.

## Agent 3 — GA4 Extractor

### Mission

Execute the query plan against GA4 or explicit fixtures.

### Inputs

- `QueryPlan`.
- Credentials/configuration.
- Demo/fixture mode flag.

### Outputs

- `AnalyticsDataset` objects.
- Extraction errors/warnings.

### Responsibilities

- Load credentials.
- Instantiate the GA4 Data API client.
- Execute each query.
- Normalize API rows.
- Preserve metric types.
- Capture quota and API errors.
- Support explicit fixture mode for local development and tests.

### Forbidden behaviors

- Authenticating successfully just because credentials are missing.
- Returning demo data in production mode.
- Hiding partial failures.

### Tests

- Missing credentials fail in production mode.
- Fixture mode returns known fixture rows.
- Empty GA4 response is represented explicitly.
- API error is converted into a typed extraction error.

## Agent 4 — Data Quality Agent

### Mission

Protect the user from misleading reports.

### Inputs

- `AnalyticsDataset` objects.

### Outputs

- `DataQualityReport`.

### Responsibilities

- Check empty datasets.
- Check missing metrics or dimensions.
- Check date coverage.
- Check negative or impossible values.
- Flag zero traffic and suspiciously flat data.
- Decide whether insight generation is safe.

### Forbidden behaviors

- Generating business recommendations.
- Mutating raw data silently.
- Hiding warnings from the final report.

### Tests

- Empty dataset warning.
- Missing dimension warning.
- Partial date coverage warning.
- Insight generation blocked when critical data is missing.

## Agent 5 — Metrics Processor

### Mission

Convert raw analytics rows into deterministic, comparable metrics.

### Inputs

- Validated `AnalyticsDataset` objects.
- `DataQualityReport`.

### Outputs

- `ComputedMetrics`.

### Responsibilities

- Aggregate totals.
- Build time series.
- Rank channels, pages, and devices.
- Calculate deltas vs comparison period.
- Calculate rates and ratios safely.
- Prepare chart-ready structures.

### Forbidden behaviors

- Calling an LLM.
- Writing prose insights.
- Making strategic recommendations.

### Tests

- Totals are exact.
- Rates handle division by zero.
- Deltas are correct.
- Sorting of top pages/channels is stable.

## Agent 6 — Insight Generator

### Mission

Explain what the metrics mean, with evidence.

### Inputs

- `ComputedMetrics`.
- `DataQualityReport`.
- Audience/language preferences.

### Outputs

- List of `Insight` objects.

### Responsibilities

- Identify significant changes.
- Explain trends in accessible language.
- Attach evidence references to every statement.
- Assign confidence.
- Separate facts from interpretation.

### Initial implementation approach

Start rule-based, not LLM-first:

- traffic increase/decrease thresholds;
- engagement rate anomalies;
- channel concentration;
- top-page dependence;
- mobile/desktop divergence;
- pages with high views and low engagement.

An LLM may later rewrite explanations, but it must receive structured insights and must not alter facts.

### Forbidden behaviors

- Producing insight without evidence.
- Writing generic marketing advice.
- Inferring conversions if conversion metrics were not queried.

### Tests

- High-confidence insight for large traffic change.
- No insight for statistically weak/noisy change.
- Every generated insight has evidence.
- Language/audience changes wording but not facts.

## Agent 7 — Recommendation Generator

### Mission

Turn insights into prioritized actions.

### Inputs

- `Insight` objects.
- `ComputedMetrics`.
- Audience preference.

### Outputs

- List of `Recommendation` objects.

### Responsibilities

- Suggest concrete actions.
- Estimate impact and effort.
- Identify owner role.
- Link every action to one or more insights.
- State assumptions.

### Recommendation rules for MVP

- Mobile share high + mobile engagement weak -> mobile UX/performance audit.
- Organic traffic strong + engagement high -> expand related content.
- Single channel dependence -> diversify acquisition.
- Top page concentration -> improve internal linking and conversion paths.
- High traffic + low engagement page -> content/intent mismatch review.

### Forbidden behaviors

- Mentioning trendy tools without metric evidence.
- Estimating specific percentage gains without a source or model.
- Recommending implementation work that cannot be tied to observed behavior.

### Tests

- Recommendations require linked insights.
- Priority is deterministic.
- Generic recommendations are not emitted when data is insufficient.

## Agent 8 — Report Generator

### Mission

Produce user-facing outputs from the validated report model.

### Inputs

- `ComputedMetrics`.
- `Insight` objects.
- `Recommendation` objects.
- Query manifest.
- Data quality report.

### Outputs

- HTML report.
- JSON report.
- Optional Markdown summary.

### Responsibilities

- Render consistent facts across output formats.
- Generate charts from computed data.
- Include methodology and data freshness.
- Clearly label demo data.
- Clearly show warnings.

### Forbidden behaviors

- Hard-coding metric cards.
- Hard-coding chart datasets.
- Hiding data quality warnings.

### Tests

- HTML contains report metadata.
- JSON validates against schema.
- Demo report is visibly labelled as demo.
- Charts use computed values.

## Collaboration protocol

Each agent call should follow this pattern:

```text
input model -> validation -> agent work -> output model -> trace event
```

Each trace event should include:

- `step_name`
- `started_at`
- `finished_at`
- `duration_ms`
- `input_summary`
- `output_summary`
- `warnings`
- `errors`

## Error handling model

Use typed errors rather than generic exceptions where possible:

- `ConfigurationError`
- `CredentialError`
- `AnalyticsApiError`
- `EmptyDatasetError`
- `DataQualityError`
- `ReportGenerationError`

Final reports should include non-fatal warnings. Fatal errors should stop the workflow and explain exactly what to fix.

## Demo mode

Demo mode is allowed and useful, but it must be explicit.

Rules:

- CLI flag: `--demo`.
- Report label: `Demo data — not from Google Analytics`.
- JSON field: `data_mode: demo`.
- Tests may use fixture mode by default.
- Production mode must never silently load fixtures.

## LLM use policy

LLMs should be used only after deterministic analytics processing.

Allowed:

- Rewriting a structured insight in simpler language.
- Producing role-specific summaries from validated facts.
- Suggesting wording for recommendations already selected by rules.

Not allowed:

- Inventing metrics.
- Deciding if GA4 data is valid.
- Creating ungrounded strategic claims.
- Estimating ROI without a model.

## Minimum credible MVP checklist

- [ ] One package import path: `webinsights_assistant`.
- [ ] One runtime model: current ADK or framework-neutral, not mixed fake/real ADK.
- [ ] Explicit `--demo` mode.
- [ ] Production mode fails on missing credentials.
- [ ] Real GA4 extractor.
- [ ] Typed contracts across all agent boundaries.
- [ ] Deterministic metric processor.
- [ ] Evidence-backed insights.
- [ ] Recommendations linked to insights.
- [ ] HTML and JSON reports from the same report model.
- [ ] Tests that verify calculations, not just key existence.
