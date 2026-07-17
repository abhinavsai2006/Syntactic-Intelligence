import os
from PIL import Image, ImageDraw, ImageFont

def draw_flowchart():
    # Image dimensions
    w, h = 1000, 700
    img = Image.new("RGB", (w, h), (248, 250, 252)) # Slate-50 background #f8fafc
    draw = ImageDraw.Draw(img)
    
    # Colors
    slate_900 = (15, 23, 42)
    slate_500 = (100, 116, 139)
    slate_200 = (226, 232, 240)
    indigo = (79, 70, 229)
    teal = (14, 116, 144)
    white = (255, 255, 255)

    # Drawing helper: rounded card with header
    def draw_card(x1, y1, x2, y2, title, desc, border_color):
        # Draw base card
        draw.rounded_rectangle([x1, y1, x2, y2], radius=8, fill=white, outline=border_color, width=2)
        # Draw header bar
        draw.rounded_rectangle([x1, y1, x2, y1 + 30], radius=8, fill=indigo, outline=indigo, width=1)
        draw.rectangle([x1, y1 + 15, x2, y1 + 30], fill=indigo) # flatten bottom corners of header
        
        # Text
        draw.text((x1 + 12, y1 + 7), title, fill=white)
        # Splitting desc into lines
        y_offset = y1 + 42
        for line in desc:
            draw.text((x1 + 12, y_offset), line, fill=slate_900)
            y_offset += 16

    # Drawing helper: connecting arrow
    def draw_arrow(x1, y1, x2, y2, text=""):
        draw.line([x1, y1, x2, y2], fill=slate_500, width=2)
        # Arrowhead
        if x1 == x2: # Vertical arrow
            draw.polygon([x2 - 5, y2 - 8, x2 + 5, y2 - 8, x2, y2], fill=slate_500)
            if text:
                draw.text((x2 + 8, (y1 + y2)/2 - 8), text, fill=slate_500)
        else: # Horizontal arrow
            draw.polygon([x2 - 8, y2 - 5, x2 - 8, y2 + 5, x2, y2], fill=slate_500)
            if text:
                draw.text(((x1 + x2)/2 - 30, y2 - 18), text, fill=slate_500)

    # 1. UI Selection Card
    draw_card(40, 40, 290, 160, "1. Frontend Selection", [
        "User chooses Function:",
        " - Q&A, Summarizer, Creative",
        "Selects style dropdown",
        "Enters input text prompt"
    ], slate_200)

    # 2. AJAX Dispatch Arrow
    draw_arrow(290, 100, 390, 100, "fetch() POST")

    # 3. Flask Server Router Card
    draw_card(390, 40, 640, 160, "2. Flask Server (app.py)", [
        "Endpoint: POST /generate",
        "Retrieves prompts template",
        "Formats payload with input",
        "Loads .env variables"
    ], slate_200)

    # 4. NVIDIA NIM API Call Arrow
    draw_arrow(640, 100, 740, 100, "API Request")

    # 5. NVIDIA Model API Card
    draw_card(740, 40, 960, 160, "3. NVIDIA NIM LLM", [
        "Model Llama-3.1-8b-instruct",
        "Processes system prompt",
        "Generates structured response",
        "Returns JSON payload"
    ], slate_200)

    # 6. Response pipeline back
    draw_arrow(850, 160, 850, 240)
    # Intermediate line running left
    draw.line([850, 240, 165, 240], fill=slate_500, width=2)
    draw_arrow(165, 240, 165, 300, "JSON Response")

    # 7. UI Markdown Render Card
    draw_card(40, 300, 290, 420, "4. UI Render & Copy", [
        "Renders markdown in UI card",
        "Offers Copy to Clipboard",
        "Triggers feedback panel",
        "Outputs final solution"
    ], slate_200)

    # 8. Feedback Logging arrow
    draw_arrow(290, 360, 390, 360, "Thumbs Up/Down")

    # 9. CSV Logger Card
    draw_card(390, 300, 640, 420, "5. Thread-Locked CSV", [
        "Endpoint: POST /feedback",
        "threading.Lock() primitive",
        "Appends rating to logger:",
        " feedback_log.csv"
    ], slate_200)

    # 10. Dashboard analytics arrow
    draw_arrow(640, 360, 740, 360, "Analytics dashboard")

    # 11. Dashboard card
    draw_card(740, 300, 960, 420, "6. Feedback Summary", [
        "Endpoint: GET /feedback-summary",
        "Reads aggregate feedback logs",
        "Calculates satisfaction rates",
        "Renders visual performance"
    ], slate_200)

    # Title Banner at the bottom
    draw.rounded_rectangle([40, 520, 960, 640], radius=8, fill=slate_900, outline=slate_900, width=1)
    draw.text((80, 545), "SYNTACTIC INTELLIGENCE SYSTEM PIPELINE FLOWCHART", fill=white, font=None)
    draw.text((80, 575), "Details the request-response lifecycle from initial user input selection to NVIDIA NIM API model pipelines", fill=slate_500, font=None)
    draw.text((80, 595), "and thread-safe feedback metrics aggregation.", fill=slate_500, font=None)

    img.save("flowchart.png")
    print("Flowchart generated successfully.")

if __name__ == "__main__":
    draw_flowchart()
