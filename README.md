# Maya - AI-Powered Bar Management

**An open experiment in automating the business side of running a bar, so the human side gets more room to breathe.**

Built on [OpenClaw](https://openclaw.org) · Orchestrated with [Hermes](https://hermes.org) · Developed with [Claude Code](https://claude.ai/code)

---

## What This Is

Maya is a research project exploring how much of bar management can be automated using AI agents, CLI tools, and lightweight integrations - without losing the soul of the place.

This isn't about replacing bartenders with robots. It's about taking the spreadsheets, vendor emails, scheduling headaches, inventory counts, and compliance paperwork off the bar owner's plate so they can focus on what actually matters: the room, the people, the craft.

## Building in Public

This project is built in public. Every configuration, every skill, every integration - it's all here.

We believe the best way to prove that AI can help traditional businesses is to show the work. No black boxes. No proprietary lock-in. Just tools that work, documented openly so anyone running a bar, a restaurant, or a small business can learn from it, fork it, and make it their own.

## Prior Art - We've Done This Before

This isn't our first time bringing AI tooling to real-world operations. Maya builds on lessons learned from:

- **A Vending Machine** - automated inventory tracking, restocking alerts, and sales pattern analysis for an unmanned retail unit
- **A Travel Manager** - booking coordination, itinerary optimization, and expense tracking powered by AI agents
- **Personal AI Assistants** - daily workflow automation, communication management, and decision support for individuals

Each of these taught us something about what works and what doesn't when AI meets the physical world. Maya takes those lessons to a more complex domain: a business with staff, regulars, vendors, compliance requirements, and a neighborhood to be part of.

## Why a Bar

Bars are one of the oldest businesses in the world. They're also one of the least "disrupted" - for good reason. The product is human connection. You can't optimize that.

But you *can* optimize the back-of-house work that eats up an owner's time and energy. Ordering, scheduling, inventory, bookkeeping, vendor management, compliance - these are systems problems, and systems problems are where AI shines.

We care about bringing this technology to traditional businesses. Not to modernize them. To free them up to stay exactly what they are.

## Architecture

```
Maya/
├── config/
│   ├── openclaw/       # OpenClaw agent configuration
│   ├── hermes/         # Hermes orchestration config
│   └── claude-code/    # Claude Code project settings
├── docs/
│   ├── menu/           # Current menu and drink recipes
│   ├── inventory/      # Beer, wine, spirits tracking
│   ├── permits/        # Licenses and compliance docs
│   ├── seating.md      # Room layout and capacity
│   └── calendar.md     # Special dates that affect the bar
├── skills/             # Callable skills (CLI & agent-invocable)
├── AGENTS.md           # How Maya operates
├── DREAMS.md           # Where Maya is headed
├── SOUL.md             # Who Maya is
└── CLAUDE.md           # Claude Code project instructions
```

## Tools

| Tool | Role |
|------|------|
| **OpenClaw** | Agent framework - defines Maya's capabilities, personality, and decision-making |
| **Hermes** | Orchestration - routes tasks between agents, services, and the real world |
| **Claude Code** | Development - builds, tests, and iterates on skills and integrations from the CLI |

## Integrations

Integrations will be added as they're tested and proven in the bar. No names until they earn their place.

## Skills

Skills are self-contained, callable units of work. They're designed to run on a Mac Mini behind the bar, invocable via CLI or through agent orchestration.

```bash
# Examples of what a skill call looks like
maya inventory check
maya schedule next-week
maya vendor order --supplier=wine-distributor
maya close-out tonight
```

See [skills/](skills/) for the full catalog.

## Getting Started

### Prerequisites

- macOS (tested on Mac Mini)
- [OpenClaw](https://openclaw.org) installed
- [Hermes](https://hermes.org) installed
- [Claude Code](https://claude.ai/code) CLI

### Setup

```bash
git clone https://github.com/cvander/Maya.git
cd Maya

# Configure OpenClaw agent
cp config/openclaw/config.example.yaml config/openclaw/config.yaml

# Configure Hermes orchestration
cp config/hermes/config.example.yaml config/hermes/config.yaml

# Configure Claude Code
# CLAUDE.md is already in the repo root
```

## Contributing

This is a public research project. If you're running a bar, a restaurant, or any traditional business and want to explore what AI can do for your operations - we want to hear from you.

Open an issue, submit a PR, or just watch and learn. That's the whole point of building in public.

## License

MIT - see [LICENSE](LICENSE) for details.

Use it, fork it, make it yours. If you build something cool with it, let us know.
