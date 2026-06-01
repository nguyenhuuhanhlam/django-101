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
