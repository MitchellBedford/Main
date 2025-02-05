import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Hardcoded email credentials (⚠️ Security Risk - Don't use in public/shared code)
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "recipient_email@gmail.com"
EMAIL_PASSWORD = "sender_email_password/App_Password"

# Function to fetch cryptocurrency data sorted by biggest % loss in 24h
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "price_change_percentage_24h_asc",  # Sort by biggest loss
        "per_page": 200,  # Fetch more cryptos
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Print the full list of cryptos looked at
        print("\n📊 Full List of Cryptos and 24h % Change:")
        for coin in data:
            print(f"{coin['name']} ({coin['symbol'].upper()}): {coin['price_change_percentage_24h']:.2f}%")
        
        return data
    else:
        print("❌ Error fetching data:", response.status_code)
        return []

# Function to identify cryptocurrencies that have dropped more than 6% in 24h
def get_large_drops():
    crypto_data = get_crypto_data()
    notification_list = []

    for coin in crypto_data:
        if coin["price_change_percentage_24h"] is not None and coin["price_change_percentage_24h"] < -6:
            notification_list.append({
                "name": coin["name"],
                "symbol": coin["symbol"].upper(),
                "current_price": coin["current_price"],
                "price_change_24h": coin["price_change_percentage_24h"],
                "rank": coin["market_cap_rank"]
            })
    
    return notification_list

# Function to send email notifications
def send_email(notification_list):
    if not SENDER_EMAIL or not RECEIVER_EMAIL or not EMAIL_PASSWORD:
        print("❌ Email credentials are missing. Please enter them in the script.")
        return

    subject = "🚨 Crypto Alert: Major 24h Drops 🚨"
    
    body = "📉 **Full List of Cryptos Sorted by 24h % Loss:**\n\n"
    all_cryptos = get_crypto_data()
    for coin in all_cryptos:
        body += f"🔹 {coin['name']} ({coin['symbol'].upper()}): {coin['price_change_percentage_24h']:.2f}%\n"

    body += "\n📌 **Cryptos That Dropped More Than 6% in 24h:**\n\n"

    for coin in notification_list:
        body += (f"🔻 {coin['name']} ({coin['symbol']})\n"
                 f"📉 24h Change: {coin['price_change_24h']:.2f}%\n"
                 f"💰 Current Price: ${coin['current_price']}\n"
                 f"🏆 Popularity Rank: {coin['rank']}\n\n")

    # Email setup
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Sending email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Error sending email:", e)

# Main function
def main():
    print("\n🔍 Fetching crypto data...")
    notification_list = get_large_drops()

    if notification_list:
        print("\n⚠️ Cryptos with more than 6% drop in the last 24 hours:")
        for coin in notification_list:
            print(f"{coin['name']} ({coin['symbol']}): {coin['price_change_24h']:.2f}%")
        send_email(notification_list)
    else:
        print("\n✅ No major drops detected.")

if __name__ == "__main__":
    main()
