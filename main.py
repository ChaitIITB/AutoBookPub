from dotenv import load_dotenv
import chromadb
load_dotenv()
import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from playwright.sync_api import sync_playwright
import base64
from langchain.schema import HumanMessage

with sync_playwright() as p:
    for browser_type in [p.chromium, p.firefox, p.webkit]:
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto('https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1')
        page.screenshot(path=f'example-{browser_type.name}.png')
        browser.close()
        print(f"Screenshot taken with {browser_type.name} browser.")


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

image_file_path = "example-chromium.png"

with open(image_file_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

message_local = HumanMessage(
    content=[
        {"type": "text", "text": "You are a book AI book writer, you don't write original content, but write a spin on the existing content, this is done using the image of a book page that is provided to you, in the response, you will write a new chapter based on the image provided."},
        {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"},
    ]
)
result_local = llm.invoke([message_local])
print(f"Response for local image: {result_local.content}")


