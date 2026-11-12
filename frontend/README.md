# FounderGate Frontend Shell

## Setup

```bash
cd frontend
pnpm install
pnpm dev
```

## Testing

```bash
cd frontend
pnpm type-check
pnpm lint
npx playwright test
```

## Structure
- `/src/app/page.tsx` - Home page (scenario setup routing)
- `/src/app/analysis/new/page.tsx` - New analysis configuration
- `/src/app/analysis/page.tsx` - Active analysis view (split pane)
- `/src/app/report/page.tsx` - Strategic Decision Record (Report)
- `/src/components/ui` - Shared UI components (Buttons, etc.)

## Design System
The application uses a custom design system based on TailwindCSS, defined in `tailwind.config.ts` and `src/app/globals.css`. It features a dark theme with cyan and red accents, using `Inter` as the primary font.
