# Positioning and Feature Thesis

## Positioning statement
For TTRPG players, non-pro GMs, pro GMs, and local game stores who want reliable groups without platform thrash, our product is a group-finding and session coordination platform that turns natural free-text intent into complete, trustworthy sessions. Unlike forum posts and fragmented LFG channels (Reddit/Discord) or paid-only marketplaces, we combine free-text input with structured previews, scheduling, and safety so groups form faster with higher confidence.

- Target segments: casual players, non-pro GMs/hosts, pro GMs, stores/events.
- Category: gamer group discovery and coordination.
- Core value: trust + speed to session via natural input -> structured plan.
- Key differentiators:
  - Free-text to structured listing (schema extraction + inline clarifications).
  - Built-in schedule alignment (time windows, time zones, calendar sync).
  - Trust signals (profile verification, references/reviews, commitment score, no-show history).
  - Safety and norms (reporting, identity tiers, content guardrails).
  - Cross-posting hooks to Reddit/Discord with back-link to structured flow.

## Feature thesis (prioritized)
- P0 Core
  - Free-text session creation -> structured preview (system fills game, system, VTT/IRL, location/online, seats, levels, beginner-friendly, safety tools).
  - Ambiguity resolution micro-prompts; chip suggestions; inline provenance.
  - Player/GM profiles with minimal required fields; messaging; basic RSVP.
  - Scheduling: availability capture, UTC normalization, ICS/Google Calendar.
- P1 Trust & Safety
  - Identity tiers (email/phone -> social -> gov ID for pros), reputation, reviews.
  - Commitment score (attendance history), deposit/hold for pro games (optional).
  - Report flows, moderation tools, blocklists; session safety checklist.
- P2 Liquidity & Growth
  - Cross-post to Reddit/Discord; auto-sync updates; import replies via link/DM bot.
  - Recommendations: match by schedule, proximity, playstyle, skill level.
  - Store/organizer portals; repeat sessions; templated campaigns.
- P3 Power tools
  - Waitlists, role preferences, pre-session onboarding (rules/tools), AI recap.
  - Payments for pros (escrow, payouts, refund policies) where applicable.

## KPIs
- Conversion to posted session from free-text start.
- Time to first full roster; fill rate by segment.
- No-show rate; dispute/report rate; repeat session rate.
- Message latency to commit (first response -> confirmed).

## Risks and mitigations
- Cold-start liquidity: seed via cross-posting, store partnerships, targeted Discords.
- Safety/abuse: verification tiers, rate limits, quick takedowns, community mods.
- Extraction accuracy: confidence thresholds with human-readable previews and quick edits.
- Fragmentation: bi-directional sync to discovery channels; canonical session page.

## Why now
- High LFG activity has shifted to Discord/Reddit with poor trust and scheduling; VTTs optimize play, not formation. A natural-language, trust-first coordinator addresses the gap.
