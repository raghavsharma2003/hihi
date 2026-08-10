# Project notes for Claude

## Agent/model policy (user preference)
Delegate simple, mechanical, or standard subtasks (web collection, data
extraction, QA sampling, formatting, bulk file edits) to **Sonnet** subagents
(`model: 'sonnet'`) instead of Fable/Opus — don't spend Fable limits on work
Sonnet can do. Keep the stronger model only for orchestration, architecture,
scoring/design decisions, and final verification.

## Project
NCR battery-as-a-service lead scraper (see README.md). Two ICPs: commercial
sites and housing societies in high-outage corridors. Hard rules:
- Never fabricate lead data; every row needs real `source_urls`; unknown
  fields stay blank.
- Respect robots.txt (ncr_leads/robots.py gates every fetch); no login-walled
  scraping.
- `python -m ncr_leads.pipeline` regenerates data/output/ from data/raw/.
