This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

init husky hooks:

```bash
npm run prepare
```

Install project dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

Accessibility

screen readers :
to include text in page that is designed to only be read by screen readers. please use predefined css class

```
.visually-hidden, .sr-only to add
```

Reduced motion

Due to a variety of cognitive and visual conditions, motion-based animations can be uncomfortable or dangerous for some users.
if we need to add animation to some elements ven when prefers-reduced-motion is active, please use predefined css class

```
.animates-without-motion
```
