# CLAUDE.md - Project Instructions for Claude Code

## Project Context

Maya is an AI-powered bar management system built on OpenClaw, orchestrated with Hermes, and developed with Claude Code. This is a public research project exploring automation for traditional businesses.

## Key Files

- `AGENTS.md` - How Maya operates (operational rules, voice, boundaries)
- `DREAMS.md` - Where Maya is headed (direction, not roadmap)
- `SOUL.md` - Who Maya is (identity, personality)
- `config/` - Tool configurations (OpenClaw, Hermes, Claude Code)
- `skills/` - Callable automation skills

## Rules

- Read `AGENTS.md` before making operational decisions - it defines hard stops and red lines
- Maya is tech-forward but selective. She's from Silicon Valley. Suggest tools when they solve real problems.
- No branding, franchising, or scaling suggestions
- Maya's voice is direct, warm, short sentences. No corporate filler.
- Privacy is paramount - regulars' personal information stays in context, never exported
- `trash` > `rm` - move files, don't delete them
- Skills should be CLI-invocable and Mac Mini compatible
- All integrations should fail gracefully - the bar runs with or without them

## Development Patterns

- Skills are self-contained scripts in `skills/`
- Configs use YAML for OpenClaw and Hermes, JSON for Claude Code settings
- Keep dependencies minimal - this runs on a Mac Mini behind a bar
- Test locally before pushing - no CI/CD surprises
- Write for clarity, not cleverness

## Integrations

Integrations are added as they're tested. Keep credentials in environment variables, never in config files.

## Tone

When writing anything Maya would send - vendor emails, staff notes, booking replies - match her voice from `AGENTS.md`. Short. Direct. Human.
