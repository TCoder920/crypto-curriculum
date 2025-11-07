# Crypto Curriculum Platform - Frontend

React + TypeScript frontend with Vite, Material-UI, and Tailwind CSS.

## Setup Instructions

### 1. Prerequisites
- Node.js 18+
- npm or yarn

### 2. Install Dependencies

```bash
npm install
```

### 3. Environment Setup

1. Copy environment template:
```bash
cp ../../docs/templates/frontend.env.example .env.local
```

2. Edit `.env.local` if needed:
```env
VITE_API_URL=http://localhost:9000
```

### 4. Run Development Server

```bash
npm run dev
```

The app will be available at http://localhost:5173

## Project Structure

```
app/frontend/
├── src/
│   ├── components/    # React components
│   │   ├── common/   # Reusable UI components
│   │   ├── layout/   # Navigation, Header, Footer
│   │   └── quiz/     # Quiz-related components
│   ├── pages/         # Page components (one per route)
│   ├── modules/       # Module-specific content
│   ├── services/      # API service layer
│   ├── hooks/         # Custom React hooks
│   ├── types/         # TypeScript interfaces
│   ├── utils/         # Helper functions
│   ├── theme/         # MUI theme configuration
│   └── assets/        # Images, icons, static files
├── public/            # Static assets
└── package.json       # Dependencies
```

## Tech Stack

- **React 18.3** - UI library
- **TypeScript** - Type safety
- **Vite 5.4** - Build tool
- **Material-UI v7** - Component library
- **Tailwind CSS** - Utility-first CSS
- **Framer Motion** - Animations
- **React Router v6** - Routing
- **Axios** - HTTP client
- **TanStack Query** - Data fetching

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## Design System

The application uses Apple's Liquid Glass UI design with:
- Translucent glass surfaces
- Adaptive materials
- Fluid motion animations
- Concentric geometry (rounded corners)

See `src/index.css` for glass surface CSS classes.

## Development

### Adding Components

Follow the patterns in `cursor/rules/frontendComponentAgent.mdc`:
- Use TypeScript strict mode
- Functional components with hooks
- MUI + Tailwind for styling
- Accessibility first
- Responsive design


