# COO Chat – Angular UI (Story 4)

Chat experience that calls the AI Gateway and shows answers with citations.

## Features

- Send messages to the COO chatbot.
- Display assistant replies and citation sources (source file, title, snippet).
- API base URL configurable via environment.

## Prerequisites

- Node 18+
- Angular CLI: `npm i -g @angular/cli@17`

## Setup

1. Set the API base URL in `src/environments/environment.ts` (and `environment.prod.ts` for production).
2. Run the AI Gateway API (see `api/README.md`) so the chat can call `/chat`.

## Development

```bash
cd frontend
npm install
ng serve
```

Open `http://localhost:4200`. Use the chat panel to ask COO FAQs.

## Integration into COO app

To embed this chat in an existing COO Angular app:

1. Copy the `chat` module/components and the `CoochatService` into your app.
2. Add a chat trigger (e.g. floating button or header icon) that opens the chat panel.
3. Set `apiBaseUrl` in your environment to point to the deployed AI Gateway.

## Build

```bash
ng build
```

Output in `dist/`. For production, set `apiBaseUrl` in `environment.prod.ts`.
