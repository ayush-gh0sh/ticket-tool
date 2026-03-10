import discord
from discord.ext import commands
import os
import json

# ==============================
# LOAD CONFIG
# ==============================
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

PREFIX = config["prefix"]
TOKEN = config["token"]
STATUS = config["status"]

# ==============================
# BOT SETUP
# ==============================
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# ==============================
# ASYNC AUTO LOADER
# ==============================
async def load_cogs():
    base_path = os.getcwd().replace("\\", "/")

    for root, dirs, files in os.walk("."):
        root = root.replace("\\", "/")  # Normalize

        if "__pycache__" in root:
            continue

        for file in files:
            if not file.endswith(".py"):
                continue
            if file == "__init__.py":
                continue
            if file == "bot.py":
                continue

            filepath = os.path.join(root, file).replace("\\", "/")

            # Remove "./"
            if filepath.startswith("./"):
                filepath = filepath[2:]

            # Strip ".py"
            module_path = filepath[:-3]

            # Replace slashes with dots
            module_path = module_path.replace("/", ".")

            try:
                await bot.load_extension(module_path)
                print(f"[LOADED] {module_path}")
            except Exception as e:
                print(f"[FAILED] {module_path} → {e}")


# ==============================
# BOT READY EVENT
# ==============================
@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")
    await bot.change_presence(activity=discord.Game(name=STATUS))

        # Sync slash commands here (correct place)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Slash sync failed: {e}")

# ==============================
# START BOT
# ==============================
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)
import asyncio
asyncio.run(main())
