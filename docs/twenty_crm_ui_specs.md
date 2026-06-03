# Twenty CRM UI Specifications

This document outlines the UI architecture and design specifications used to build a 100% pixel-perfect clone of the Twenty CRM interface.

## Tech Stack
- **Backend:** Django
- **Styling:** Tailwind CSS
- **Interactivity:** Alpine.js (`x-data`, `x-show`, `x-bind:class`)
- **Icons:** Lucide Icons (CDN)
- **Typography:** Inter (Google Fonts, `antialiased` on `<body>`)

## Layout & Shell
The main shell consists of a left sidebar (`app_sidebar.html`), a top header (`app_header.html`), and a main content area (`<main>`). The state for the sidebar is managed globally on the `<body>` tag via Alpine.js (`x-data="{ sidebarOpen: true }"`).

## Sidebar Specifications (`app_sidebar.html`)

### Dimensions & States
- **Expanded Width:** `224px` (Tailwind `w-56`).
- **Collapsed Width:** `40px` (Tailwind `w-10`).
- **Padding:** `px-3` when expanded, `px-0` when collapsed.
- **Animations:** `transition-all duration-200` for smooth state toggling.
- **Background:** `bg-zinc-900` with `border-zinc-800` right border.

### Sidebar Header
- **Height:** `44px` (`h-11`).
- **Alignment:** `justify-between` (expanded) vs `justify-center` (collapsed).
- **Logo (D):** `20x20px` (`w-5 h-5`), `rounded-md`, `bg-sky-600`, text `9px`. 
- **Text:** `text-[rgb(179,179,179)] tracking-wide text-sm font-medium`.

### Menu Items (Workspace Group)
Menu items are dynamically rendered via a Django Context Processor (`apps.core.context_processors.sidebar_menu`) to keep the template DRY.

#### Typography & Spacing
- **Text:** `text-[rgb(179,179,179)] tracking-wide text-sm font-light` (Inter 300).
- **Gap:** `gap-2` between icon and text.
- **Icon Wrapper:** `20x20px` (`w-5 h-5`), `rounded-md` with 25% opacity background (e.g., `bg-sky-500/25`, `bg-violet-500/25`).
- **Icon Size:** `12x12px` (`w-3 h-3`) inside the wrapper.

#### Hover & Highlight Behaviors (Critical for Twenty CRM look)
1. **Expanded State (`sidebarOpen = true`):**
   - The hover highlight (`bg-white/5`) stretches across the full width of the sidebar.
   - **Alignment Trick:** Uses `-mx-1 px-1` (4px negative margin + 4px padding). This pushes the background 4px to the left, but perfectly compensates the content. **Result:** The menu icons stay vertically perfectly aligned with the header logo, while the hover background wraps them neatly.
   - **Height:** `32px` (`h-8`).

2. **Collapsed State (`sidebarOpen = false`):**
   - The hover highlight **does not** stretch horizontally.
   - It shrinks to a `28x28px` square (`w-7 h-7`), centered via `self-center` and `justify-center`.
   - **Result:** Since the icon wrapper is `20x20px`, the `28x28px` container creates exactly `4px` of padding around the icon on all sides. It remains perfectly centered in the `40px` wide collapsed sidebar.

#### Collapsible Workspace Label
- Uses an inner Alpine state: `x-data="{ workspaceOpen: true }"`.
- Label (`WORKSPACE`) is `text-[11px] font-medium uppercase tracking-wider text-zinc-500`.
- Only visible when the sidebar is expanded.
- Has a chevron icon that rotates (`-rotate-90`) when collapsed.
- Menu items inside are shown if `workspaceOpen == true`.

## Coding Conventions
1. **Tailwind Classes:** Written vertically (one class per line) inside `class="..."` for extreme readability and easy version control diffs.
2. **Alpine Logic:** Inline logic using `x-bind:class` for ternary operations (e.g., `sidebarOpen ? 'w-56' : 'w-10'`).
3. **DRY Templates:** Use Django Context Processors for arrays of data to avoid repeating complex HTML structures (like menu items).

## Theme Color Palette
- **Main Workspace Background:** `#09090b` (Tailwind `bg-[#09090b]` / zinc-950).
- **Sidebar & Header Background:** `#0f0f11` (Tailwind `bg-[#0f0f11]`).
- **Sidebar Right Border & Header Bottom Border:** `#1f1f23` (Tailwind `border-[#1f1f23]`).
- **Grid Divider Borders:** `#1a1a1e` (Tailwind `border-[#1a1a1e]`).

## Header Specifications (`app_header.html`)
- **Height:** `56px` (`h-14`) to align with the sidebar header.
- **Horizontal Padding:** `px-6` (24px) to align content cleanly with the table's horizontal margins.
- **Header Button:** Subtle action button with shortcut split indicator (`| ⌘K`), coupled with a `more-horizontal` options dropdown.

## Table & Grid Specifications (`user_list.html`)
- **Spacing Alignments:** Layout container utilizes `mx-6` (24px) horizontal margins and `pt-5` (20px) top padding below header.
- **Toolbar Actions:**
  - View dropdown titled `"All People · {count}"` with list icon and chevron.
  - Actions (`Filter`, `Sort`, `Options`) are purely text-based (no icons) spaced out with `gap-5` on the right.
- **Spreadsheet Grid Layout:**
  - Full grid lines using thin `#1a1a1e` (`border-[#1a1a1e]`) vertical and horizontal borders.
  - Sizing: compact row height with `py-1.5 px-3.5` cell padding for a data-dense look.
  - Table Head (`th`): `text-sm` (14px) and `font-normal` (to match sidebar menu items) with small prefixed Lucide icons (`w-3.5 h-3.5`).
  - Summary Row (`Calculate`): Placed at the bottom without vertical divider lines (`border-r`).
- **Vertical Stretching:** Content page and table wrapper stretch to fill the viewport (`flex-1 flex flex-col min-h-0`), locking headers/toolbar at the top while letting the table body scroll independently.

### User Detail Split Panel
- `user_list.html` now owns an Alpine component at the page root with:
  - `detailOpen`: controls whether the right-side detail panel is visible.
  - `panelWidth`: current detail panel width, default `380px`.
  - `selectedUser`: plain JS object populated from the clicked Django-rendered table row.
  - `selectUser(user)`: stores the selected user, opens the panel, then calls `lucide.createIcons(...)` inside `$nextTick()` so icons inside dynamically rendered Alpine content are hydrated.
  - `startResize(event)`: handles mouse resize for the split panel.
- Clicking a user row opens the right split panel. The selected row uses `x-bind:class` to apply `bg-white/5`.
- Checkboxes inside rows must use `@click.stop` so selecting a checkbox does not open the detail panel.
- Keyboard access: rows have `tabindex="0"` and `@keydown.enter="$el.click()"`.
- The detail panel is an `<aside>` rendered to the right of the table with `x-cloak`, `x-show="detailOpen"`, and `x-transition`.
- Panel sizing:
  - Default width: `380px`.
  - Minimum width: `320px`.
  - Maximum width: `560px`.
  - Resize handle is a `w-1.5` absolute strip on the panel's left edge with `cursor-col-resize` and `hover:bg-violet-500/40`.
- Panel layout:
  - Background: `bg-[#0f0f11]`.
  - Border: `border-[#1a1a1e]`.
  - It is separated from the table by `ml-3`.
  - Header height is `h-14`, matching the app header rhythm.
  - Body uses `overflow-y-auto`, so detail content scrolls independently.
- Current detail sections:
  - `Profile`: username, first name, last name.
  - `Access`: active/inactive status, staff flag, superuser flag.
  - `Timeline`: created timestamp, last login timestamp.
- `base.html` contains a global `[x-cloak] { display: none !important; }` rule. Keep this rule because Alpine loads with `defer` and the split panel should not flash before initialization.

### Tailwind Build Note
- New split panel classes are compiled into `static/css/style.css` from `static/src/input.css`.
- After changing templates or Tailwind utility classes, rebuild CSS with:
  - `npx @tailwindcss/cli -i .\static\src\input.css -o .\static\css\style.css`
