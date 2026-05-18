import os
import gradio as gr
from openai import OpenAI
import pandas as pd

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

products = pd.DataFrame([
    {"id": 1, "name": "Nike Air Max",       "category": "Shoes",       "price": 120, "description": "Comfortable running shoes"},
    {"id": 2, "name": "Samsung Galaxy S24", "category": "Electronics", "price": 899, "description": "Latest Android smartphone"},
    {"id": 3, "name": "Levi's 501 Jeans",   "category": "Clothing",    "price": 60,  "description": "Classic straight-fit jeans"},
    {"id": 4, "name": "Sony WH-1000XM5",    "category": "Electronics", "price": 350, "description": "Noise cancelling headphones"},
    {"id": 5, "name": "Adidas Hoodie",       "category": "Clothing",    "price": 55,  "description": "Comfortable everyday hoodie"},
    {"id": 6, "name": "Apple Watch SE",      "category": "Electronics", "price": 249, "description": "Smartwatch with fitness tracking"},
    {"id": 7, "name": "Puma Running Shoes",  "category": "Shoes",       "price": 85,  "description": "Lightweight sport shoes"},
])

def search_products(query):
    query = query.lower()
    results = products.copy()
    if "shoes" in query:
        results = results[results["category"] == "Shoes"]
    elif "electronics" in query:
        results = results[results["category"] == "Electronics"]
    elif "clothing" in query or "clothes" in query:
        results = results[results["category"] == "Clothing"]
    if "under 100" in query:
        results = results[results["price"] < 100]
    elif "under 200" in query:
        results = results[results["price"] < 200]
    elif "under 300" in query:
        results = results[results["price"] < 300]
    return results.to_string(index=False)

conversation_history = []

def chat(user_message, history):
    global conversation_history
    filtered = search_products(user_message)
    conversation_history.append({"role": "user", "content": user_message})
    recent_history = conversation_history[-10:]
    messages = [{"role": "system", "content": f"You are a helpful ecommerce shopping assistant. Relevant products: {filtered}. Only recommend these products, always mention price, be friendly."}] + recent_history
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1024
    )
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

demo = gr.ChatInterface(
    fn=chat,
    title="🛍️ Ecommerce Shopping Assistant",
    description="Ask me about products, prices, and recommendations!",
    examples=[
        "What shoes do you have?",
        "Show me electronics under $300",
        "What is the cheapest item?",
        "Recommend something for fitness"
    ]
)

demo.launch()
