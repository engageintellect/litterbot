# litterbot

## Description

An app to interact with the "Litter Robot", by [Whisker](https://www.litter-robot.com/litter-robot-4.html). Built using Sveltekit, Python, FastAPI, WebSockets, TailwindCSS, and more.

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

```bash
cp /client/.env.example /client/.env
```

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
