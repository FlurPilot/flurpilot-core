---
trigger: always_on
---

FlurPilot "Freebie" Style Guide
Source of Truth for the "Clean Light" Design (matching the Scouting Kit)

1. Core Philosophy
Vibe: Clean, Serious, Municipal, "Digital Amtsstube" but modern.
Mode: Light Mode only (No Dark Mode for this view).
Contrast: High contrast dark slate text on white/light slate background.
2. Color Palette (Tailwind Mapping)
Primary / Brand (Emerald - "Growth & Land")
Primary: #10b981 (bg-emerald-500) - Buttons, Highlights, Map Polygons
Primary Dark: #059669 (text-emerald-600) - Strong Text, Hover States
Primary Light: #ecfdf5 (bg-emerald-50) - Badges, CTA Backgrounds
Border: #d1fae5 (border-emerald-100)
Neutrals (Slate - "Professionalism")
Background: #f8fafc (bg-slate-50) - Page Background (Canvas)
Surface: #ffffff (bg-white) - Cards, Sidebar, Header
Headlines: #0f172a (text-slate-900) - H1, H2, Strong Labels
Body Text: #334155 (text-slate-700) - Paragraphs
Muted: #64748b (text-slate-500) - Meta data, Labels
Borders: #e2e8f0 (border-slate-200) - Dividers, Card Borders
UI Elements
Shadows: Soft, diffuse. box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
Radius: Large radius. rounded-2xl (16px) for cards, rounded-xl (12px) for buttons.
3. Typography
Font: Inter (sans-serif).
Weights:
Regular (400): Body
Medium (500): Labels, Links
Semibold (600): Buttons, Badges
Extrabold (800): Hero Claims, Logos
4. Components
Sidebar / Navigation
Bg: White (bg-white)
Border: Slate-200 (border-r)
Active Item: Emerald-50 background (bg-emerald-50), Emerald-600 text (text-emerald-600).
Inactive Item: Slate-500 text (text-slate-500), Slate-50 hover (hover:bg-slate-50).
Map Styling
Tiles: CartoDB Positron (Light/Gray).
Polygons:
Fill: #10b981 (Opacity 0.25)
Stroke: #10b981 (Opacity 1.0, Weight 3px)
Badges (Status)
Verified/Success: Emerald-50 bg + Emerald-600 text + Dot indicator.
5. Refactoring Plan (Dashboard)
Layout: Switch bg-black to bg-slate-50.
Sidebar: Switch Glassmorphism/Dark to White/Clean.
Map: Change MapLibre style URL to a light theme (e.g. Carto or MapTiler Basic).
Colors: Replace Blue (blue-500) with Emerald (emerald-500).