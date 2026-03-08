import speech_recognition as sr
from voice_output import speak

recognizer = sr.Recognizer()

def listen():
    """
    Listen from microphone and return text.
    Returns (text, error)
    """
    with sr.Microphone() as source:
        print("\n🎤 Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        speak("I am listening. Ask your question.")
        print("🎤 Listening... speak now!")

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("⏳ Processing your voice...")
            text = recognizer.recognize_google(audio)
            print(f"✅ You said: {text}")
            return text, None

        except sr.WaitTimeoutError:
            return None, "No speech detected. Please try again."
        except sr.UnknownValueError:
            return None, "Could not understand. Please try again."
        except sr.RequestError as e:
            return None, f"Microphone error: {e}"


def get_input(mode="both"):
    """
    Get user input via voice or text.
    mode: 'voice' | 'text' | 'both'
    """
    if mode == "text":
        return input("\n⌨️  Type your question: ").strip(), None

    if mode == "voice":
        return listen()

    # mode == "both"
    print("\n─────────────────────────────")
    print("  [1] 🎤 Speak your question")
    print("  [2] ⌨️  Type your question")
    print("  [q] 👋 Quit")
    print("─────────────────────────────")
    choice = input("  Choose: ").strip().lower()

    if choice == "1":
        return listen()
    elif choice == "2":
        return input("\n⌨️  Type your question: ").strip(), None
    elif choice == "q":
        return "quit", None
    else:
        return None, "Invalid choice. Enter 1, 2 or q."


if __name__ == "__main__":
    print("=" * 40)
    print("   🎤 Voice Input Test")
    print("=" * 40)
    text, error = get_input(mode="both")
    if error:
        print(f"❌ {error}")
    else:
        print(f"📝 Got: {text}")