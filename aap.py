from flask import Flask,jsonify,request
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import markdown
from flask_cors import CORS

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API"))

app = Flask(__name__)
CORS(app, resources={ 
                    r"*": {
                            "origins": "*",
                            "methods": ["GET", "POST", "DELETE"],
                            "allow_headers": ["Content-Type","ngrok-skip-browser-warning"]
                        }
                    }
     )  

def call_llm(user_question):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful Gujarati assistant. No matter what language the user asks the question in, you must always reply only in Gujarati. Each answer should be maximum 50 words long."),
        contents=user_question,
    )

    return response


@app.route("/")
def home_page():
    return "hy"


@app.route("/response",methods =["POST"])
def reply():
    data = request.get_json()
    user_query = data["query"]
    response =call_llm(user_query)
    # text = 'LLM stands for **Large Language Model**.\n\nIn simpler terms, an LLM is a type of **artificial intelligence (AI)** program that is trained on a massive amount of text data. This training allows it to:\n\n*   **Understand and generate human-like text:** LLMs can read, write, and converse in a way that is remarkably similar to how humans do.\n*   **Process and analyze information:** They can digest vast quantities of text, identify patterns, extract meaning, and summarize information.\n*   **Perform a wide range of language-related tasks:** This includes answering questions, writing essays, translating languages, composing code, generating creative content, and much more.\n\nHere\'s a breakdown of the key components of the term:\n\n*   **Large:** This refers to two main aspects:\n    *   **Size of the model:** LLMs have a huge number of parameters (billions or even trillions). These parameters are like the "knobs and dials" that the model adjusts during training to learn complex relationships in data. More parameters generally lead to more sophisticated capabilities.\n    *   **Size of the training data:** They are trained on enormous datasets of text and code scraped from the internet, books, and other sources. This vast exposure to diverse language helps them learn grammar, facts, reasoning abilities, and different writing styles.\n\n*   **Language:** This indicates that the primary focus of these models is on **natural language processing (NLP)**. They are designed to work with and understand human language.\n\n*   **Model:** This refers to the underlying **neural network architecture** (often a transformer architecture) that powers the LLM. This architecture is what allows the model to process sequential data like text efficiently.\n\n**How do they work (in a simplified way)?**\n\nImagine you\'re teaching a child about the world by showing them millions of books, articles, and conversations. They would start to learn how words fit together, what things mean, and how to express themselves. LLMs do something similar but on a vastly larger scale.\n\nDuring training, the model learns to predict the next word in a sequence. By doing this repeatedly on massive datasets, it develops a deep understanding of:\n\n*   **Grammar and syntax:** How sentences are structured.\n*   **Semantics:** The meaning of words and phrases.\n*   **Context:** How the meaning of words changes based on surrounding words.\n*   **Facts and knowledge:** Information embedded within the training data.\n*   **Reasoning and logic:** To some extent, the ability to make connections and draw inferences.\n\n**Examples of LLMs:**\n\nYou\'ve likely encountered LLMs even if you don\'t know the term. Some well-known examples include:\n\n*   **GPT-3, GPT-4 (and their successors) by OpenAI:** Powers tools like ChatGPT.\n*   **LaMDA, PaLM 2 (and their successors) by Google:** Powers Google Bard.\n*   **LLaMA by Meta.**\n\n**In summary, LLMs are powerful AI systems that have revolutionized how we interact with and process information through language.** They are capable of understanding, generating, and manipulating text in sophisticated ways, making them a key technology in the current AI landscape.'
    # text = "data print"
    html_string = markdown.markdown(response.text)
    return jsonify({"AI_response":html_string})



if __name__ == "__main__":
    app.run(debug=True)