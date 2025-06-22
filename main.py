from dotenv import load_dotenv
import chromadb

load_dotenv()

import getpass
import os

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")


from langchain_google_genai import ChatGoogleGenerativeAI

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto('https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1.')
        page.screenshot(path=f'example-{browser_type.name}.png')
        browser.close()
        print(f"Screenshot taken with {browser_type.name} browser.")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)



