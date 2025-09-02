<!-- Hero banner with animation -->

<div align="center">
  ![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000&color=36BCF7&center=true&vCenter=true&width=650&lines=👻+Welcome+to+Telegram+Ghost+Bot!;⚡+Educational+Security+Research+Tool;🐳+Docker+Ready+%7C+Python+Powered;✨+Session+Hijacking+%26+Phishing+Demo)
</div>

<h1 align="center">👻 Telegram Ghost Bot</h1>
<p align="center">
  A modern <b>Telegram Security Research Bot</b> showcasing session hijacking & OTP-phishing.<br/>
  <b>⚠️ For educational use only.</b>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge&logo=github" alt="Version" />
  <img src="https://img.shields.io/badge/License-Educational-red?style=for-the-badge&logo=book" alt="License" />
  <img src="https://img.shields.io/badge/Made%20With-Python-3776AB?style=for-the-badge&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker" alt="Docker" />
</p>

---

## ✨ Features

✅ **Session Hijacking Simulation** – Learn about Telegram authorization bypass in a **safe sandbox**<br/>
🔐 **OTP-Phishing Demo** – Controlled phishing demonstration for **cybersecurity awareness**<br/>
🧩 **Modular Python Code** – Well-structured and beginner-friendly<br/>
🐳 **Docker Support** – Deploy instantly with **zero setup hassle**<br/>
📊 **Educational Focus** – Built with clarity, documentation, and learning in mind

---

## 🚀 Quick Setup (Docker)

```bash
git clone https://github.com/Snowball-01/TelegramGhostBot.git
cd TelegramGhostBot

cp sample.env .env
# Edit .env with your API_ID, API_HASH, BOT_TOKEN, MONGODB_URL, and ADMINS

docker build -t telegram-ghost-bot .
docker run --env-file .env telegram-ghost-bot
```

---

## 🛠 Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp sample.env .env
# Fill in your .env file with credentials

python main.py
```

---

## ⚙️ Configuration

All configuration values go into `.env` (based on `sample.env`).

| Variable      | Description                            |
| ------------- | -------------------------------------- |
| `API_ID`      | Your Telegram API ID                   |
| `API_HASH`    | Your Telegram API Hash                 |
| `BOT_TOKEN`   | Your Telegram Bot API token            |
| `MONGODB_URL` | MongoDB connection string              |
| `ADMINS`      | Space-separated list of admin user IDs |

🔹 Example `.env` file:

```env
API_ID=your_api_id_here
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here
MONGODB_URL=your_mongodb_url_here

# You can add one or multiple admin IDs (space separated)
# Example: ADMINS=7172835107 1362204953
ADMINS=your_admin_ids_here
```

---

## 📂 Project Structure

```tree
TelegramGhostBot/
│
├── Dockerfile        # Container build file
├── sample.env        # Example environment variables
├── main.py           # Bot entry point
├── handlers/         # Telegram message/event handlers
├── database.py       # Database handling logic
├── variables.py      # Configuration variables
├── requirements.txt  # Python dependencies
├── .gitignore        # Git ignore rules
├── hero.svg          # Animated SVG banner
└── demo.gif          # Demo animation
```

---

## ⚠️ Security & Disclaimer

> ⚠️ **Important Notice**
>
> This project is provided **strictly for educational and research purposes only.**
>
> - ❌ Do **not** use this for malicious activities
> - ✅ Use only in controlled environments
> - 🛡️ The author assumes **no liability** for misuse

---

## ⭐ Contributing

We welcome contributions! 🎉

1. Fork the repo
2. Create your branch: `git checkout -b feature/NewFeature`
3. Commit: `git commit -m "Add NewFeature"`
4. Push: `git push origin feature/NewFeature`
5. Open a Pull Request 🚀

---

<p align="center">
  <img src="https://forthebadge.com/images/badges/built-with-love.svg"/>
  <br/>
  Made with ❤️ by <b>Snowball</b>
</p>
