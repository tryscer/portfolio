
# Comosense Home Assignment

## TOC
• Choosing Between Options A and B
• Problem Overview
• Goal
• Defining Success (OMTM)
• Solutions and Decision
• PROJECT: Epics, User Stories, MVP scope
• EPIC In Detail: Flow, Acceptance Criteria, KPIs, Risks
• Pricing Considerations
• GTM Plan

## Choosing Between Options A and B

Option A — Credit Card–Linked Loyalty
- Identify and reward customers by a hashed card token at POS, even without loyalty ID.
- Pre-sale opt-in (during onboarding) and post-sale opt-in (receipt/SMS/email).
Benefit: Increases tagged transaction coverage, auto-awards points/gifts, deeper insights.

Option B — Communication Time Limitation (SMS windows)
- Ensure bulk SMS campaigns are delivered within configured time windows to avoid late-night texts and expired offers; improve error handling.

### Reach
- Option A: High. Impacts 100% of in-store purchases where cards are used; scalable to ecom.
- Option B: Medium-high. Impacts merchants with large SMS lists and frequent campaigns.

### Impact
- Option A: High. +15–30% more identified transactions; +5–10% visit frequency; +3–7% AOV.
- Option B: Medium. +5–10% better campaign conversion; reduced opt-outs due to late messages.

### Ease of Implementation
- Option A: Medium-hard (tokenization partners, consent UX, matching logic, compliance gates).
- Option B: Medium (queue orchestration, time-window constraints, error/timeout handling).

### Risk
- Option A: Higher (privacy/PCI scope, regulatory variance, false-positive matches).
- Option B: Moderate (deliverability, global time zones, partial improvements only).

### RICER Table
| Option | Reach | Impact | Confidence | Effort (1–10) | RICE Score |
|---|---:|---:|---:|---:|---:|
| A: Card-linked | 9 | 9 | 0.7 | 5 | 11.34 |
| B: SMS windows | 7 | 6 | 0.8 | 4 | 8.40 |

### Desicion
- Choose Option A: Credit Card–Linked Loyalty (higher long-term value and defensibility).

## Problem Overview
Merchants lose attribution and cannot reward a large share of in-store purchases when customers forget to identify loyalty at POS. This shrinks program effectiveness and insights. Customers miss points and offers. Como’s data graph under-represents actual behavior.

Stakeholders and why it matters
- Merchants: +15–30% more identified transactions; richer cohorts; higher repeat rate.
- Customers: No-friction rewards; fewer missed perks; better personalization.
- Como: Increased data coverage, stickier integrations, clear ROI stories for sales.

Assumptions
- Como integrates with POS/ecom and payment providers to receive a non-reversible token or network token; no PAN stored.
- Profile graph supports mapping token(s) to customer profiles with consent and audit.
- Real-time eventing is available to award points within 2 seconds at POS.

## Goal 
Enable merchants to award points/gifts/offers using only payment token signals, with explicit consent and privacy compliance, minimizing friction and matching errors.

## Defining Success
- OMTM: Percent of card-present transactions matched to a loyalty profile (coverage).
- Target (pilot): 20% absolute lift in identified transactions within 60 days of launch.
- Guardrails: <0.5% false-positive matches; <1% opt-out after link.

## Solutions

### Solution 1
Card-linked loyalty using tokenization. Pre- and post-sale opt-in flows collect consent; payment tokens sent from POS/ecom via existing integrations; real-time match and award.

### Solution 2
SMS time-window enforcement for campaigns (queue segmentation, time-zone aware send, hard/soft cutoffs, retries, error budgets).

### Decision
Proceed with Solution 1 (Option A) for MVP.

## PROJECT

### EPIC 1:
Card Linking & Consent
#### User story 1: 
As a customer, I can link my card during onboarding by consenting, so I earn rewards automatically.
#### User story 2: 
As a customer, I can link post-sale from an SMS/email prompt tied to my recent purchase.

### Out of Scope for MVP:
- Bank-level account linking; multi-country BIN-specific perks; cross-merchant networks; co-branded card issuance.

## EPIC In Detail: 

### User story 1
As a customer, I can link post-sale from an SMS tied to a recent transaction.

Preconditions
- Merchant enabled card-linked loyalty; POS/ecom integrated for token capture.
- Customer completed a purchase within the last 24 hours.

Flow
1) POS/ecom sends transaction event with payment token (hashed), timestamp, amount.
2) Campaign rule triggers post-sale message with secure link (magic token, 24h TTL).
3) Customer opens link, sees consent screen explaining card token use and privacy.
4) Customer accepts; backend associates hashed token with customer profile.
5) System re-processes recent transaction(s) to award missed points, confirms via SMS/email.

Edge Cases
- Multiple cards on file: show last 4 digits if available; allow manage cards.
- Household/shared cards: allow opt-out per card; require explicit per-card consent.
- Expired link: show re-verify flow via phone/email OTP.

### Acceptance criteria
- Consent screen includes purpose, retention, and revoke controls; records audit trail.
- Linking success ties future transactions with same token within <2s at POS.
- Retroactive award runs for last N days (configurable, default 7), idempotent.
- False-positive match rate <0.5% in monitored pilots.
- Opt-out immediately disables future matching for that token.

### KPIs and guardrails
- Lift in identified transactions vs baseline.
- Opt-in rate post-sale; opt-out rate within 30 days.
- Match latency p95 at POS <2s; retro-proc within SLA.
- Privacy incidents = 0; audit completeness = 100%.

### Solution Overview
- Data: Tokenization service returns network token or irreversible hash + BIN metadata.
- Ingest: POS/ecom sends token in transaction payload through existing connectors.
- Match: Realtime service matches token→profile; if consented award rule runs.
- Storage: Token-to-profile mapping in secure vault; limited access; rotateable.
- Admin: Merchant can enable feature, set retro-window, view coverage metrics.

### User Flow per story
- Post-sale link → Consent → Link success → Retro award → Confirmation.

### Flow charts per user flow
- High-level: Transaction event → Trigger → Consent → Link → Award.

### Risks and considerations
- PCI DSS: Keep out of scope where possible by using irreversible tokens; no PAN storage.
- Privacy: GDPR/CCPA/UK GDPR lawful basis (consent), DSRs (delete, revoke), data minimization.
- Security: Hashing/tokenization partners, key rotation, least-privilege access, audit logs.
- Matching errors: Strict confidence rules; no cross-customer linking; transparent recourse.
- Regional: Time-bound consent, record retention, localization of policy text.

### Riskiest Assumption Test 
- Hypothesis: Customers will link post-sale at >=20% rate if value is clear and flow <30s.
- Test: A/B SMS message variants across 3 merchants; measure opt-in, completion, opt-out.
- Success: 20%+ link rate; <1% opt-out; NPS of flow >40.

### Pricing Considerations
- Packaging: Add-on to Loyalty Pro tier; usage-based after included tokens.
- Metric: Monthly active linked tokens and matched transactions.
- Example: $99/mo + $0.002 per matched transaction (first 50k included).

### GTM Plan
- Pilot: 3–5 merchants across verticals (QSR, retail, beauty) in 1–2 regions.
- Collateral: ROI calculator (lift in identified txns), compliance brief, setup guide.
- Partners: Tokenization provider, major POS ISVs; sales enablement training.
- Rollout: Opt-in beta → GA; case studies; migrate to self-serve in admin.