# Quickstart: Using the MetaExpert CLI

This guide provides a step-by-step tutorial for getting started with the `metaexpert` command-line interface.

## 1. Installation

First, ensure you have Python 3.12+ installed. Then, install MetaExpert from PyPI:

```bash
-pip install metaexpert
+uv pip install metaexpert
```

## 2. Create Your First Expert Project

Navigate to your workspace and run the `new` command:

```bash
metaexpert new my-first-bot
```

This will create a new directory called `my-first-bot` with a ready-to-use project structure.

## 3. Configure API Keys (for Live Trading)

Navigate into your new project directory:

```bash
cd my-first-bot
```

Open the `.env` file and add your exchange API keys. This file is ignored by Git, so your secrets are safe.

```dotenv
# .env
BYBIT_API_KEY="YourApiKey"
BYBIT_API_SECRET="YourApiSecret"
```

## 4. Run the Bot

To run your bot in the default paper trading mode, simply use the `run` command:

```bash
metaexpert run
```

Your expert is now running in the background!

## 5. Check the Status

You can see all experts in your workspace with the `list` command:

```bash
metaexpert list
```

To get more detailed information about a specific running bot, use the `status` command:

```bash
metaexpert status my-first-bot
```

## 6. Stop the Bot

To stop a running expert, use the `stop` command with the expert's name:

```bash
metaexpert stop my-first-bot
```
