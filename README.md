# Creative Agency Agents

An AI-powered creative digital marketing agency built with a multi-agent architecture. Upload a client's company PDF, tell the Planner what you want, and a team of specialised agents handles the rest.

## How it works

A **Planner Agent** (OpenAI function calling) manages five specialised agents as tools:

| Agent | Role |
|-------|------|
| RAG Agent | Saves the company PDF into a vector database and answers questions about the client |
| Strategy Agent | Researches current trends and plans the best poster concept |
| Creative Writer Agent | Writes one poster script and one video script |
| Video Editor Agent | Designs the poster image |
| Product Manager Agent | Writes the hook and caption, then emails the creative to the client |

Pipeline: `PDF upload → strategy → scripts → poster → email to client`

## Tech stack

- Python, OpenAI API (tool/function calling)
- Gradio (chat UI with PDF upload)
- RAG for company knowledge
- python-dotenv for configuration

## Getting started

1. Clone the repo and install dependencies
2. Add your `OPENAI_API_KEY` to a `.env` file
3. Run `planner_agent.ipynb`
4. Upload a company PDF in the Gradio chat and ask for a campaign
