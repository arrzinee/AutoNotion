import requests
from datetime import datetime
from config import NOTION_API_KEY, NOTION_PAGE_ID


HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def rich_text(content, bold=False, color="default"):
    return {
        "type": "text",
        "text": {"content": content},
        "annotations": {
            "bold": bold,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": color
        }
    }


def heading_block(text, level=2):
    return {
        "object": "block",
        "type": f"heading_{level}",
        f"heading_{level}": {
            "rich_text": [rich_text(text)]
        }
    }


def bullet_block(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [rich_text(text)]
        }
    }


def callout_block(text, emoji="🚀"):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [rich_text(text, bold=True)],
            "icon": {"type": "emoji", "emoji": emoji},
            "color": "gray_background"
        }
    }


def divider_block():
    return {"object": "block", "type": "divider", "divider": {}}


def paragraph_block(text, color="default"):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [rich_text(text, color=color)]
        }
    }


def todo_block(text, checked=False):
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [rich_text(text)],
            "checked": checked
        }
    }


def create_notion_page(project, structured_data):
    """
    Creates a new Notion page under the configured parent page.
    Returns the URL of the created page.
    """

    now = datetime.now()
    date_str = now.strftime("%d %B %Y")
    time_str = now.strftime("%I:%M %p")
    title = f"📅 Work Log — {date_str}"

    completed = structured_data.get("completed", [])
    pending = structured_data.get("pending", [])
    notes = structured_data.get("notes", "")

    # Build blocks
    blocks = []

    # Project callout
    blocks.append(callout_block(f"Project: {project}", emoji="💼"))
    blocks.append(divider_block())

    # Completed section
    blocks.append(heading_block("✅  Completed Today", level=2))
    if completed:
        for item in completed:
            blocks.append(todo_block(item, checked=True))
    else:
        blocks.append(paragraph_block("Nothing logged.", color="gray"))

    blocks.append(paragraph_block(""))  # spacer

    # Pending section
    blocks.append(heading_block("📌  Pending / Additional Work", level=2))
    if pending:
        for item in pending:
            blocks.append(todo_block(item, checked=False))
    else:
        blocks.append(paragraph_block("Nothing pending.", color="gray"))

    blocks.append(paragraph_block(""))  # spacer

    # Notes section
    if notes and notes.strip():
        blocks.append(heading_block("💬  Notes", level=2))
        blocks.append(paragraph_block(notes))
        blocks.append(paragraph_block(""))  # spacer

    # Footer
    blocks.append(divider_block())
    blocks.append(paragraph_block(f"🕐 Logged at {time_str}", color="gray"))

    # Page payload
    payload = {
        "parent": {"page_id": NOTION_PAGE_ID},
        "icon": {"type": "emoji", "emoji": "📝"},
        "cover": None,
        "properties": {
            "title": {
                "title": [{"type": "text", "text": {"content": title}}]
            }
        },
        "children": blocks
    }

    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        error = response.json()
        raise Exception(f"Notion API error {response.status_code}: {error.get('message', 'Unknown error')}")

    page_url = response.json().get("url", "")
    return page_url
