# AI Assistant

A web-based AI assistant powered by **Anthropic Claude Sonnet** with three distinct AI functions, multiple prompt styles, and a built-in feedback system.

## Features

| Function | Prompt Styles |
|----------|--------------|
| 💡 **Answer Questions** | Short Factual · Detailed Explainer · Bullet-Point Facts |
| 📝 **Summarize Text** | One-Paragraph · Key Points List · Executive Brief |
| ✨ **Generate Creative Content** | Short Story · Poem · Idea Generator |

- 🎨 Premium dark-themed UI with glassmorphism & animations
- 👍👎 Feedback logging with analytics dashboard
- 📊 Feedback summary page at `/feedback-summary`
- 🔒 API key stored securely in `.env`

## Setup

### 1. Clone / Navigate to the project

```bash
cd ai-assistant
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Edit the `.env` file and replace the placeholder:

```
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
```

Get your key from [console.anthropic.com](https://console.anthropic.com).

### 5. Run the app

```bash
python app.py
```

Or using Flask CLI:

```bash
flask run
```

The app will be available at **http://127.0.0.1:5000**

## Project Structure

```
ai-assistant/
├── app.py                  # Flask server & API integration
├── .env                    # API key (not committed)
├── .gitignore              # Ignores .env, __pycache__, etc.
├── requirements.txt        # Python dependencies
├── feedback_log.csv        # Auto-generated feedback log
├── README.md               # This file
├── templates/
│   ├── index.html          # Main application page
│   └── feedback_summary.html  # Feedback analytics
└── static/
    └── style.css           # Premium dark theme
```

## Usage

1. Select a **function** (Answer Questions / Summarize Text / Generate Creative)
2. Choose a **prompt style** from the dropdown
3. Type or paste your input
4. Click **Generate Response**
5. Rate the response with 👍 or 👎

## Tech Stack

- **Backend**: Python 3, Flask, python-dotenv
- **AI**: Anthropic Claude Sonnet API (`claude-sonnet-4-6`)
- **Frontend**: HTML5, CSS3 (custom dark theme), Vanilla JavaScript
- **Data**: CSV-based feedback logging
