# litterbot

## Description

An app to interact with the "Litter Robot", by [Whisker](https://www.litter-robot.com/litter-robot-4.html).

This app uses Python and FastAPI (with Web Sockets) as a backend wrapper around [@natekspencer](https://github.com/natekspencer)'s [pylitterbot](https://github.com/natekspencer/pylitterbot) library. The frontend is built using [SvelteKit](https://kit.svelte.dev/), [TailwindCSS](https://tailwindcss.com), and [DaisyUI](https://daisyui.com).

Inspired by [@natekspencer](https://github.com/natekspencer)'s [pylitterbot](https://github.com/natekspencer/pylitterbot).

## Getting Started

Clone and navigate to the the repository.

```bash
git clone https://engageintellect/litterbot
cd litterbot
```

### Configure environment variables.

```bash
cp /server/.env.example /server/.env
```

**Note:** You will need to get your Litter Robot's username and password credentials from the Whisker app.

```bash
cp /client/.env.example /client/.env
```

**Note:** Be sure to update the example values with your own.

### Server

Configure and run backend.

```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Client

Configure and run client.

```bash
cd client
pnpm i
pnpm run dev --host
```
