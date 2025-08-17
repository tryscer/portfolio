# GameConnect — Product Requirements Document (PRD)

Owner: Jonny Silver
Version: v0.1
Date: 2025-08-14

## Table of Contents
- [Overview and Context](#overview-and-context)
- [Problem Statement](#problem-statement)
- [Goals and Non-Goals](#goals-and-non-goals)
- [Target Users and Personas](#target-users-and-personas)
- [Market and Competitive Context](#market-and-competitive-context)
- [User Insights and Assumptions](#user-insights-and-assumptions)
- [Jobs To Be Done and Key Use Cases](#jobs-to-be-done-and-key-use-cases)
- [Scope](#scope)
- [Success Metrics](#success-metrics)
- [Solution Overview](#solution-overview)
- [User Experience](#user-experience)
- [Functional Requirements](#functional-requirements)
- [Non-Functional Requirements](#non-functional-requirements)
- [Data Model and Integrations](#data-model-and-integrations)
- [Security, Privacy, and Compliance](#security-privacy-and-compliance)
- [Analytics and Instrumentation](#analytics-and-instrumentation)
- [Delivery Plan (Solo Operator + Lovable)](#delivery-plan-solo-operator--lovable)
- [MVP Plan and Phasing](#mvp-plan-and-phasing)
- [Risks and Mitigations](#risks-and-mitigations)
- [Operational Readiness](#operational-readiness)
- [Go-To-Market](#go-to-market)
- [Dependencies and Open Questions](#dependencies-and-open-questions)
- [Appendix](#appendix)

## Overview and Context
GameConnect helps gamers find people to play with and coordinate sessions. It combines a social layer with scheduling/coordination tools to reduce friction from discovery to a confirmed session. Initial categories: tabletop RPGs, LARP, card games (e.g., MTG), and miniature games.

## Problem Statement
Discovery and coordination are fragmented across Reddit, Discord, forums, and VTTs. Players and hosts struggle to match on schedule, location/online preferences, and playstyle. Result: low show-up rates, high drop-off from interest to session, and poor trust signals.

## Goals and Non-Goals
- Goals
  - Increase conversion from interest to confirmed session by 25% vs. baseline channels.
  - Reduce time-to-fill (TtF) a session roster to <7 days for 80% of posts.
  - Achieve p95 schedule alignment flow time <90 seconds from entry to proposed slots.
  - Reach DAU/WAU > 0.25 within 90 days of MVP launch.
- Non-Goals
  - Full-featured VTT gameplay (focus is formation/coordination).
  - Global payments marketplace for pro GMs at MVP (defer to P2; simple links allowed).
  - Advanced content moderation beyond basic reporting and blocklists in MVP.

## Target Users and Personas
- Player (primary): Wants to discover/join compatible games; cares about schedule, vibe, travel/online.
- Non-professional GM/Host: Wants to post a session, fill seats reliably, and minimize logistics.
- Professional GM/Host (secondary at MVP): Runs paid games; needs reputation and simple payments.
- Business/Organizer (secondary): Stores/conventions seeking event signups and repeat players.

## Market and Competitive Context
Alternatives: Reddit r/lfg, Discord servers/directories, Roll20 LFG, GameTree, GameFor, Warhorn. Differentiators: natural free-text to structured listing, integrated schedule alignment and calendar sync, stronger trust/verification signals, and cross-posting hooks back to fragmented channels.

## User Insights and Assumptions
- Insights (directional): High interest flows on Reddit/Discord but low trust and scheduling UX; hosts need simpler roster management; beginners need clearer expectations.
- Assumptions: Users will provide minimal profile info if it improves matching; hosts will accept suggested time windows; cross-posting increases liquidity in early markets.

## Jobs To Be Done and Key Use Cases
- JTBD
  - As a host, I want to describe my session naturally and quickly get a structured, publishable listing.
  - As a player, I want to find games that fit my schedule, location/online preference, and skill level.
  - As any user, I want confidence the group is legit and expectations are clear.
- Key Use Cases
  1) Host creates session via free-text; system extracts fields and proposes clarifications.
  2) Players search/browse and filter by schedule, proximity/online, system/level, beginner-friendly.
  3) Schedule alignment: capture availability across participants and propose best slots.
  4) Messaging to coordinate last-mile details; roster confirmation with waitlist.
  5) Groups/communities: follow/subscription to hosts and stores; announcements.
  6) Cross-post to Reddit/Discord with canonical link and update sync.

## Scope
- In Scope (MVP): Profiles, session creation (free-text to structured), search/browse, availability capture and slot proposal, roster management/waitlist, basic messaging, calendar export (ICS/Google), cross-posting link generator, basic reporting/block.
- Out of Scope (MVP): In-app payments/escrow for pro GMs, advanced moderation, full marketplace fees, image generation, marketplace store for second-hand items.

## Success Metrics
- OMTM: Session Fill Rate within 14 days (% of posted sessions reaching target roster).
- Supporting KPIs: Time-to-fill (median), No-show rate %, First response latency, Profile completion rate, DAU/WAU, Report rate.
- Guardrails: Abuse reports per 1k users, spam detection events, opt-out rate from cross-post prompts.

## Solution Overview
Users describe sessions in free text. The system extracts structured fields (game/system, online/IRL, location, date/time windows, seats, experience level, safety tools) and proposes clarifications. A schedule alignment flow gathers availability and proposes top slots with calendar sync. Profiles provide trust signals (basic verification, reviews later). Cross-posting creates a mirrored post on external channels with a canonical session page.

## User Experience
- Flows:
  - Create session (free-text -> structured preview -> clarify -> publish -> cross-post).
  - Discover & join (search -> view -> apply -> confirm/waitlist).
  - Schedule alignment (availability -> proposed slots -> confirm -> calendar add).
- States: empty (no sessions), loading, errors (extraction low confidence), success banners.
- Content: chip suggestions, consent/verification copy, safety norms, report reasons.
- Accessibility: WCAG AA targets; keyboard navigation; labels for assistive tech; readable contrasts.

## Functional Requirements
- FR-1 (Must): Free-text input with field extraction and confidence scoring.
- FR-2 (Must): Structured listing preview with inline edit and clarification prompts.
- FR-3 (Must): Profiles with location, online/IRL preference, travel willingness.
- FR-4 (Must): Search/browse with filters (system, distance/online, schedule window, beginner-friendly).
- FR-5 (Must): Availability capture and slot proposal; host selects final time.
- FR-6 (Must): Roster management with waitlist and status updates.
- FR-7 (Must): Basic messaging (host <-> applicants/roster) with notifications.
- FR-8 (Must): Calendar export (ICS/Google) and reminders.
- FR-9 (Must): Reporting/blocking for abuse; basic moderation queue.
- FR-10 (Should): Cross-post link generator; webhook/template for Reddit/Discord posts.
- FR-11 (Could): Group/community pages with follow/announce.
- FR-12 (Could): Reviews/ratings for hosts after sessions.

## Non-Functional Requirements
- p95 page load < 2.5s; availability 99.5% during MVP; mobile-first responsive UI.
- Privacy by design; minimal PII; data retention defaults 12 months for inactive sessions.
- Localization-ready (copy externalized); time zone aware scheduling.

## Data Model and Integrations
- Entities: User, Profile, Group, Session, Application, AvailabilityWindow, Message, Report, Follow.
- Events: session_created, fields_extracted, application_submitted, slot_confirmed, calendar_exported, message_sent, report_submitted.
- Integrations: Calendar (Google ICS link), Maps/Geocoding for distance, optional Discord/Reddit posting via webhooks/templates.
- Storage/Retention: Sessions archived after end-date + 90 days; messages retained 180 days.

## Security, Privacy, and Compliance
- Threats: spam/scams, harassment, scraping. Mitigations: rate limits, basic verification, block/report, limited profile surface by default.
- Privacy: GDPR/CCPA aware; export/delete account; consent for notifications and cross-posting.
- Safety: Code of conduct surfaced; quick takedown workflow for reported sessions.

## Analytics and Instrumentation
- Funnel: free-text start -> structured preview -> publish -> first response -> roster full.
- Dashboards: OMTM (Fill Rate), TtF, response latency, extraction confidence distribution, report rate.
- Feature flags for extraction model versions and schedule alignment algorithms.

## Delivery Plan (Solo Operator + Lovable)
- Prototype core flows (session creation, discovery, availability) in Lovable to validate UX and copy; integrate minimal backend for persistence.
- Weekly cadence: build Mon–Thu, user validation Fri (5 testers via Discord/Meetup). Decision log per week.
- Graduate to production stack once Fill Rate and TtF targets are trending positively in pilot.

## MVP Plan and Phasing
- MVP (Month 1–2): FR-1..FR-9, minimal groups, Google Calendar export, geocoding, basic moderation.
- P1 (Month 3): Cross-posting templates, follow/announce, reviews (read-only).
- P2 (Month 4–5): Pro GM enhancements (payments integration), richer verification, recommendation engine.
- Rollout: Private beta (two cities + online) -> Public beta -> GA.

## Risks and Mitigations
- Liquidity cold-start: cross-posting and seeding via partner stores/Discords.
- Abuse/spam: rate limits, invite codes, and early moderation volunteers.
- Low extraction accuracy: confidence gates with human edits; chip suggestions.
- Scheduling complexity: constrain to proposed windows first; expand after signal.

## Operational Readiness
- Monitoring: uptime, error rate, extraction failures, report backlog. Alerts to email/Slack.
- Runbooks: incident response, abuse takedown, data export/delete.
- Rollback: feature flags and blue/green deploy for critical flows.

## Go-To-Market
- Positioning: “From chat to confirmed table in minutes.” Trust + scheduling as key wedge.
- Channels: Reddit/Discord communities, local game stores, Meetup groups.
- Launch checklist: city seeding, host outreach, content playbooks, feedback loop.

## Dependencies and Open Questions
- Dependencies: Maps/geocoding provider; calendar integration; optional Reddit/Discord hooks.
- Open Questions: Required verification for hosts at MVP? Which cities to seed first? Review model (stars vs. testimonials)?

## Appendix
- Source notes: `general research/gamerconnect/Game Group Finder`
- Related: `stencils/PRDFormat.md`, `stencils/OnePager.md`, `stencils/ExperimentPlan.md`
