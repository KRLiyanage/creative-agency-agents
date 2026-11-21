import os
from dotenv import load_dotenv
from openai import OpenAI
import smtplib
from email.message import EmailMessage

load_dotenv(override=True)

MODEL = "gpt-5.4-nano"
openai = OpenAI()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

system_message = """
You are the product manager at a creative digital marketing agency.
For the creative below, write a social media post. Reply in exactly this format:
HOOK: <one scroll-stopping line>
CAPTION: <Instagram caption with a few emojis, a call to action and 5-8 hashtags>
"""

def send_creative_email(company_name, scripts, poster_path):
    print(f"PRODUCT MANAGER AGENT: sending creative for {company_name} to {EMAIL_TO}", flush=True)
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Client: {company_name}\n\n{scripts}"},
    ]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    hook_and_caption = response.choices[0].message.content

    msg = EmailMessage()
    msg["Subject"] = f"New creative for {company_name}"
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg.set_content(f"""Hi,

Here is the new creative for {company_name}. Poster is attached.

{hook_and_caption}

----------------------------------------
{scripts}
""")

    with open(poster_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png", filename=os.path.basename(poster_path))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    return f"Email sent to {EMAIL_TO}.\n\n{hook_and_caption}"

sample_scripts = """
POSTER SCRIPT
Headline: Sip The Summer
Sub-headline: Our new iced menu is here - cold, bright and made fresh
Call to action: Try it today
Visual description: tall iced coffee glass in the centre with condensation, pastel blue background,
warm orange sun shapes, bold rounded white headline at the top, small logo "Blue Bottle Cafe" at the bottom.
"""

import glob

poster_paths = sorted(glob.glob("outputs/*.png"))[-1]
print(send_creative_email("Blue Bottle Cafe", sample_scripts, poster_paths))