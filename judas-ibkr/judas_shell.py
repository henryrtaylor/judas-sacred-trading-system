import speech_recognition as sr

def handle_command(command):
    command = command.lower()
    if "scan" in command:
        return "📡 Running full scan..."
    elif "sacred trades" in command:
        return "📜 Displaying sacred trades this week..."
    elif "gabriel" in command and "vote" in command:
        return "📖 Gabriel voted HOLD on ARKK yesterday."
    else:
        return "❓ I do not understand yet... but I'm learning."

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak your command:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        return "I didn't catch that."
    except sr.RequestError:
        return "Speech service is unreachable."

def main():
    print("🧠 Welcome to the Judas Command Shell (type or speak)")
    while True:
        choice = input("Press V for voice, T to type, or Q to quit: ").lower()
        if choice == 'q':
            break
        elif choice == 'v':
            command = listen_for_command()
        elif choice == 't':
            command = input("💬 Enter command: ")
        else:
            print("Invalid input.")
            continue
        response = handle_command(command)
        print(response)

if __name__ == "__main__":
    main()
