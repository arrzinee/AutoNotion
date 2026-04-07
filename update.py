from config import DEFAULT_PROJECT
from gemini_client import get_structured_work
from notion_client import create_notion_page


def multiline_input(prompt):
    """Accepts multiline input. User presses Enter twice to finish."""
    print(prompt)
    print("  (press Enter twice when done)\n")
    lines = []
    while True:
        line = input()
        if line == "":
            if lines:
                break
        else:
            lines.append(line)
    return "\n".join(lines)


def main():
    print("\n" + "─" * 50)
    print("  📝  Notion Work Log Updater")
    print("─" * 50 + "\n")

    # Project name
    project_input = input(f"  Project name [{DEFAULT_PROJECT}]: ").strip()
    project = project_input if project_input else DEFAULT_PROJECT
    print()

    # What they did
    did = multiline_input("  What did you do today?")
    print()

    # What's left
    left = multiline_input("  What's left / additional work?")
    print()

    # Process with Gemini
    print("  ⏳ Sending to Gemini for formatting...")
    try:
        structured = get_structured_work(project, did, left)
    except Exception as e:
        print(f"\n  ❌ Gemini error: {e}")
        return

    print("  ✅ Gemini done. Pushing to Notion...\n")

    # Preview what's being pushed
    print("─" * 50)
    print(f"  Project : {project}")
    print(f"  Done    : {len(structured['completed'])} items")
    print(f"  Pending : {len(structured['pending'])} items")
    print("─" * 50 + "\n")

    # Push to Notion
    try:
        page_url = create_notion_page(project, structured)
        print(f"  🚀 Notion page created successfully!")
        print(f"  🔗 {page_url}\n")
    except Exception as e:
        print(f"\n  ❌ Notion error: {e}\n")
        return


if __name__ == "__main__":
    main()
