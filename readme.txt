# Amazon Hub Outreach Automation

This project automates two major business tasks for local outreach:

1. **Scraping Business Listings**: Extracts small, local business information (like coffee shops, electronics repair, etc.) in Manhattan ZIP codes using the Google Maps Places API.
2. **Automated Email Outreach**: Sends a professionally crafted outreach email to those businesses with attachments promoting Amazon Hub partnership opportunities.

---

## 🔧 Features

- Scrapes business name, phone, address, and website
- Extracts verified email addresses from business websites
- Sends personalized emails with flyer attachments
- Logs which businesses have been contacted
- Prevents duplicate sends using `Sent_Email_Log.csv`

---

## 📂 File Overview

| File                      | Purpose                                                    |
|--------------------------|-------------------------------------------------------------|
| `business_scraper_clean.py` | Scrapes Google Maps data for local businesses               |
| `amazonhub_email_sender.py` | Sends emails to businesses using Gmail + App Password        |
| `Sent_Email_Log.csv`     | Logs all businesses that were successfully emailed         |
| `IMG_0843.jpeg`, `IMG_0844.jpeg` | Flyer attachments included in the email outreach           |

---

## 📧 Email Details
- Subject: *"Unlock Extra Income with Amazon Hub!"*
- Includes flyer attachments and call-to-action
- Cc's Amazon work address for transparency

---

## 🔐 Requirements

- Gmail account with App Password enabled
- Python 3.9+
- Required Python packages: `pandas`, `tqdm`, `requests`, `bs4`, `smtplib`
- Google Maps Places API key

---

## 🚀 Getting Started

1. Configure your API key and email settings inside each script.
2. Run `business_scraper_clean.py` to generate your business list.
3. Run `amazonhub_email_sender.py` to send outreach emails automatically.

---

## 📜 License
This project is private and intended for internal use only.

---

## 👤 Author
**Richard Calvo**
- GitHub: [@Rical71](https://github.com/Rical71)
- Contact: `skiva2002@gmail.com`
- Amazon Work Email: `calvrric@amazon.com`
