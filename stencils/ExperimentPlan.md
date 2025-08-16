# Experiment Plan Template

Owner: <your name>
Version: <v0.1>
Date: <YYYY-MM-DD>

## Table of Contents
- [Overview](#overview)
- [Hypothesis and Primary Metric](#hypothesis-and-primary-metric)
- [Secondary Metrics and Guardrails](#secondary-metrics-and-guardrails)
- [Population and Eligibility](#population-and-eligibility)
- [Experimental Design](#experimental-design)
- [Randomization Unit and Stratification](#randomization-unit-and-stratification)
- [Sample Size, Duration, and MDE](#sample-size-duration-and-mde)
- [Variants](#variants)
- [Instrumentation and Data Quality](#instrumentation-and-data-quality)
- [Analysis Plan](#analysis-plan)
- [Stop/Ship Criteria](#stopship-criteria)
- [Risks, Ethics, and Privacy](#risks-ethics-and-privacy)
- [Runbook and On-Call](#runbook-and-on-call)
- [Timeline](#timeline)
- [Appendix](#appendix)

## Overview
Briefly describe the change under test, the user journey affected, and why this experiment is the right approach now.

## Hypothesis and Primary Metric
State a falsifiable hypothesis tying the change to a single primary (OMTM) metric. Example: “If we X, then Y will increase by Z% among population P within T days.”

## Secondary Metrics and Guardrails
List 2–4 secondary KPIs and guardrails to detect harm (e.g., error rates, opt-outs, support tickets). Define the acceptable movement direction.

## Population and Eligibility
Define inclusion/exclusion criteria, geography, devices, and any recency/frequency filters. Note ramp strategy if relevant.

## Experimental Design
Choose A/B, A/A, sequential, or quasi-experimental (e.g., difference-in-differences) and justify. Note if this is a paint-the-trunk test (prototype) or production.

## Randomization Unit and Stratification
Specify unit (user, device, account, store) and any stratification variables (locale, cohort) to balance treatment/control.

## Sample Size, Duration, and MDE
Back-of-envelope power planning: baseline rate, desired MDE, power, and alpha. Provide estimated sample size and run time. If not powered, describe decision heuristic.

## Variants
Describe Control and Treatment(s). Include screenshots/wireframes if applicable. List exact copy or UI deltas to avoid ambiguity.

## Instrumentation and Data Quality
- Events and properties to log; sanity checks (e.g., exposure counts match splits).  
- Bot/duplicate filtering, time zone handling, late events, and attribution windows.

## Analysis Plan
Statistical tests (e.g., frequentist with corrected p-values, or Bayesian). Handling of outliers, CUPED/covariate adjustment, segment cuts, and how you’ll interpret mixed signals.

## Stop/Ship Criteria
Pre-commit to criteria to stop early, extend, or ship. Include business and ethical thresholds, not just p-values.

## Risks, Ethics, and Privacy
List risks (user confusion, spam, revenue cannibalization). Address consent, regional privacy laws (GDPR/CCPA), and data retention.

## Runbook and On-Call
Monitoring during the run (dashboards, alerts), escalation path (even if you’re solo), rollback steps, and communication plan.

## Timeline
Key dates: build complete, QA, start, checkpoints, end, decision meeting.

## Appendix
Data sources, queries, prior related experiments, and any raw notes.


