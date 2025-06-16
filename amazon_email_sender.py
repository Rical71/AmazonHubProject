import pandas as pd
import smtplib
import ssl
import os
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from email.message import EmailMessage

# === Load business data ===
df = pd.read_csv("Filtered_Manhattan_Small_Businesses.csv")

# === Email log setup ===
log_file = "Sent_Email_Log.csv"
sent_log = []
if os.path.exists(log_file):
    sent_df = pd.read_csv(log_file)
    already_sent = set(sent_df["Email Sent To"].dropna().unique())
else:
    already_sent = set()

# === Extract and clean email from website ===
def get_email_from_website(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            match = re.search(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}", text)
            if match:
                return match.group(0).strip().split()[0]  # Ensure no extra text after email
    except:
        pass
    return ""

# === Email content ===
subject = "Unlock Extra Income with Amazon Hub!"
body = """Unlock Extra Income with Amazon Hub!
Are you a business in Manhattan looking for a simple way to boost your revenue? Amazon is seeking neighborhood businesses like yours to become Amazon Hub Partners!

Here's how it works:
Amazon delivers packages to your business daily.
Your staff or a family member delivers these packages to customers within 3 blocks radius in your community.
Earn $2.00 per package for the first 25 packages and $1.50 per package for each package thereafter.
Start with approximately 25 packages daily and grow from there!

Join us in making delivery more personal while adding a steady income stream to your business. Interested?

Reply to this email or click here to learn more!
"""

# === Email settings ===
sender_email = "skiva2002@gmail.com"
sender_name = "Richard Calvo"
app_password = "your_app_password_here"
cc_email = "calvrric@amazon.com"
attachments = ["IMG_0843.jpeg", "IMG_0844.jpeg"]
smtp_server = "smtp.gmail.com"
port = 587

# === Send emails ===
context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(sender_email, app_password)

    for index, row in tqdm(df.iterrows(), total=len(df)):
        business_name = row.get("Business Name", "")
        website = str(row.get("Website", ""))
        recipient_email = get_email_from_website(website)

        if not recipient_email or recipient_email in already_sent:
            continue

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"{sender_name} <{sender_email}>"
        msg["To"] = recipient_email
        msg["Cc"] = cc_email
        msg.set_content(body)

        for file_path in attachments:
            with open(file_path, "rb") as f:
                data = f.read()
                name = os.path.basename(file_path)
                msg.add_attachment(data, maintype="image", subtype="jpeg", filename=name)

        try:
            server.send_message(msg)
            print(f"✅ Email sent to {recipient_email}")
            sent_log.append({"Business Name": business_name, "Email Sent To": recipient_email, "Website": website})
        except Exception as e:
            print(f"❌ Failed to send to {recipient_email}: {e}")

# === Save log ===
if sent_log:
    log_df = pd.DataFrame(sent_log)
    if os.path.exists(log_file):
        log_df.to_csv(log_file, mode='a', index=False, header=False)
    else:
        log_df.to_csv(log_file, index=False)
    print(f"✅ Log updated in {log_file}")
else:
    print("⚠️ No new emails were sent.")
