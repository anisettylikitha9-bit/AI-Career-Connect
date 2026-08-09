<<<<<<< HEAD
# 🤖 AI Career Connect

**AI Career Connect** is an intelligent, web-based career assistant built with **Flask**, **SQLite**, and **Mistral AI**. It helps users get career advice, analyze resumes, practice interview questions, create 6-month career roadmaps, and interact using both text and voice!

---

## ✨ Features

1. 🔐 **User Registration & Login**: Secure account creation with encrypted passwords.
2. 📊 **Dynamic Dashboard**: View total chats, analyzed resumes, interview preps, and recent activity.
3. 💬 **AI Chat Assistant**: Real-time conversational AI powered by Mistral AI to give career guidance.
4. 🎙️ **Speech to Text (STT)**: Ask career questions directly using your microphone.
5. 🔊 **Text to Speech (TTS)**: Listen to AI career responses read aloud in clear audio.
6. 📄 **Resume Analyzer**: Upload PDF resumes to get instant AI scoring, strengths, weaknesses, and tips.
7. ❓ **Interview Question Generator**: Generate tailored technical & behavioral interview questions with answer hints for any job role.
8. 🗺️ **Career Roadmap Generator**: Generate a personalized 6-month step-by-step career development plan.
9. 🗃️ **SQLite Database**: Automatically saves all chat history, resume analyses, and interview preps.

---

## 🛠️ Tech Stack

| Component | Technology Used |
|---|---|
| **Backend** | Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF |
| **AI Model** | Mistral AI API (`mistral-large-latest`) |
| **Database** | SQLite (with SQLAlchemy ORM) |
| **Speech Processing** | SpeechRecognition (STT), gTTS (TTS) |
| **Frontend Styling** | HTML5, CSS3, JavaScript, Bootstrap 5 |

---

## 📁 Project Structure

```text
AI_Career_connect/
├── run.py                 # 🏁 Application startup entry point
├── config.py              # ⚙️ Central configuration (Dev/Prod/Test)
├── requirements.txt       # 📦 Project Python package dependencies
├── .env                   # 🔐 Secret environment variables (API Key)
├── README.md              # 📖 Project documentation (This file)
│
├── app/                   # 🏗️ Application Core
│   ├── __init__.py        # 🏭 Flask Application Factory & Blueprints
│   ├── models.py          # 🗃️ Database schema (User, ChatHistory, Resume, etc.)
│   ├── forms.py           # 📋 Web input forms (WTForms)
│   │
│   ├── routes/            # 🛣️ Blueprint Page Handlers
│   │   ├── auth.py        # Login & Register routes
│   │   ├── chat.py        # AI Chat routes
│   │   ├── dashboard.py   # Dynamic Dashboard routes
│   │   ├── resume.py      # Resume Upload & Analyzer routes
│   │   ├── interview.py   # Interview Question Generator routes
│   │   ├── roadmap.py     # Career Roadmap routes
│   │   └── speech.py      # STT and TTS API routes
│   │
│   ├── services/          # 🧠 Business Logic & External APIs
│   │   ├── ai_service.py     # Mistral AI integration wrapper
│   │   └── speech_service.py # Speech-to-Text & Text-to-Speech logic
│   │
│   ├── templates/         # 🎨 HTML Page Layouts (Bootstrap 5)
│   └── static/            # 📁 Static files (CSS, JS, Uploaded Files)
│
└── tests/                 # 🧪 Automated Test Suite (Pytest)
```

---

## 🚀 Quick Setup & Installation

### Step 1: Clone or Open the Project
Open terminal in the project directory:
```powershell
cd c:\Users\NIKKI\Desktop\AI_Career_connect
```

### Step 2: Set Up Virtual Environment & Dependencies
```powershell
# Create virtual environment
python -m venv venv

# Install dependencies
.\venv\Scripts\pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a file named `.env` in the root folder with the following contents:
```ini
SECRET_KEY=dev-secret-key-change-in-production
MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-large-latest
DATABASE_URL=sqlite:///ai_career_connect.db
```

### Step 4: Run the Application
```powershell
.\venv\Scripts\python.exe run.py
```
Open your browser and visit: **http://127.0.0.1:5000**

---

## 🧪 Running Unit Tests

Run the automated test suite to verify all routes, models, and auth functions:

```powershell
.\venv\Scripts\python.exe -m pytest
```

---

## 💡 License
This project is open-source and built for AI Career Connect.
=======
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.
>>>>>>> 23cc4f0c6ce394568f312abe518fb026e127e639
