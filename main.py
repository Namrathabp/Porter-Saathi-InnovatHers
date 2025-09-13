from ai_engine import ask_ai
from voice_client import listen, speak

if __name__ == "__main__":
    print("🚚 Porter Saathi CLI — type or speak your queries.")
    while True:
        query = input("👉 Enter query (or 'exit'): ")
        if query.lower() == "exit":
            break
        ans = ask_ai(query)
        print(f"🤖 Saathi: {ans}")
        speak(ans)
