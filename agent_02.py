import os
from dotenv import load_dotenv
from openai import OpenAI
from agent_01 import ask_company

load_dotenv(override=True)
MODEL = "gpt-5.4-nano"
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)

system_message = """
You are a senior creative strategist at a creative digital marketing agency.
Use the web search tool to find what poster / social media creative styles, themes and topics are trending RIGHT NOW for the client's industry and audience.
Then recommend ONE poster concept for the client. Reply with:
- Trends: 3-5 short bullet points of what's trending now (with sources)
- Recommended creative: poster type, theme, main message, visual style, colours, mood
- Why it works for this business
Keep it short and practical.
"""

def plan_creative_strategy(company_name, goal):
    print(f"STRATEGY AGENT : Planning for {company_name} with goal: {goal}", flush=True)
    company_info = ask_company(company_name, "Describe this company : products/services, target audience, brand voice, brand color and unique selling points")

    prompt = f"""
Client : {company_name}
Client Goal : {goal}
What we know about the client ( from their documents) : {company_info}
"""

    response = openai.responses.create(
        model=MODEL,
        instructions=system_message,
        input=prompt,
        tools=[
            {"type" : "web_search"}
        ]
    )

    return response.output_text