import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
MODEL = "gpt-5.4-nano"
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)

system_message = """
You are an award-winning creative copywriter at a creative digital marketing agency.
Using the creative strategy, write exactly these two things:

POSTER SCRIPT
- Headline (max 6 words, bold and punchy)
- Sub-headline (max 12 words)
- Call to action (max 5 words)
- Visual description: layout, imagery, colours, typography - detailed enough for a designer

VIDEO SCRIPT
- A 30-second vertical video (Reels / TikTok)
- Scroll-stopping hook in the first 3 seconds
- Scene by scene: visuals, voice-over, on-screen text
- End with the call to action

Make it bold, specific to the brand and based on the strategy. No generic filler.
"""

def write_creative_scripts(company_name, strategy):
    print("CREATIVE WRITER AGENT: writing scripts for", company_name, "with strategy:", strategy)
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Client: {company_name}\nStrategy: {strategy}"}
    ]
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    
    return response.choices[0].message.content