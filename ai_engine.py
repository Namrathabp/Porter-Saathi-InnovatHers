from openai import OpenAI
from voice_client import speak
from rule_based import rule_based_reply  # if you have it in a separate file
client = OpenAI(api_key="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")
#openai.api_key = "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"
def ask_ai(query: str) -> str:
    return ask_ai_stream(query)   # wrapper for compatibility
  # put your OpenAI key here

def ask_ai_stream(query: str):
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Porter Saathi, a helpful, voice-first AI assistant for drivers with limited literacy. Respond in simple Hindi (or Hinglish if needed) with short, clear sentences."},
                {"role": "user", "content": query},
            ],
            max_tokens=200,
            temperature=0.1,
            stream=True,  # 👈 streaming enabled
        )

        buffer = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                buffer += delta
                # Speak sentence by sentence
                if any(p in buffer for p in [".", "?", "!", "।"]):
                    sentence, buffer = buffer, ""  # flush buffer
                    speak(sentence)

        # Speak any leftover text
        if buffer.strip():
            speak(buffer.strip())

    except Exception:
        # Fallback to rule-based if OpenAI fails
        speak(rule_based_reply(query))
