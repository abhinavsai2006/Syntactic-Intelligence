import os
import csv
import threading
from datetime import datetime
import requests

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# App Configuration
# ---------------------------------------------------------------------------
load_dotenv()

app = Flask(__name__)

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_LLM_MODEL = os.getenv("NVIDIA_LLM_MODEL", "meta/llama-3.1-8b-instruct")
MAX_TOKENS = 1000

FEEDBACK_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback_log.csv")
CSV_LOCK = threading.Lock()

# ---------------------------------------------------------------------------
# Prompt Configuration  (3 functions × 3 styles = 9 prompts)
# ---------------------------------------------------------------------------
PROMPTS = {
    "answer_questions": {
        "short_factual": "Answer briefly and factually: {input}",
        "detailed_explainer": "Explain in detail with context and examples: {input}",
        "bullet_point_facts": "Give me 3 concise facts about: {input}",
    },
    "summarize_text": {
        "one_paragraph": "Summarize the following text in one paragraph: {input}",
        "key_points": "Extract the main points of this text as a bulleted list: {input}",
        "executive_brief": "Provide a brief executive overview (2-3 sentences) of this document: {input}",
    },
    "generate_creative": {
        "short_story": "Write a short story (under 300 words) about: {input}",
        "poem": "Write a poem in a creative tone about: {input}",
        "idea_generator": "Generate 3 creative concept ideas for a story/essay about: {input}",
    },
}

# Human-readable labels for the UI
FUNCTION_LABELS = {
    "answer_questions": "Answer Questions",
    "summarize_text": "Summarize Text",
    "generate_creative": "Generate Creative Content",
}

STYLE_LABELS = {
    "answer_questions": {
        "short_factual": "Short Factual",
        "detailed_explainer": "Detailed Explainer",
        "bullet_point_facts": "Bullet-Point Facts",
    },
    "summarize_text": {
        "one_paragraph": "One-Paragraph Summary",
        "key_points": "Key Points List",
        "executive_brief": "Executive Brief",
    },
    "generate_creative": {
        "short_story": "Short Story",
        "poem": "Poem",
        "idea_generator": "Idea Generator",
    },
}

# System prompts per function for richer context
SYSTEM_PROMPTS = {
    "answer_questions": (
        "You are a knowledgeable AI assistant specialized in answering questions "
        "accurately. Provide clear, well-structured answers. Use markdown formatting "
        "where helpful."
    ),
    "summarize_text": (
        "You are an expert text summarizer. Distill the provided content into its "
        "most essential points while preserving key meaning and nuance. Use markdown "
        "formatting where helpful."
    ),
    "generate_creative": (
        "You are a creative writing assistant with a flair for vivid imagery and "
        "engaging narratives. Produce original, compelling content. Use markdown "
        "formatting where helpful."
    ),
}


# ---------------------------------------------------------------------------
# Helper: Call the NVIDIA NIM API
# ---------------------------------------------------------------------------
def call_nvidia(function_key: str, style_key: str, user_input: str) -> str:
    """Build the prompt and call the NVIDIA NIM API. Returns the response text."""
    if not NVIDIA_API_KEY or NVIDIA_API_KEY == "your-api-key-here":
        return (
            "⚠️ **API key not configured.** Please add your NVIDIA API key "
            "to the `.env` file and restart the server."
        )

    # Validate keys
    if function_key not in PROMPTS:
        return "❌ Invalid function selected."
    if style_key not in PROMPTS[function_key]:
        return "❌ Invalid prompt style selected."

    prompt_template = PROMPTS[function_key][style_key]
    user_message = prompt_template.format(input=user_input)
    system_prompt = SYSTEM_PROMPTS[function_key]

    try:
        url = f"{NVIDIA_BASE_URL.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": NVIDIA_LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": 0.7
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 401:
            return "❌ **Authentication failed.** Please check your NVIDIA API key in the `.env` file."
        
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "⏳ **Request timeout.** The NVIDIA API server took too long to respond."
    except requests.exceptions.HTTPError as e:
        try:
            err_msg = response.json().get("detail", str(e))
        except Exception:
            err_msg = str(e)
        return f"❌ **NVIDIA API error ({response.status_code}):** {err_msg}"
    except Exception as e:
        return f"❌ **Unexpected error:** {str(e)}"



# ---------------------------------------------------------------------------
# Helper: CSV Feedback Logging
# ---------------------------------------------------------------------------
def _ensure_csv():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(FEEDBACK_CSV):
        with open(FEEDBACK_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "function", "prompt_style", "input", "response", "feedback"])


def log_feedback(function_key: str, style_key: str, user_input: str, response: str, feedback: str):
    """Append a feedback row to the CSV file (thread-safe)."""
    _ensure_csv()
    with CSV_LOCK:
        with open(FEEDBACK_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                function_key,
                style_key,
                user_input[:500],   # truncate very long inputs
                response[:500],     # truncate very long responses
                feedback,
            ])


def get_feedback_stats() -> dict:
    """Read the CSV and return aggregated feedback statistics."""
    _ensure_csv()
    stats = {
        "total_helpful": 0,
        "total_not_helpful": 0,
        "by_function": {},
    }
    with CSV_LOCK:
        with open(FEEDBACK_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                fn = row.get("function", "unknown")
                style = row.get("prompt_style", "unknown")
                fb = row.get("feedback", "")

                if fn not in stats["by_function"]:
                    stats["by_function"][fn] = {"helpful": 0, "not_helpful": 0, "styles": {}}
                if style not in stats["by_function"][fn]["styles"]:
                    stats["by_function"][fn]["styles"][style] = {"helpful": 0, "not_helpful": 0}

                if fb == "helpful":
                    stats["total_helpful"] += 1
                    stats["by_function"][fn]["helpful"] += 1
                    stats["by_function"][fn]["styles"][style]["helpful"] += 1
                elif fb == "not_helpful":
                    stats["total_not_helpful"] += 1
                    stats["by_function"][fn]["not_helpful"] += 1
                    stats["by_function"][fn]["styles"][style]["not_helpful"] += 1

    return stats


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Render the main application page."""
    return render_template(
        "index.html",
        functions=FUNCTION_LABELS,
        styles=STYLE_LABELS,
    )


@app.route("/generate", methods=["POST"])
def generate():
    """Accept user input, call Claude, and return the response as JSON."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided."}), 400

    function_key = data.get("function", "")
    style_key = data.get("style", "")
    user_input = data.get("input", "").strip()

    if not user_input:
        return jsonify({"error": "Please enter some text."}), 400

    response_text = call_nvidia(function_key, style_key, user_input)
    return jsonify({"response": response_text})


@app.route("/feedback", methods=["POST"])
def feedback():
    """Log user feedback (thumbs up / thumbs down) to CSV."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided."}), 400

    log_feedback(
        function_key=data.get("function", ""),
        style_key=data.get("style", ""),
        user_input=data.get("input", ""),
        response=data.get("response", ""),
        feedback=data.get("feedback", ""),
    )
    return jsonify({"status": "ok"})


@app.route("/feedback-summary")
def feedback_summary():
    """Render the feedback analytics page."""
    stats = get_feedback_stats()
    return render_template(
        "feedback_summary.html",
        stats=stats,
        function_labels=FUNCTION_LABELS,
        style_labels=STYLE_LABELS,
    )


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    _ensure_csv()
    app.run(debug=True, port=5000)
