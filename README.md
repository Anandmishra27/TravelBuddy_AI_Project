# TravelBuddy AI Project

Your smart travel companion powered by AI — plan trips, chat with an assistant, and download itineraries as PDFs.

## Features

- *AI Assistant Chat* – Ask travel questions, get real-time suggestions using Google Gemini AI.
- *Trip Planner* – Generate multi-day trip itineraries based on destination and interests.
- *PDF Export* – Download your AI-generated itinerary instantly as a styled PDF.
- *Secure Google Login* – Sign in using your Google account with OAuth 2.0.

## Tech Stack

- *Backend:* Flask, Google OAuth, Google Generative AI
- *Frontend:* HTML, Tailwind CSS, Jinja2 templates
- *Extras:* pdfkit for PDF generation, dotenv for environment secrets

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Anandmishra27/TravelBuddy_AI_Project.git
cd TravelBuddy_AI_Project

2. Create a virtual environment and activate it

python -m venv venv
venv\Scripts\activate  # On Windows

3. Install dependencies

pip install -r requirements.txt

4. Create a .env file with your credentials

FLASK_SECRET_KEY=your_secret_key
GOOGLE_OAUTH_CLIENT_ID=your_google_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_google_client_secret
GEMINI_API_KEY=your_gemini_api_key

5. Run the Flask app

python app.py

Visit the app at: http://127.0.0.1:5000


---

Future Improvements

Voice-based AI assistant

Live travel deals integration

Multi-user dashboard & itinerary storage

Author

GitHub: Anandmishra27

---