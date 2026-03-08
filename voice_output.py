import pyttsx3
import tabulate
from datetime import date

# Initialize TTS engine once
engine = pyttsx3.init()
engine.setProperty("rate", 165)    # Speed — 165 is natural pace
engine.setProperty("volume", 1.0)  # Max volume

def speak(text):
    """Speak text out loud using offline TTS"""
    engine.say(text)
    engine.runAndWait()

def format_value(value):
    """Convert raw values to clean readable strings"""
    if isinstance(value, date):
        return value.strftime("%B %d, %Y")
    if isinstance(value, float):
        return f"{value:.2f}"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value)

def to_table(result):
    """Print results as a clean terminal table"""
    if not result.get("success"):
        print(f"\n❌ Error: {result['error']}\n")
        return

    rows = result["rows"]
    count = result["count"]

    if count == 0:
        print("\n⚠️  No results found.\n")
        return

    # Format all values
    formatted_rows = [
        [format_value(v) for v in row.values()]
        for row in rows
    ]

    headers = result["columns"]

    print("\n" + "=" * 60)
    print(tabulate.tabulate(
        formatted_rows,
        headers=headers,
        tablefmt="rounded_outline"
    ))
    print(f"\n  ✅ {count} row(s) returned")
    print("=" * 60 + "\n")

def to_voice_text(result, question):
    """
    Convert query result into a natural speakable sentence.
    """
    if not result.get("success"):
        return f"Sorry, I encountered an error. {result['error']}"

    rows = result["rows"]
    count = result["count"]

    if count == 0:
        return "I found no results for your question."

    columns = result["columns"]
    first_row = rows[0]

    # Single number result (COUNT, SUM, AVG etc.)
    if count == 1 and len(columns) == 1:
        value = format_value(list(first_row.values())[0])
        col = columns[0].replace("_", " ")
        return f"The {col} is {value}."

    # List of names
    if "first_name" in columns and "last_name" in columns:
        names = [f"{r['first_name']} {r['last_name']}" for r in rows[:5]]
        if count == 1:
            return f"Found 1 result: {names[0]}."
        elif count <= 5:
            return f"Found {count} results: {', '.join(names)}."
        else:
            preview = ', '.join(names)
            return f"Found {count} results. First few are: {preview}, and more."

    # Product / item list
    if "product_name" in columns and "price" in columns:
        items = [f"{r['product_name']} at {format_value(r['price'])} dollars" for r in rows[:5]]
        return f"Found {count} products. {'. '.join(items)}."

    # Generic fallback
    if count == 1:
        parts = [f"{k.replace('_', ' ')} is {format_value(v)}" for k, v in first_row.items()]
        return "Result: " + ", ".join(parts) + "."
    else:
        return f"Found {count} results for your question."

def display_and_speak(result, question, speak_output=True):
    """
    Main function — show table + optionally speak the result.
    """
    # Always show table
    to_table(result)

    # Build voice text
    voice_text = to_voice_text(result, question)
    print(f"🔊 {voice_text}\n")

    # Speak if enabled
    if speak_output:
        speak(voice_text)


if __name__ == "__main__":
    # Test with fake result
    fake_result = {
        "success": True,
        "columns": ["product_name", "price"],
        "rows": [
            {"product_name": "Smart Watch", "price": 249.99},
            {"product_name": "Wireless Headphones", "price": 199.99},
            {"product_name": "Bluetooth Speaker", "price": 149.99},
        ],
        "count": 3
    }

    display_and_speak(fake_result, "top 3 most expensive products", speak_output=True)