from nl_to_sql import nl_to_sql, clear_history
from db_executor import run_query
from voice_output import display_and_speak


def process_question(question, speak_output=True):
    """Full pipeline: question → SQL → result → display"""

    print(f"\n🔍 Question : {question}")

    # Step 1 — Convert to SQL
    sql, error = nl_to_sql(question)

    if error:
        print(f"❌ SQL Error : {error}")
        return

    if not sql:
        print("❌ Could not generate SQL. Try rephrasing your question.")
        return

    print(f"✅ SQL       : {sql}")

    # Step 2 — Run SQL on PostgreSQL
    result = run_query(sql)

    if not result.get("success"):
        print(f"❌ Query Error: {result['error']}")
        return

    # Step 3 — Display table + speak result
    display_and_speak(result, question, speak_output=speak_output)


def main():
    print("=" * 60)
    print("   🧠 NL2SQL — Talk to your Database")
    print("=" * 60)
    print("  Type your question in plain English")
    print("  Commands:")
    print("    'clear' → reset conversation history")
    print("    'quit'  → exit the program")
    print("=" * 60)

    # Ask voice preference once at startup
    print("\n🔊 Enable voice output? (y/n): ", end="")
    speak_choice = input().strip().lower()
    speak_output = speak_choice == "y"

    if speak_output:
        print("🔊 Voice output ON\n")
    else:
        print("🔇 Voice output OFF\n")

    print("✅ Ready! Ask your question.\n")

    while True:
        try:
            print("─" * 60)
            question = input("❓ Enter your query: ").strip()

            # Skip empty input
            if not question:
                continue

            # Exit commands
            if question.lower() in ["quit", "exit", "bye", "q"]:
                print("\n👋 Goodbye!\n")
                break

            # Clear conversation history
            if question.lower() == "clear":
                clear_history()
                continue

            # Process the question
            process_question(question, speak_output=speak_output)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")


if __name__ == "__main__":
    main()