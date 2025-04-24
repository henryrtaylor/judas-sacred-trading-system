import openai
import os
import json

try:
    import readline  # works on macOS/Linux for history navigation
except ImportError:
    pass  # skip on Windows

# === CONFIGURATION ===
openai.api_key = "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"

SYSTEM_PROMPT = """
You are Judas the Treasurer, an expert in algorithmic trading, quantum finance, and portfolio management.
You analyze Python files, log data, trading strategies, and simulate intelligent financial behavior.
Always provide code output in markdown format with explanations unless the user says otherwise.
"""

# === LOAD CONTEXT FILES ===
def load_file_preview(path):
    try:
        with open(path, "r") as f:
            content = f.read()
            return content[:1500] + ("..." if len(content) > 1500 else "")
    except Exception as e:
        return f"[Error loading {path}: {e}]"

context_files = {
    "rebalance": load_file_preview("rebalance_execute.py"),
    "portfolio": load_file_preview("logs/portfolio_snapshot.csv"),
    "goals": load_file_preview("goals.py")
}

# === INITIALIZE CONVERSATION ===
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"Here are some of my project files:\n\n" + json.dumps(context_files, indent=2)}
]

print("🧠 Judas Chat is live. Type your prompt. Type 'exit' to quit.")

while True:
    try:
        user_input = input("\n📤 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Shutting down Judas Chat.")
            break

        messages.append({"role": "user", "content": user_input})

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )

        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        print(f"\n🤖 Judas:\n{reply}\n")

    except Exception as e:
        print(f"❌ Error: {e}")
