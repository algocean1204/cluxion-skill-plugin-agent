# Apple interaction principles for the web

Load only the sections relevant to the current UI. These are implementation heuristics,
not a visual theme. Explicit requirements, exact references, repository truth, and
accessibility remain authoritative.

## Response and direct manipulation

- Show press feedback on pointer-down; do not wait for click release.
- During drag, sheet, slider, or carousel movement, update continuously with 1:1 tracking.
- Preserve the grab offset and use pointer capture so the object does not jump or detach.
- Track a short position/time history when release velocity affects the result.
- Use a small intent threshold before committing a direction; retain cancel and reversal.

## Interruptibility and continuity

- Keep motion interruptible. Never disable input merely because a transition is running.
- Retarget from the current on-screen value, not the stale logical destination.
- Preserve velocity across a reversal or gesture-to-animation handoff.
- Enter and exit along the same path and anchor a surface to its initiating control.
- Use independent axes when X and Y have meaningfully different velocities.

## Springs and momentum

- Prefer critically damped motion with no overshoot for ordinary state changes.
- Use momentum-only bounce: a restrained overshoot is eligible only after a real flick,
  throw, or drag release whose velocity should remain visible.
- Never bounce menu/modal entrances, automatic reveals, or decorative transitions.
- Project a release toward where the gesture is going before selecting a snap point.
- Use progressive resistance beyond a drag boundary instead of a hard frozen stop.

## Performance

- Prefer transform and opacity on the compositor path.
- Use requestAnimationFrame for pointer-driven work and avoid unnecessary input latency.
- Inspect fast or complex motion frame-by-frame when it feels discontinuous.
- Do not add a motion dependency for a simple transition the platform already handles.

## Materials and depth

- Use translucency only to explain hierarchy or preserve context beneath a floating layer.
- Avoid stacking translucent surfaces where contrast collapses.
- Match material weight and shadow to surface scale and background complexity.
- A modal may dim the background; a parallel non-blocking panel should preserve flow.
- Prefer a spatially anchored materialization over an arbitrary fade when origin matters.

## Typography and structure

- Start with `system-ui` unless the product identity requires another typeface.
- Tighten tracking and leading carefully as display size grows; keep body text legible.
- Scale layout with text using relative units and preserve user text-size preferences.
- Use order, spacing, contrast, and direct labels to make purpose and wayfinding obvious.
- Simplicity means fewer unnecessary decisions, not hiding necessary context.

## Accessibility alternatives

- Under `prefers-reduced-motion`, replace slides, parallax, and springs with short fades or
  static state changes while retaining status feedback.
- Under reduced transparency, increase surface opacity and remove blur.
- Under increased contrast, use near-solid surfaces and explicit contrasting boundaries.
- Maintain visible focus, keyboard equivalence, readable contrast, and adequate hit areas.
- Never make motion, sound, or haptics the only carrier of meaning.

## Review questions

1. Does feedback begin at the user's action and continue through it?
2. Can a moving control be grabbed, reversed, or cancelled without a jump?
3. Does the path explain where the surface came from and where it returns?
4. Is any bounce caused by real gesture momentum rather than decoration?
5. Does reduced-motion preserve meaning without the physical movement?
6. Did the implementation preserve the reference and repository design system?
