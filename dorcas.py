import random
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ChatMemberHandler
from telegram import ChatPermissions
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.rpc.types import TxOpts

# Telegram and Solana Credentials
BOT_TOKEN = '7552724713:AAF3oCaHO0w7m7E7llvh_q63frBjQUNCcRc'
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
YOUR_WALLET_ADDRESS = "F6ZxJ5KnYwzvzBMoVtakRrVRLhtpWVFLyQ9WZWnr494a"
PRIVATE_KEY = [139, 31, 135, 66, 180, 172, 249, 40, 0, 148, 129, 241, 255, 152, 245, 183, 219, 148, 20, 204, 0, 67, 175, 196, 205, 49, 231, 167, 97, 128, 8, 233, 209, 112, 200, 15, 147, 124, 146, 219, 132, 77, 122, 9, 235, 219, 183, 235, 128, 23, 184, 126, 249, 22, 44, 175, 241, 189, 62, 105, 81, 160, 131, 215]

# Initialize Solana Client and Wallet
client = Client(SOLANA_RPC_URL)
wallet = Keypair.from_secret_key(bytes(PRIVATE_KEY))
print("Wallet Public Key:", wallet.public_key)

# Banned Words for Moderation
BANNED_WORDS = ["spam", "scam", "nigga", "fuck"]

# Admin Functions
async def welcome_new_member(update, context):
    """Welcome new group members."""
    for member in update.chat_member.new_chat_members:
        await context.bot.send_message(chat_id=update.chat_member.chat.id, text=f"Welcome {member.full_name} to the group!")

async def delete_banned_words(update, context):
    """Delete messages containing banned words."""
    for word in BANNED_WORDS:
        if word in update.message.text.lower():
            await update.message.delete()
            await update.message.reply_text("Your message contained inappropriate content and was removed.")
            break

async def mute_user(update, context):
    """Mute a user."""
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await context.bot.restrict_chat_member(
            chat_id=update.message.chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text("User has been muted.")

# Gambling Functions
def coin_flip():
    """Simulate a coin flip."""
    return random.choice(["heads", "tails"])

def check_deposit(user_wallet, amount):
    """Check if the user sent the required amount to your wallet."""
    try:
        transactions = client.get_confirmed_signature_for_address2(YOUR_WALLET_ADDRESS, limit=10)
        for tx in transactions['result']:
            details = client.get_confirmed_transaction(tx["signature"])
            for instruction in details["result"]["transaction"]["message"]["instructions"]:
                if (
                    "parsed" in instruction and
                    instruction["parsed"]["info"]["source"] == user_wallet and
                    float(instruction["parsed"]["info"]["lamports"]) / 1e9 == amount
                ):
                    return True
        return False
    except Exception as e:
        print(f"Error checking deposit: {e}")
        return False

def send_winnings(user_wallet, amount):
    """Send winnings to the user's wallet."""
    try:
        transaction = Transaction()
        transaction.add(
            client.request_airdrop(PublicKey(user_wallet), int(amount * 1e9))
        )
        response = client.send_transaction(transaction, wallet, opts=TxOpts(skip_preflight=True))
        return response
    except Exception as e:
        print(f"Error sending winnings: {e}")
        return None

async def gamble(update, context):
    """Handle the gambling logic."""
    args = context.args

    if len(args) != 3:
        await update.message.reply_text("Usage: /gamble <amount> <heads/tails> <wallet_address>")
        return

    try:
        amount = float(args[0])
        user_choice = args[1].lower()
        user_wallet = args[2]

        if user_choice not in ["heads", "tails"]:
            await update.message.reply_text("Please choose 'heads' or 'tails'.")
            return

        # Check deposit
        if not check_deposit(user_wallet, amount):
            await update.message.reply_text("Deposit not detected. Please send your bet amount to the wallet.")
            return

        # Perform coin flip
        result = coin_flip()
        if user_choice == result:
            if send_winnings(user_wallet, amount * 2):
                await update.message.reply_text(f"The coin landed on {result}. You won {amount * 2:.2f} SOL!")
            else:
                await update.message.reply_text("Error sending winnings. Please contact support.")
        else:
            await update.message.reply_text(f"The coin landed on {result}. You lost. Better luck next time!")

    except ValueError:
        await update.message.reply_text("Invalid amount. Please enter a valid number.")

# General Message Handling
async def handle_message(update, context):
    """Handle general user messages."""
    user_message = update.message.text.lower()
    if "bet" in user_message:
        await update.message.reply_text("It seems you're interested in gambling. Use /gamble <amount> <heads/tails> <wallet_address> to get started.")
    else:
        await update.message.reply_text("I’m here to help! Ask me anything or type '/gamble' to start betting.")

# Start Command
async def start(update, context):
    """Handle the start command."""
    await update.message.reply_text(
        f"Welcome! This bot manages the group and allows gambling. Deposit funds to: {YOUR_WALLET_ADDRESS} to get started."
    )

# Main Function
def main():
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Admin Handlers
    application.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_banned_words))
    application.add_handler(CommandHandler("mute", mute_user))

    # Gambling Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gamble", gamble))

    # General Message Handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()
