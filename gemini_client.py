import subprocess
import json
import re
from config import GEMINI_CLI_PATH


def get_structured_work(project, did, left):
    """
    Send raw user input to Gemini CLI.
    Returns structured dict with completed, pending, notes.
    """

    prompt = f"""You are a professional work log formatter for a software/startup project.

The user will give you a casual description of what they did today and what's left.
Your job is to clean it up, rewrite it in clear professional English, and return ONLY a JSON object.

Project: {project}

What they did today (raw):
{did}

What's left / pending (raw):
{left}

Return ONLY this JSON structure, nothing else, no markdown, no explanation:
{{
  "completed": ["clear sentence about task 1", "clear sentence about task 2"],
  "pending": ["clear sentence about pending task 1", "clear sentence about pending task 2"],
  "notes": "any important context or observations worth noting, or empty string if none"
}}

Rules:
- Each item should be a complete, clear sentence
- Fix grammar, spelling, make it professional but not overly formal
- Split combined tasks into separate items if needed
- Keep it concise
- Return ONLY the JSON, absolutely nothing else
"""

    try:
        result = subprocess.run(
    [GEMINI_CLI_PATH],
    input=prompt,
    capture_output=True,
    text=True,
    timeout=60,
    shell=True
)

        if result.returncode != 0:
            raise Exception(f"Gemini CLI error: {result.stderr.strip()}")

        output = result.stdout.strip()

        # Extract JSON from output (in case gemini adds any extra text)
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
        else:
            raise Exception("Could not find JSON in Gemini response")

        # Validate structure
        if "completed" not in data:
            data["completed"] = []
        if "pending" not in data:
            data["pending"] = []
        if "notes" not in data:
            data["notes"] = ""

        return data

    except subprocess.TimeoutExpired:
        raise Exception("Gemini CLI timed out. Check your internet connection.")

    except json.JSONDecodeError:
        # Fallback: return raw text split into lines
        print("⚠️  Could not parse Gemini response as JSON, using raw formatting...")
        return {
            "completed": [line.strip() for line in did.split('\n') if line.strip()],
            "pending": [line.strip() for line in left.split('\n') if line.strip()],
            "notes": ""
        }

    except FileNotFoundError:
        raise Exception(
            f"Gemini CLI not found at '{GEMINI_CLI_PATH}'.\n"
            "Make sure Gemini CLI is installed and accessible in your PATH.\n"
            "Try running 'gemini --version' in your terminal to check."
        )
