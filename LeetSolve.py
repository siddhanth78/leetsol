from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import warnings
from PIL import Image
import pytesseract
import pyautogui
import pyperclip
import time

warnings.filterwarnings("ignore", message="cumsum_out_mps supported by MPS on MacOS 13+")

time.sleep(3)

def screenshots():
    screenshot = pyautogui.screenshot(region=(15, 310, 695, 1000))
    screenshot.save("q.png")

    screenshot2 = pyautogui.screenshot(region=(785, 250, 700, 250))
    screenshot2.save("sn.png")

def extract_text_from_image(image, snip):
    return pytesseract.image_to_string(image), pytesseract.image_to_string(snip)

screenshots()
question, snipp = extract_text_from_image(Image.open("q.png"), Image.open("sn.png"))

question = question.split("Example 1")[0]

print(question+"\n")
print(snipp+"\n")

model = OllamaLLM(model="qwen2.5:7b")

template = """Solve the incomplete snippet in the question in Python 3.
If a module offers a speed boost, always import and use it.
Make sure they are modules included with Python.
Don't add a main to call the class or run the program.
Make sure the program runs as fast as possible.

Question: {question}

Snippet: {snipp}

Just give me the code with no explanations.
Handle edge cases as well.
Be precise.
""" 

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

print("Generating response...\n")

ans = chain.invoke({"question": question, "snipp": snipp})

print(ans)
print("Snippet generated.")

pyperclip.copy(ans)
print("Copied to clipboard")
