from flask import Flask, redirect, url_for, render_template, session, request, make_response
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
import os
import pdfkit
import google.generativeai as genai

# Load .env
load_dotenv()
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Flask config
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "defaultkey")
app.config["SESSION_COOKIE_NAME"] = "travelbuddy_session"

# Google OAuth setup
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"
    ],
    redirect_url="/dashboard"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Travel facts generator
def generate_ai_facts():
    try:
        prompt = "Give 5 fun and short travel facts. Keep them within 25 words each."
        response = model.generate_content(prompt)
        return response.text.split("\n") if response and response.text else []
    except:
        return ["Traveling opens the mind more than any book ever could."]

# Home route
@app.route("/")
def home():
    return redirect(url_for("dashboard"))

# Dashboard
@app.route("/dashboard")
def dashboard():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        resp = google.get("/oauth2/v2/userinfo")
        session["user"] = resp.json()
    except:
        return redirect(url_for("google.login"))

    travel_facts = generate_ai_facts()
    travel_tips = [
        "Always carry a backup power bank.",
        "Use Google Maps offline when roaming.",
        "Check weather before planning your outfits."
    ]
    return render_template("dashboard.html", user=session["user"], travel_facts=travel_facts, travel_tips=travel_tips)

# AI Assistant Chat
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if not google.authorized:
        return redirect(url_for("google.login"))

    if "user" not in session:
        resp = google.get("/oauth2/v2/userinfo")
        session["user"] = resp.json()

    if "chat_history" not in session:
        session["chat_history"] = []

    ai_response = None
    if request.method == "POST":
        user_input = request.form.get("message")
        if user_input:
            try:
                convo = model.start_chat(history=session["chat_history"])
                reply = convo.send_message(user_input)
                ai_response = reply.text.strip()
                session["chat_history"].append({"role": "user", "content": user_input})
                session["chat_history"].append({"role": "assistant", "content": ai_response})
            except Exception as e:
                print("AI Chat Error:", e)
                ai_response = "AI is currently unavailable. Please try again."

    return render_template("chat.html", user=session["user"], response=ai_response)

# Trip Planner
@app.route("/plan", methods=["GET", "POST"])
def plan():
    if not google.authorized:
        return redirect(url_for("google.login"))

    if "user" not in session:
        resp = google.get("/oauth2/v2/userinfo")
        session["user"] = resp.json()

    itinerary = None
    if request.method == "POST":
        destination = request.form.get("destination", "").strip()
        days = request.form.get("days", "").strip()
        interests = request.form.get("interests", "").strip()

        if destination and days and interests:
            prompt = (
                f"Create a {days}-day itinerary for {destination} focusing on {interests}. "
                f"Include sightseeing, local experiences, and food recommendations."
            )
            try:
                response = model.generate_content(prompt)
                itinerary = response.text.strip()
            except Exception as e:
                print("Planner Error:", e)
                itinerary = "Sorry, I couldn't generate the itinerary. Please try again."
        else:
            itinerary = "Please fill all the fields to get your travel plan."

    return render_template("plan.html", user=session["user"], itinerary=itinerary)

# PDF Download
@app.route("/download_plan", methods=["POST"])
def download_plan():
    if "itinerary" not in request.form:
        return "No itinerary provided.", 400

    html = render_template("pdf_template.html", itinerary=request.form["itinerary"])
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False, configuration=config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=trip_plan.pdf"
    return response

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# Run app
if __name__ == "__main__":
    app.run(debug=True)