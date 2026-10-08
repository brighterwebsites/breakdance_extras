---
name: breakdance-style-conventions
description: Vanessa's personal conventions for naming CSS selectors and design-token variables, structuring reusable styles, and handling images/fonts on Breakdance builds. Consult before creating new selectors, global variables, hero sections, or background images — including greenfield builds, even if naming wasn't asked about. Living document: append new preferences here as Vanessa states them, don't wait for a rewrite.
---

# Breakdance Style & Build Conventions

Personal build conventions for Breakdance sites, applied consistently without Vanessa having to restate them each time. This file is expected to grow: when she gives a new rule in conversation, append it to the relevant section (or add a section) rather than waiting for a full rewrite.

Canonical copy: https://github.com/brighterwebsites/breakdance_extras/blob/main/breakdance-style-conventions/SKILL.md. Edit there; other copies are mirrors.

## 1. Selector naming & prefixing

**One prefix per site**, applied only to semantic/component classes — anything naming a section or component specific to this site's content (`gs_hero`, `gs_hero-title`, `gs_card`). Get the prefix from `site-info`/`get-css-selectors` (`css_prefix`) rather than inventing one — matches Breakdance's own convention. The site prefix is for **selectors**; design-token variables follow §10 instead.

**Utility classes stay unprefixed.** Small, single-purpose classes not tied to this site's content (`.right` = align-self: right, `.bg-dark-10` = background 10% darker, may also lift paired text colour) skip the prefix. Test: would this exact class do the same job unchanged on a completely different site? Yes → utility, no prefix. No, because it names something specific to this site's content or structure → semantic, prefix it.

**Why:** the prefix doubles as a workflow signal. Experiment freely with unprefixed classes while building; prefix only what's kept. Anything still unprefixed at cleanup time is safe to delete — don't prefix speculative classes early, it kills the signal.

**Sub-elements:** BEM double-underscore for compound names once a component has more than one part — `gs_project__wrapper`, `gs_project__card`, `gs_project__overlay`. Don't mix in hyphens or camelCase for the same relationship.

**Don't repurpose the prefix for migration/build status.** One prefix per site, permanently. To track what's been touched during a rebuild or platform upgrade, use Breakdance's selector folders/organisation — not an interim variant prefix (`xx_`). Names encode what a selector *is*; migration status is a filing concern.

**Fleet exception — one prefix across a set of near-identical sites.** "One prefix per site" assumes the sites are independent builds. When a group of sites is deliberately *the same* build — same structure and design system, differing only in minor colour / font-size / spacing values — give the whole fleet a single shared prefix instead of one each. A shared prefix means a component authored on one site drops into the others unchanged, which is the entire point when the design is common.

First case: the six **Cube** sites (`cubepersonalloans`, `cubeconnect`, `cubeconveyancing`, `cubehealthinsurance`, `cubecentral`, `cubebusinessloans`) all use **`cu-`**, set 2026-09-20, replacing per-site `cbl-` / `cc-` / `chi-`. Per-site prefixing had already produced a silent collision — `cubecentral` and `cubeconveyancing` were *both* `cc-` — which is the tell that the per-site model was wrong for this group.

**Before changing an existing site's prefix, check `get-css-selectors` for selectors still carrying the old one.** Setting `css_prefix` records a convention; it does **not** rename anything, so changing it on a site with existing prefixed selectors orphans them. (All four Cube sites had zero registered selectors, so the switch was free.) To set the prefix without importing any CSS, pass a comment-only stylesheet — `insert-stylesheet` with `/* … */` and `css_prefix` creates nothing and returns the new prefix.

**`insert-stylesheet`'s `css_prefix` argument normalizes to kebab-case** regardless of what you pass (passing `gs_` is echoed back and stored as `gs-` by `get-css-selectors`/`site-info`). The class names you type in the stylesheet are unaffected — `.gs_fontsize_001` is created exactly as written. If a site's established convention uses underscores (check existing selectors, not the `css_prefix` field), keep typing that literally and don't trust the echoed prefix as the source of truth.

## 2. Reuse before creating page-scoped selectors

Before adding a page-scoped selector (`gs_home-hero`), check whether the same pattern exists elsewhere and reuse the general one (`gs_hero`). Only go page-specific when that page's version is actually different — not by default.

## 3. Background images — never `background-image`

Hero and section background images are always an image element (§25), never CSS `background-image`, so that:
- `fetchpriority` and `decoding` (sync/async) can be set appropriately
- lazy loading is explicitly turned **off** in the element's design settings for above-the-fold/hero images

Hard rule, no exceptions.

## 4. Hero fonts — max 2 font files

Max 2 font **files** per hero section, so every hero font can be preloaded. Count files, not weights:
- A **static** font ships one file per weight, so each weight counts (Barlow Condensed Bold + Inter Regular = 2 files).
- A **variable** font ships one file covering its whole weight range (e.g. Nata Sans 100–900), so any number of its weights counts as 1.

Check which kind each font is before counting. Don't add a third file even for a small touch.

*Updated 2026-10-08 (was "max 2 styles, weight counts as a style"): the cap exists for preloading, and a variable font's weights cost no extra preload.*

## 5. Third-party/infrastructure classes — leave untouched

Classes written by a plugin for its own tracking/function — Google Analytics data-attribute selectors and `ga-*` prefixed selectors, LiteSpeed Cache's lazy-load-control classes, etc. — are a separate category. Don't rename them, fold them into the site prefix, or reclassify them as utilities; leave exactly as found. If unsure whether something's plugin-native vs. design-system, ask — they can look like genuine one-off utilities at a glance.

## 6. Extend scales, don't fork them

If a size/spacing/weight scale already exists on one mechanism (e.g. a numbered `clamp()` set) and a new value is needed at either end, add the next step the same way. Don't patch the gap with a parallel mechanism (a fixed-px class sitting under a clamp scale). One scale, one mechanism, extended as needed.

## 7. Retire workarounds once a native option exists

Some classes exist only because a cleaner native mechanism wasn't known/available at the time (e.g. per-child "span N columns" utilities, built before realising the grid's own column-template setting on the parent does the job). When rebuilding and you spot one, retire it for the native mechanism rather than preserving or relabelling it as a utility. Ask if unsure whether something's a genuine utility or a superseded workaround.

## 8. Agency-shared components — their own prefix

Components built once and reused across multiple client sites get the agency prefix `bw-`. Three naming tiers: site prefix = this site's content/structure; `bw-` = shared agency component library; no prefix = generic single-purpose utility usable anywhere. `bw-` components consume only the standard semantic tokens (§10), which is what lets them drop onto any site unchanged.

**Brighter Websites' own site** (brighterwebsites.com.au) uses `bws_` as its site prefix, so its site-specific selectors never blur with the shared `bw-` tier. Set 2026-10-08; older `bw-`/`bw_` selectors on that site are being retired page by page into a "BWS" selector collection.

## 9. Elements — prefer Fundamentals; handle mixed-content sites

**Prefer Fundamental elements** (F-Text, F-Text Link and the rest of the Fundamental set) over the standard Essential/basic elements wherever a Fundamental can do the job. They output cleaner markup, which is easier for AI to work with, and the MCP's element lookups miss some basic standard blocks. Don't recommend switching away from Fundamentals to dodge a builder bug; work around the bug instead (e.g. the `-t` pointer variables in §10) and expect Breakdance to fix it.

### Mixed-content sites — basic vs fundamental elements

Breakdance 3.x has two element families, and sites built before or across the betas usually contain both.
- **Fundamentals** render with a `bde-f-` class (`bde-f-container`, `bde-f-text`, `bde-f-image`). They ship **no default CSS**: what you write is what renders.
- **Basic elements** render with a plain `bde-` class (`bde-div`, `bde-text`, `bde-column`, `bde-section`). They ship **hidden base CSS** that does not appear in the element's design panel or its custom CSS field.

The one that causes most of the trouble:

```css
.bde-div { display:flex; flex-direction:column; align-items:flex-start; text-align:left; max-width:100%; position:relative; background-size:cover; }
```

So a class that only sets `display:flex` on a basic Div still lays out as a column, its children shrink to content width, and `justify-content: space-between` appears to do nothing. (This is the "flex defaults to column" behaviour seen on earlier builds: it's the basic element's hidden CSS, not browser behaviour. Verify rendered output with `preview-post`/`preview-element` rather than assuming either way.)

**How to tell which family an element belongs to:** check the rendered class (`bde-f-` or `bde-`). In the element tree, fundamentals usually hold registered selectors (by ID). Older basic elements often hold loose class strings, and some of those are not registered selectors at all.

**Before styling — check**
1. **Read the hidden defaults.** Render the post or template with its CSS included, then read `element_default_css` for every basic element type you are about to style.
   - As of beta 9, the per-element CSS lookup returns Div, Text, Image, RichText and TextLink as "missing" (bug reported), so don't rely on it for those.
   - Custom elements (Brighter BD Elements) and other built-ins return correctly.
2. **Check every class you will touch.** Is it a registered selector? Is it used anywhere else on the site?
   - If a class is unregistered, scope a nested rule under a registered parent. Don't register a new global class just to style it.
   - **Before reusing an existing class on a new or rebuilt element, expand it and inspect its nested children** (`& > div`, `& > div:first-child` and so on), not just its own properties. Nested rules don't show on the element, and they reapply the old structure's layout to whatever the new element contains. On early-beta sites, assume a reused class carries baggage until you've checked.
3. **Read existing selector properties back before changing them.** Importing a selector replaces its properties; it does not merge.

**While styling — declare, don't inherit.** Any class applied to a basic element must restate every layout property the element's defaults set: `display`, `flex-direction`, `align-items` and `width` (plus `justify-content` where it matters). Never write `display:flex` on its own against a basic Div. The explicit declarations win whatever the element type, so the rule still holds if the wrapper is later swapped to a fundamental.

**After styling — verify**
1. Read the selectors back. The import should report no dropped properties, other than ones you removed on purpose.
2. Check the result visually against a real record. For templates, render with a real product or post as context.
3. Purge LiteSpeed before judging the frontend.

**When to swap or rebuild instead of restyling**

| Situation | Approach |
| --- | --- |
| Restyling a block that works structurally | Keep the basic elements and apply "declare, don't inherit". Lowest-risk option on live sites and the default. |
| Restructuring that block anyway, or fighting the basic wrapper's defaults on more than a few properties | Swap the wrapper to a fundamental Container, move the children into it, and give it a fresh role-named class. Reuse an existing class only if fundamentals already use it. |
| The section is being redesigned, not just restyled | Rebuild it from fundamentals, and delete the old section in the same pass. |

**Naming — don't encode the element family.** No family-specific prefixes such as `cns_f_` or `cns_b_`. Same reasoning as §1: a name says what a selector *is*, not how it is currently built. The family is already visible in the rendered class, a family prefix becomes wrong the moment a wrapper is swapped, and migration progress belongs in selector collections or folders.

*Origin: CNS single-product template, Oct 2026. The price block and specs box were shrinking and stacking because of the `.bde-div` defaults. Fixed with explicit layout declarations; no rebuild was needed.*

## 10. Design tokens

### Variables are the single source of truth

**Every token is a registered global variable.** Colours, spacing, radius, type sizes, weights, line heights, letter spacing, shadows, motion and font families live in Global Settings > Variables, so they can be picked in the builder. Register them with `insert-css-variables` (or a `:root` block passed to `insert-stylesheet`, which registers Variables); check what exists with `get-css-variables`. Reference with `var()` — never redefine a value inline once it's a token.

**Colours are Variables, not the Global Colours palette.** The 3.0 selector colour picker doesn't expose `colors.palette` swatches, only registered variables. Register every colour as a colour variable. On existing sites, move palette colours into Variables (same names and values), then empty the palette once everything is migrated. The palette is likely to be deprecated: once its colours are removed, new colours can't be added to it in the builder. Where `set-global-settings` needs a colour (`colors.background/text/headings/links`, button backgrounds), point it at `var(--c-…)`, not a raw hex. Don't populate the big palette swatch array — that's exactly what turned into "rebuilt a number of times, lots of CSS bloat" on Guerilla Steel (2026-08-16).

**Keep the global stylesheet as empty as possible.** Don't define tokens in a `:root {}` block in Global Settings > Code, and don't load fonts with `@import`: registering a font as a font-family variable makes Breakdance load it. Move any remaining global CSS (base element styles, form and button styling) into global selectors, so it's visible and editable in the selector panel. Leave only what can't live anywhere else, such as `@keyframes`.

### Link variables, never type them into design inputs

**Never type `var(--x)` into a builder design-setting input** (a size, colour, spacing or weight field on an element or selector). Pick the variable from the input's variable picker instead.
- **Why:** a picked variable is stored by ID (`{var-<uuid>}`), so renaming the variable updates every place it's used. A typed `var(--x)` is plain text: rename the variable and that link silently breaks.
- **Exceptions, only when absolutely necessary:** a control with no variable picker, or a custom CSS block (gradients, multi-value shorthands). Keep these to a minimum.
- **AI/MCP work:** `insert-stylesheet` and `html-to-page` store `var(--name)` of a *registered* variable as a linked ID, so authoring through them is safe. Verify by reading the selector back (`get-css-selectors`, `include_properties`) and checking for `{var-…}`. Element `design` properties set with `edit-post` take the same `{var-<uuid>}` form.
- **Gradients are the trap:** `insert-stylesheet` parses `background: linear-gradient(… var(--x) …)` into the gradient control with the `var()` typed inside it. Use a linked solid colour (plus opacity if needed), or accept it as a documented custom-CSS exception.
- **When one is found:** flag it to Vanessa to fix or approve. Don't leave it silently.

### Naming standard — type prefix, then name

Tokens get a short **type prefix**, not the site prefix. The site prefix (§1) is for selectors only.

| Prefix | Holds | Examples |
|---|---|---|
| `--c-` | semantic colour — a role, see §11 | `--c-primary`, `--c-on-primary`, `--c-surface-alt`, `--c-primary-hover` |
| `--fs-` | font size | `--fs-sm`, `--fs-base`, `--fs-lg`, `--fs-h1` |
| `--sp-` | spacing: padding, margin, gap | `--sp-xs` … `--sp-2xl`, `--sp-section` |
| `--rad-` | border radius | `--rad-sm`, `--rad-md`, `--rad-pill` |
| `--ff-` | font family | `--ff-heading`, `--ff-body` |
| `--fw-` | font weight | `--fw-regular`, `--fw-semibold`, `--fw-bold` |
| `--lh-` | line height | `--lh-tight`, `--lh-body` |
| `--ls-` | letter spacing | `--ls-tight`, `--ls-caps` |
| `--sh-` | box shadow | `--sh-card`, `--sh-raised` |
| `--dur-` / `--ease-` | motion | `--dur-fast`, `--ease-out` |
| `--_` | **primitive** — a raw value, never applied | `--_orange-600`, `--_space-4`, `--_size-18` |

- **Step names:** t-shirt sizes (`2xs xs sm md lg xl 2xl 3xl`) for `fs`/`sp`/`rad` scales, or a role name when a value is tied to a job (`--fs-h1`, `--sp-section`). A scale uses one scheme, extended per §6.
- **Gaps are spacing.** No separate `--gap-` family; a layout gap uses `--sp-`.
- **Superseded names** (old agency table: `--text-*`, `--space-*`, `--radius-*`, `--gap-*`, `--transition-*`) are not used on new builds.

### Apply only semantic tokens; never `--_` primitives

Elements, selectors, global settings and component CSS reference **only semantic tokens** (`--c-`, `--fs-`, `--sp-`, `--rad-` and the rest of the table). A `--_` primitive appears in exactly one place: as the *value* of a semantic token (`--c-primary: var(--_orange-600)`). If you find yourself typing `var(--_` anywhere else, stop and use or create the semantic token instead.

**Why this gives about 90% of scoping's value.** Site-prefixing every token was buying two things: changing a value in one place, and keeping this site's design system from colliding with anything else. The semantic layer already gives the first: it is the only interface, so remapping a role or changing a primitive touches one variable, and the leading underscore marks primitives as private. Unprefixed semantic names add something scoping couldn't: a `bw-` component or a fleet component drops onto any site and picks up that site's values with no renaming. The ~10% given up is collision protection against third-party CSS that happens to use the same generic names. Breakdance's own variables are `--bde-*` and WordPress's are `--wp--preset--*`, so neither clashes; before registering on a site, check `get-css-variables` and the rendered CSS for plugin variables already using `--c-`/`--fs-`/`--sp-`/`--rad-`.

**Primitives are optional.** Create a `--_` primitive only when one raw value feeds more than one semantic token, or a scale is generated from a base value. Otherwise the semantic token holds the value directly (`--c-primary: #e8541f`) — no tier for its own sake. Register primitives in their own collection, "Primitives (don't apply)", so they're visible in the picker but plainly off-limits. Primitive names may describe the value (`--_orange-600`, `--_space-4`) — that's their job; §11's no-hue rule governs everything else.

**Verify on first use per site** that the relevant Breakdance variable type accepts `var(--_x)` as its value. The `-t` pattern below proves it for text variables; colour, number and size types are not yet confirmed. If a type won't take a `var()` value, that token stays single-tier.

### Variable-type mismatch workaround (`-t` pointer variables)

Some builder controls only list one variable type: F-Text's font-weight control takes text (T) variables while F-Text Link's takes number (#) variables, even though both are the same CSS property. Until Breakdance fixes it:
- The `#` variable is the single source of truth and holds the value (`--fw-semibold: 600`).
- A matching text variable with a `-t` suffix holds only a pointer to it (`--fw-semibold-t: var(--fw-semibold)`), kept in a separate "(T aliases)" collection.
- Never put a value in a `-t` variable; only ever change the `#` one.
- Use the same pattern, suffix and collection anywhere else the mismatch shows up. When Breakdance fixes it, delete the aliases collection.

### Existing sites and intake

- **Sites already built with site-prefixed tokens** (`--cns-…`, `--gs-…`, `--pfs-…`) keep them. Don't rename tokens that elements already reference just for tidiness — on Guerilla Steel (2026-08-17), renaming ~15 tokens plus every reference across the CSS and mockup HTML was pure mechanical risk with no functional upside. Consistency *within* a site matters more than cross-site uniformity.
- **New builds and full rebuilds use this standard.** That includes claude-design intake (§14): map the intake's token names to the standard at registration time, before any element references them — renaming then is free.

## 11. Colour naming — semantic only

**Name colours by the job they do, never by what they look like.** A colour token's name must stay true if its value changes. `--c-primary` survives a rebrand from orange to teal; `--c-orange` becomes a lie the moment it changes. So no hue or shade words in semantic colour names: no `blue`, `orange`, `sand`, `charcoal`, `navy`, `forest`, and no numbered shade scales (`-100`…`-900`). Those belong only in `--_` primitives (§10), which are never applied.

**Semantic tier always, primitive tier only when it earns its place.** The default is one tier: the semantic token holds the value (`--c-primary: #e8541f`). Add a `--_` colour primitive only when one raw colour genuinely feeds several roles. Don't build a full raw palette underneath by habit — it doubles the variable count for no gain on a small-business site.

**Pattern:** `--c-{role}` with an optional `-{variant}` for state or strength.

Core roles (use these names; add only what the site actually needs):
- `primary` — main brand colour (buttons, key links, brand moments)
- `on-primary` — text/icons sitting on `primary`
- `accent` — secondary highlight (badges, small emphasis, hover moments)
- `on-accent` — text/icons sitting on `accent`
- `text` — body text
- `text-muted` — secondary text, captions, meta
- `heading` — only if headings differ from `text`
- `bg` — page background
- `surface` — cards, panels sitting on `bg`
- `surface-alt` — alternating section band
- `inverse-bg` / `on-inverse` — dark (or contrasting) sections and the text on them
- `border` — dividers, input borders
- `success`, `warning`, `error` — form and status feedback, when needed

Variants describe state or strength, not lightness: `primary-hover`, `primary-soft` (tint used for backgrounds), `primary-strong`. Each variant is its own token.

**Same rule for utility classes.** A colour utility references the role, not the hue: `.bg-surface-alt`, `.text-muted` — not `.bg-beige`, `.text-grey`. (Lightness modifiers like `.bg-dark-10` from §1 are fine; they describe an adjustment, not a hue.)

## 12. Breakpoints — optimise down to 350px

Active mobile users typically sit at 393px down to 375px. Optimise layouts down to 350px, and add a custom 350px breakpoint below Phone Portrait (479px) on new sites and rebuilds.

## 13. Editing safety

**Deleting a selector strips its class from every element.** Breakdance stores an element's classes as selector IDs, so deleting a selector that is in use removes that class from every element using it. Never delete a selector that is used on any element. To retire a duplicate or generic class that's in use, rename it within its component's rename pass, so the elements are updated in the same edit.

**Reload the builder before editing after an AI change.** The builder saves its whole in-memory copy of selectors and variables, so a tab opened before an AI or MCP change can overwrite that change on save. Refresh the builder before testing or editing whenever changes have been made outside it.

**Snapshot before bulk changes.** Before deleting or bulk-editing selectors or variables, export the raw Breakdance options (selectors, variables, collections, global settings) to a JSON file outside the web root, so a single option can be restored without a full database restore.

**Purge after writes.** After any write that changes CSS output, purge the LiteSpeed cache so the live site picks up the regenerated Breakdance CSS.

## 14. Claude design system intake

Site rebuilds increasingly start from a "claude design" folder — design work produced in a separate Claude session/project (claude.ai or another Claude Code project) with no access to the Breakdance environment, MCP tools, or these skills. Treat its output as design intent to translate, not implementation instructions to execute literally.

**Rules:**
- **These conventions win on conflict.** If a claude-design directive contradicts a rule in this skill, or would make the Breakdance implementation meaningfully more complex for no real benefit, don't follow it blindly — rethink the approach, or ask Vanessa. Token names are the common case: map them to §10's standard on intake.
- **If a website-level project rule conflicts with a claude-design file, ask** — don't silently pick a side.
- **The folder arrives with its full design history, not just the final answer.** Iteration rounds, abandoned variations and scratch work usually sit alongside the current deliverable. First task is always to work out what's canonical vs superseded — check what the mockup pages actually reference (unreferenced folders/files are a strong signal of superseded work); don't assume the newest-looking or largest files are current. Vanessa will usually point at the right starting point; treat that as a strong signal, but still verify.

**Three intake shapes**, roughly in increasing completeness:
1. **Design system only** — `tokens.css`-equivalent + usually a markdown doc + often a mockup site. May arrive as React-like components rather than plain HTML unless it's been packaged/bundled.
2. **Mockup only** — pages or a full site (React or bundled/standalone HTML), no separate formal token file.
3. **Both** — a mockup *and* a project-level design-system/token file. Richest case: build the token/component CSS layer from the design-system file, then convert the mockup pages via `html-to-page`, reusing those classes rather than inventing new ones per page.

Confirmed on Guerilla Steel (2026-08-17): the design-system file was already written with Breakdance-adjacent conventions in mind (real `<img>` never `background-image`, max-2-fonts-per-hero, semantic role-based colour naming) — so alignment issues aren't guaranteed, but always verify.

## 15. Never hand-write internal Breakdance property JSON — author as CSS and let it parse

Global CSS selector properties (the `breakpoint_base.layout/size/spacing/...` shape returned by `get-css-selectors`) and element `design` blocks are Breakdance's internal representation, not a documented format to author directly. Guessing key names by pattern-matching neighbouring properties (e.g. inventing `grid.simple_grid_template_columns` / `grid_auto_flow` instead of the real `grid.enable_advanced_mode` + sibling `grid_template_columns` array) produces a selector that looks schema-plausible but is wrong. The compiler silently drops what it doesn't recognise (class applies, no visible styling) and can throw on save.

**Rule:** author global selector CSS through `insert-stylesheet` (plain CSS — let Breakdance's parser build the internal shape), never by constructing the `properties` object by hand. For element `design` properties, always call `get-element-schemas` first and match its shape exactly — don't infer one property's shape from how a *different* property looks.

**Why it matters even when the save "succeeds":** the malformed shape still gets written to the DB (that internal format isn't schema-enforced the way `edit-post` enforces element content/settings), so the bad selector sits there quietly not rendering. Confirmed on Guerilla Steel Stables (2026-08-17): `gs_singlehead__inner`'s grid properties used invented keys matching none of the site's other 200+ selectors; fixed by rewriting it as plain CSS via `insert-stylesheet` against the same selector id.

## 16. A visible "Array to string conversion" 500 on save doesn't mean the save failed — verify before assuming data loss

`breakdance_save` (native builder save, `admin-ajax.php`) throwing `Ajax Handler Error: ... Array to string conversion ... in ".../plugin/ajax/api.php"` on a specific compiled-template hash/line can happen *after* the database write already succeeded — the crash is in building the response, not the write. Confirmed twice on Guerilla Steel Stables (2026-08-17), different templates (single-post, archive), same signature: both times `get-post-tree`/`get-css-selectors` showed the edit persisted exactly as sent, and `preview-post` (with `include_css`) rendered it correctly.

**Don't panic-resave or assume corruption.** Check before doing anything destructive like restoring a backup:
1. `get-post-tree` / `get-css-selectors` (with `include_properties`) — did the edit persist?
2. `preview-post` with `include_css` — does it render and compile without error now?
3. If both are clean, diff what you just touched against §15's pattern (an invented/malformed property shape) or against `get-element-schemas` for the element involved.
4. Only if the shape genuinely validates and still throws is it worth treating as a Breakdance bug — and even then, reproduce it via an actual builder-UI action before reporting, since properties set through `edit-post`/raw stylesheets can create schema-valid combinations a human clicking through the UI would never produce. Don't file speculative reports on a single MCP-driven repro (the 1% rule — Vanessa doesn't want to be the account that reports every non-bug).

**Where to find the trace (confirmed 2026-08-18, 3.0.0-beta.4):** don't bother with `WP_DEBUG_LOG` — Breakdance runs its own `set_exception_handler()` (bundled Whoops, `error-reporter/error-reporter-ajax-handler.php`) that intercepts the exception before PHP's native logging, so nothing lands in `debug.log`. That handler puts a full stack trace with per-frame snippets straight into the failing AJAX response as `error.trace` (file, line, function, class); the toast/console text is just `error.message`. Capture the *full* response body (Network tab, Query Monitor's AJAX panel, or `read_network_requests` when driving the browser).

**Root cause traced:** tied to saves that include `oxySelectors` (the global-classes system new in 3.0). `data/save.php::save_document()` writes the tree to postmeta first (safe), then calls `saveSelectors()`, which writes to `wp_options` (also safe) before `generateCacheForGlobalSettings()` — and *that* CSS rebuild, through Breakdance's Twig compiler (`render/twig.php::runTwig()`), throws. Because the exception isn't caught inside `save_document()`, `wp_update_post()` (modified date, revision) and `generateCacheForPost()` (this post's cached CSS/HTML) never run for that save. Not yet isolated to one specific selector.

## 17. Second `html-to-page` pass on the same page — clear first, or target explicitly

`html-to-page` defaults to `parent_id: 1` (root) and appends at the end — it does NOT replace existing content. For a corrective/second pass, either delete the existing top-level tree first or pass an explicit `parent_id`/`position`; otherwise the old draft's elements stay as extra leading top-level siblings, rendering above the real content. Confirmed on Guerilla Steel (2026-08-17): Home, Standard Stable Kit and Contact each got a second build appended after the first, leaving 4–11 leftover draft sections per page ahead of the real ones.

**Diagnostic tell:** the old sections' classes reference selector IDs that don't exist in `get-css-selectors` (shown in the builder as class chips reading "(deleted)"). Confirm with `get-post-tree`, cross-referencing every `meta.classes` id against `get-css-selectors`, and check whether the orphans cluster in a contiguous leading block of top-level siblings — that means leftover draft content, not a selector problem. Fix is a plain `edit-post` delete on those top-level element ids; the correct content is already right behind them.

## 18. Adding a Container via the builder UI auto-names its class `container-N` if left unrenamed

Confirmed 2026-08-18 on 3.0.0-beta.4: a Container added through the visual builder gets a generic class like `container-1`, `container-2`… if not renamed. These carry no prefix or role, so they're easy to mistake for orphaned leftovers (the first read on Guerilla Steel) — they're just the builder default. Rename on creation to a real role-based name (§1); if one's already loose in the selector list, rename in place (check `get-css-selectors` for where it's applied first) rather than deleting it blind.

## 19. Element ID goes in the dedicated `settings.advanced.id` control, not the `attributes` array

Confirmed 2026-08-18 on 3.0.0-beta.4: element schemas have a first-class `settings.advanced.id` property, separate from `settings.advanced.attributes`, and the builder UI now rejects `id` through the attributes control ("ID is not allowed here, use the dedicated control"). Earlier Guerilla Steel section ids were set via `attributes: [{"name":"id","value":"..."}]` and rendered fine, but couldn't be hand-edited; all were migrated to `settings.advanced.id` with `attributes` cleared to `[]` (avoiding a duplicate `id=`).

**How to apply:** give any element an HTML `id` via `settings.advanced.id`, never `{"name":"id",...}` in `attributes`. Migrate old attributes-array ids opportunistically when touching an element rather than leaving both mechanisms mixed on a page.

**`html-to-page` uses the old path.** A plain `id="..."` attribute in `html-to-page` markup is imported as the deprecated `attributes` shape. Any section built that way with an `id` needs the follow-up `edit-post` migration (set `settings.advanced.id`, clear `attributes` to `[]`) before Vanessa can safely hand-edit it.

## 20. Footer/header elements render with an infixed auto-class — don't hand-write `bde-text-link` etc. in scoped CSS

Confirmed 2026-08-18 on Coastal Native Supply: elements inside a `breakdance_footer` (and presumably `breakdance_header`) template render auto-classes with an extra infix — `bde-f-text-link`, `bde-f-container`, `bde-f-container-link`, `bde-f-svg-icon2` — not the plain page-context `bde-text-link` / `bde-container`. A selector written against the plain class inside a footer/header scope silently never matches, and the element falls through to a less-specific rule (often the global link colour).

**Rule:** don't hardcode Breakdance's element-type auto-class inside footer/header-scoped CSS. Use a structural/tag selector — `.footer .col a` rather than `.footer .col .bde-text-link`. If you really need the auto-class, confirm it with `preview-post`/`preview-element` first.

## 21. Footer/nav text — never heading tags, always text-only

Structural/UI text that isn't page content — footer column titles ("Plants", "Trade"), a brand name repeated in the footer, sidebar labels — must never render as `<h1>`–`<h6>`. Each one pollutes the page's real heading outline, hurting SEO (heading structure is read as content hierarchy) and screen-reader navigation (users jumping by heading land on "Trade" instead of real sections). Use `<div>`/`<p>`/`<span>` with a class carrying the visual weight.

**How to apply:** give the label a dedicated class (reuse an existing one where the style exists — check `get-css-selectors` first) and set `settings.advanced.tag` to a non-heading tag. Confirmed on Coastal Native Supply (2026-08-18): footer titles had been `h5`/`h6` purely to inherit typography from a bare tag selector; switched to `div`. The first reassignment to `.footer-title`/`.footer-sec-title` looked right (tag was `div`, no error) but the classes never rendered — see §22. Don't trust "the tag changed and nothing errored"; check the rendered `class=""` list for the class name itself.

## 22. `meta.classes` needs a flat class-selector ID — a nested/descendant selector's ID doesn't resolve to an assignable class

The real bug behind §21's first attempt: `.footer-title` and `.footer-sec-title` had been authored as **nested/descendant selectors** — `.footer .footer-title`, registered as a child under `.footer` (what `& .footer-title` inside a `.footer { }` block produces, and what `get-css-selectors` returns as a `children[]` entry with its own `id`). Assigning that child's `id` via `meta.classes` does **not** work — Breakdance can't resolve a nested selector's id to a standalone class name. The element gets no class at all and silently falls back to default styling, while its tag/tree looks completely correct.

**Rule:** before assigning a selector id via `meta.classes`, confirm it's top-level in `get-css-selectors`' `selectors[]` with `"type": "class"`, not inside another selector's `children[]`. If the style only exists nested, rebuild it as a flat class (`.name { ... }` via `insert-stylesheet`), reassign every element to the new id, then delete the old nested selector. Confirmed on Coastal Native Supply (2026-08-18): both footer classes rebuilt flat, five elements reassigned, dead nested selectors deleted.

**Verify by reading the rendered class list.** `class="bde-f-text-42-100 bde-f-text"` with the expected custom class absent is the tell — cross-check every assigned class id against the literal class name in rendered HTML.

## 23. Slider/carousel pagination dots — no visible text, `aria-label` only

A pagination dot is a visual affordance sized by CSS, not content — it should never show visible text like "Slide 1". The accessible name comes from `aria-label` on the button/link (`aria-label="Slide 1"`); `aria-label` fully replaces the computed accessible name, so inner text is redundant at best.

**Trap:** Breakdance's `FTextLink` renders a literal "Click Here" fallback on the live front end when its `text` property is empty. Set `text` to a single non-breaking space instead — non-empty enough to suppress the fallback, visually blank, with `aria-label` carrying the name. Confirmed on Coastal Native Supply (2026-08-18), hero slider dots using `EssentialElements\FTextLink` with `tag: "button"`.

## 24. Business facts (phone, email, name, ABN) come from SCOS Business Info — never hardcoded

Stated by Vanessa 2026-10-07. Phone, email, business name and similar facts live once in SCOS Business Info (`scos_biz_*` options, Site Essentials → Business Info module) and every element reads them dynamically. Changing the number is then one option update, not a hunt through templates.

- **Visible text:** `[business_info setting="phone_number"]` (or `email`, `business_name`, …). Copyright line: `[site_copyright]`.
- **`tel:` / `mailto:` hrefs:** Breakdance dynamic data → PHP return (or the equivalent shortcode with dynamic-data safety off). Strip spaces so `+61 400 000 000` becomes `tel:+61400000000`:

```
[breakdance_dynamic field='phpreturn' params='{"code":"$phone = get_option('scos_biz_phone_number');\n\n// Optional: Clean up any accidental spaces the user might have saved\n$clean_phone = str_replace(' ', '', $phone);\n\nreturn 'tel:' . $clean_phone;"}']
[breakdance_dynamic field='phpreturn' params='{"code":"$email = get_option('scos_biz_email');\n\n// Optional: Clean up any accidental spaces the user might have saved\n$clean_email = str_replace(' ', '', $email);\n\nreturn 'mailto:' . $clean_email;"}']
```

  `sms:` links use the same pattern with `return 'sms:' . $clean_phone;` (add `?&body=` + urlencoded text for a pre-filled SMS).
- `breakdance_dynamic` is only registered during a Breakdance front-end render: `do_shortcode()` from WP-CLI returns it unexpanded. Verify with `preview-post`, not `wp eval`.
- Field reference: https://brighterwebsites.com.au/software/business-information/ (request with `Accept: text/markdown` for clean text). Option keys are `scos_biz_` + the field id (`phone_number`, `email`, `business_offering`, `service_area`, `provider_mobility` static/dynamic, `price_tier` literal `$`–`$$$$`).

## 25. Images in AI builds — the fundamental Image element

Stated by Vanessa 2026-10-07: placeholder and real images go in Breakdance's fundamental Image element (the AI-preferred image element; confirm its slug with `get-element-slugs`, and check which element `html-to-page` maps a plain `<img>` to, on first use per site), never as a CSS background (§3) or a custom wrapper. Placeholders are real `<img>` elements with final dimensions, `alt` and loading/fetchpriority set, so replacing one later is only a media swap.

## 26. `html-to-page` stores `&` as the literal text `&amp;`

Confirmed 2026-10-08 on Brighter Websites: any `&` in `html-to-page` markup, typed raw or as `&amp;`, is saved into the element's text as the five characters `&amp;`. Browsers still display "&", so the front end looks right, but the builder field shows `&amp;` and a later hand edit can double-escape it.

**After any `html-to-page` build whose copy contains `&`,** follow up with `edit-post` and set those text fields again with a plain `&`. `edit-post` stores it correctly. Check with `preview-element`: a correct field renders a bare `&` in the HTML; a double-encoded one renders `&amp;`.

## 27. Legacy string classes (`settings.advanced.classes`) can't be edited through the MCP

Confirmed 2026-10-08 on Brighter Websites: older Essential elements (e.g. `EssentialElements\Section`) can hold classes as a plain string array in `settings.advanced.classes`, not as selector IDs in `meta.classes`. `get-post-tree` shows them, but `edit-post` rejects any write to that key (not in the element schema), so the MCP cannot add or remove them. GA tracking classes like `ga-hrcy-*` commonly live here.

**To retire one:** remove it in the builder (Advanced > Classes), or neutralise it at the source (pause the GTM trigger that listens for it). It also goes when the section is rebuilt from Fundamentals. Don't try to delete a matching global selector to remove it: the string class isn't linked to the selector and keeps rendering.

## 28. Grid images — set a real `sizes` attribute, or the browser downloads the full-size file

Confirmed 2026-10-08 on Brighter Websites: a media-library image in the Fundamental Image element renders WordPress's default `sizes="(max-width: {full}px) 100vw, {full}px"`. In a multi-column grid that tells the browser each image is full-viewport wide, so desktop pulls the 1200–1800px original for a ~300px tile.

**When an image sits in a grid or column,** add a `sizes` entry in the element's attributes (`settings.advanced.attributes`) that matches the layout, e.g. `(max-width: 1023px) 50vw, 25vw` for a 4-up grid that drops to 2-up at tablet portrait. It replaces the default cleanly (verified with `preview-element`; no duplicate attribute). Full-width heroes keep the default.

Also: a `get-post-tree` snapshot of `media.alt` can be stale or empty. Check the rendered `alt` with `preview-element` before reporting missing alt text.
