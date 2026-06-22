# NEXA AI 🎯

**Your AI Placement Mentor** — an intelligent chatbot built to help students prepare for technical placements, powered by Google's Gemini API and Streamlit.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Overview

NEXA AI is a multi-mode placement preparation assistant designed for engineering and CS students. Instead of a single generic chatbot, it routes conversations through specialized prompts depending on what the student needs — DSA help, core CS concept explanations, interview question generation, or a full mock interview experience.

## 🚀 Features

| Mode | Description |
|------|-------------|
| 💬 **Ask Nexa** | General Q&A for any placement-related doubt |
| 🧩 **DSA Practice** | Get approach, time/space complexity, and code for any DSA problem |
| 📘 **Concept Explainer** | Clear explanations (with analogies) for OS, DBMS, Computer Networks, OOPs, Data Structures & Algorithms |
| 🎤 **Mock Interview** | A simulated interview for a chosen role — one question at a time, with feedback after each answer |
| ❓ **Question Generator** | Generates a custom set of interview questions (easy/medium/hard) on any topic |

### Other highlights
- 🗂️ **ChatGPT-style chat history** — multiple conversations saved in the sidebar, switch between them anytime
- 🔄 **Automatic retry logic** — gracefully handles temporary Gemini API errors (503) with up to 3 retries before showing a friendly fallback message
- 🎨 **Custom branding** — dedicated logo and avatars for a polished, professional feel
- 🧠 **Context-aware prompting** — each mode injects a tailored instruction so Gemini responds appropriately for that specific task

## 🛠️ Tech Stack

- **Frontend/UI:** [Streamlit](https://streamlit.io/)
- **AI Engine:** [Google Gemini API](https://ai.google.dev/) (`gemini-2.5-flash`)
- **Language:** Python 3.10+
- **Key libraries:** `google-genai`, `python-dotenv`

## 📂 Project Structure

```
NexaAI/
├── app.py              # Main Streamlit application
├── prompts.py           # System prompts & mode-specific instructions
├── assets/
│   ├── logo.png          # App logo (used as page icon, hero image, assistant avatar)
│   └── user.png          # User avatar
├── .env                  # Your Gemini API key (not committed to Git)
├── .gitignore
└── requirements.txt
```

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/NexaAI.git
cd NexaAI
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a free Gemini API key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in and click **"Create API key"** (no credit card required)

### 5. Configure your environment
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

### 6. Run the app
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

## 🌐 Deployment

This app is ready to deploy for free on **[Streamlit Community Cloud](https://share.streamlit.io)**:

1. Push your code to GitHub (make sure `.env` is excluded via `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app**, select this repository, and set the main file to `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```
   GEMINI_API_KEY = "your_api_key_here"
   ```
5. Click **Deploy** 🚀

## 🧭 Roadmap

- [ ] Persist chat history across sessions (file/database-backed storage)
- [ ] Export mock interview transcripts as PDF
- [ ] Add scoring/analytics for mock interview performance over time
- [ ] Support multiple AI backends (OpenAI, Claude)

## 📄 License

This project is licensed under the MIT License — feel free to use, modify, and build on it.

---

*Built as a placement preparation tool — combining prompt engineering, conversational UX, and resilient API handling.*
