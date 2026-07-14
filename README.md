# Cluxion Skills and Plugins

Public source-only backup of Cluxion's personal agent skills and plugins. All discovery and repository names use the `clx-` prefix. Build artifacts, virtual environments, caches, credentials, and runtime sessions are excluded.

## Skills

| Skill | Purpose |
|---|---|
| `clx-apple-design` | Applies Apple-first interaction, motion, material, and typography foundations to substantial UI work. |
| `clx-playwright` | Automates real-browser navigation, interaction, screenshots, and UI-flow verification. |
| `clx-claude-config` | Maintains Claude Code rules, guides, skills, plugins, hooks, and settings. |
| `clx-codex-config` | Maintains Codex rules, guides, skills, plugins, hooks, and configuration. |
| `clx-session-intent` | Keeps one short, session-owned objective and objective completion criteria. |
| `clx-bracket-payload` | Distinguishes bracketed actionable payloads from surrounding context. |
| `clx-concise-report` | Produces outcome-first, evidence-based reports with strict length limits. |
| `clx-report-policy` | Decides when a report should be a file and prevents report-file clutter. |
| `clx-dataset-work` | Runs disk-aware dataset preparation, validation, conversion, and Hub workflows. |
| `clx-figma-workflow` | Routes Figma inspection, implementation, and verification work. |
| `clx-theme-factory` | Supplies reusable color and typography themes for design-token work. |
| `clx-unslop` | Removes repetitive AI-writing patterns before publication. |
| `clx-vercel-web-design-guidelines` | Audits interfaces against Vercel's published web-interface guidelines. |
| `clx-frontend-design` | Establishes an intentional initial visual direction for new interfaces. |
| `clx-canvas-design` | Creates original static poster, print, cover, PNG, and PDF compositions with an offline-first workflow. |
| `clx-color-expert` | Handles explicit OKLCH/OKLab, gamut, contrast, WCAG/APCA, and color-system analysis. |
| `clx-immersive-web` | Routes named 3D/WebGL/advanced-motion work to one local technology reference at a time. |
| `clx-algorithmic-art` | Creates seeded art with local p5.js runtime/source files and a dependency-free Canvas fallback. |
| `clx-hand-drawn-diagrams` | Creates editable local Excalidraw diagrams without requiring hosted URLs or global browser setup. |
| `clx-grill-me` | Elicits missing requirements and pressure-tests important decisions. |
| `clx-anti-hallucination` | Preserves context integrity in long or compacted sessions. |
| `clx-modular-architecture-design` | Produces evidence-gated modular architecture and pipeline specifications. |

## Plugins

| Plugin | Discovery skill | Purpose |
|---|---|---|
| `clx-preprocessing` | `clx-preprocess` | Clarifies requests and provides bounded queue, loop, and runtime contracts. |
| `clx-supercoder` | `clx-supercoder` | Applies hash-verified patches with syntax, lint, test, and stale-write gates. |
| `clx-autoclearmemory` | `clx-forgetforge` | Stores, retrieves, archives, and prunes agent memory with bounded lifecycle rules. |
| `clx-ultracode` | `clx-ultracode` | Runs bounded multi-agent adversarial debate and reports consensus or `no_consensus`. |
| `clx-hermes-call` | `clx-hermes-call` | Provides a bounded, cleanup-aware CLI bridge to Hermes agent sessions. |
| `clx-grok-call` | `clx-grok-call` | Provides a bounded one-shot Grok 4.5 CLI for token-efficient delegated analysis. |

## Layout

```text
skills/clx-*/
plugins/clx-*/
```

Each asset keeps its own README, manifest, tests, and installation instructions where applicable. The private environment backup, including local host configuration, lives separately in `agents-setting-back-up`.

## Apple-first AoE design routing

Design guidance is lazy-loaded: unresolved UI behavior uses `clx-apple-design`, then at most one aesthetic specialist (`clx-frontend-design` for new UI or upstream `impeccable` for existing UI), followed by an evidence tool only when needed. Exact references skip aesthetic invention. Static art, generative art, diagrams, color science, and immersive-web helpers activate only for their explicit media or technical trigger. No separate dispatcher or always-loaded design catalog is installed.

`design-sources.lock.json` records upstream commits, digests, licenses, and offline boundaries. Figma editing still requires an explicitly connected MCP session; immersive runtime packages must already exist in the project; hosted diagram URLs remain optional. The bundled guidance and local artifact paths work without network access.
