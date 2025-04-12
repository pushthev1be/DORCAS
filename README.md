python-telegram-bot==20.3
solana==0.35.1
openai==0.27.8
httpx==0.27.2
cryptography==41.0.3
 🎰 Telegram Solana Gambling Bot

A multifunctional Telegram bot built with `python-telegram-bot` that enables users to gamble using SOL (Solana), while also moderating group messages and managing new members.

---

## ⚙️ Features

### ✅ Group Management
- 👋 Welcomes new users with a friendly message
- 🧼 Auto-deletes messages containing banned/inappropriate words
- 🔇 Allows admins to mute users via `/mute` command

### 💸 Gambling Game (Heads/Tails)
- Users can gamble using Solana cryptocurrency
- Accepts SOL transfers to the bot wallet
- Verifies deposit transactions
- Performs a fair coin flip (`heads` or `tails`)
- Sends winnings back to user wallet if they win

---

## 🔐 Prerequisites

- Python 3.8+
- Telegram Bot Token from [BotFather](https://t.me/BotFather)
- A funded Solana wallet (with private key)
- Phantom wallet or any compatible Solana wallet for users

---

## 🧪 Commands

- `/start` — Shows welcome message and wallet address for deposits
- `/gamble <amount> <heads/tails> <wallet_address>` — Flip a coin to win SOL
- `/mute` (reply to message) — Mutes a user in group
- **Message filtering** — Automatically deletes messages with banned words

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/telegram-solana-bot.git
cd telegram-solana-bot
2. Create a Virtual Environment (Recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Configure Your Environment
Update these variables in your script:

python
Copy
Edit
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
YOUR_WALLET_ADDRESS = "YOUR_PUBLIC_SOL_ADDRESS"
PRIVATE_KEY = [your_private_key_array]
💡 You can export these as environment variables or use a .env file for better security.

🔒 Security Warning
This project is NOT production-ready. Sensitive information like private keys is hardcoded, which is unsafe. Before deploying:

Move secrets to environment variables or secure vaults

Implement secure handling of private keys

Add backend validation and deposit confirmation checks

Consider using Solana smart contracts for transparent wager processing

📦 Dependencies
python-telegram-bot

solana

Install via:

bash
Copy
Edit
pip install python-telegram-bot solana
📌 To-Do
 Add logging and error reporting

 Move sensitive info to .env

 Deploy backend for coin flip validation

 Add leaderboard and transaction history

 Host using a cloud server (e.g., Heroku, Render)

📝 License
MIT License © 2025 [Your Name]

🤝 Disclaimer
This bot is a demo and should not be used for real gambling or deployed without legal compliance. Gambling laws vary by jurisdiction — ensure you're operating within legal frameworks.
