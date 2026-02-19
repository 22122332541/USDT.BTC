# USDT.BTC

A Next.js application for USDT to BTC exchange with Vercel Web Analytics integration.

## Features

- Built with Next.js 15 App Router
- TypeScript support
- Vercel Web Analytics integration for tracking visitors and page views
- Modern React 18.3
- ESLint configuration

## Getting Started

### Prerequisites

- Node.js 18.17 or later
- npm, pnpm, yarn, or bun

### Installation

1. Install dependencies:

```bash
npm install
# or
pnpm install
# or
yarn install
# or
bun install
```

2. Run the development server:

```bash
npm run dev
# or
pnpm dev
# or
yarn dev
# or
bun dev
```

3. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Building for Production

```bash
npm run build
# or
pnpm build
# or
yarn build
# or
bun build
```

### Running in Production

```bash
npm start
# or
pnpm start
# or
yarn start
# or
bun start
```

## Vercel Web Analytics

This project includes Vercel Web Analytics integration. The `<Analytics />` component from `@vercel/analytics/next` is included in the root layout (`app/layout.tsx`).

### Setup

1. Deploy your app to Vercel
2. Enable Web Analytics in your Vercel project dashboard (Analytics tab)
3. Once deployed, the analytics will automatically start tracking visitors and page views

### Viewing Analytics Data

After deployment:
1. Go to your [Vercel dashboard](https://vercel.com/dashboard)
2. Select your project
3. Click the **Analytics** tab
4. View your data after users have visited your site

For more information, see the [Vercel Web Analytics documentation](https://vercel.com/docs/analytics).

## Project Structure

```
.
├── app/
│   ├── layout.tsx       # Root layout with Analytics component
│   ├── page.tsx         # Home page
│   └── globals.css      # Global styles
├── public/              # Static assets
├── .eslintrc.json       # ESLint configuration
├── .gitignore          # Git ignore rules
├── next.config.js      # Next.js configuration
├── package.json        # Project dependencies
└── tsconfig.json       # TypeScript configuration
```

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Vercel Web Analytics](https://vercel.com/docs/analytics)

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new).

Check out the [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.
