# 🤖 Dynamic AI Chatbot System

An **AI-powered conversational chatbot system** built using **FastAPI, NLP, and LLM integration** that enables intelligent user interaction through natural language conversations.

This project demonstrates how modern backend technologies, NLP pipelines, and conversational AI models can be combined to build a **scalable and interactive chatbot platform** with features like **user authentication, conversation memory, chat history, feedback collection, and analytics dashboard**.

---

# 🚀 Project Overview

The **Dynamic AI Chatbot System** is designed to simulate human-like conversations by analyzing user input, identifying intent and sentiment, and generating appropriate responses.

The system integrates:

- **Rule-based NLP responses**
- **LLM-based fallback responses (Llama3 via Ollama)**
- **Conversation memory management**
- **User authentication and session handling**
- **Chat history tracking**
- **Feedback collection**
- **Analytics dashboard for chatbot performance**

Each chat session is handled as a **separate conversation thread**, ensuring contextual understanding while preventing cross-chat interference.

---

# 🧠 Key Features

### 💬 Conversational AI
- Natural language query handling
- Intent detection and sentiment analysis
- Rule-based responses
- LLM-powered fallback responses using **Llama3**

### 🧾 Chat Management
- Multi-conversation chat threads
- Chat history stored in database
- Sidebar conversation navigation
- Context-aware responses within a conversation

### 🔐 User Authentication
- User registration
- Email OTP verification
- Secure login system
- Password reset functionality

### 📊 Analytics Dashboard
- Chat usage statistics
- Intent distribution visualization
- Sentiment distribution
- Feedback analytics

### 👍 Feedback System
- Users can rate chatbot responses
- Feedback stored and analyzed
- Improves chatbot performance insights

### 🎨 Modern Chat Interface
- Chat bubbles UI
- Conversation sidebar
- User profile display
- Real-time interaction

---

# 🏗 System Architecture
```
User
 │
 │ Chat Interface
 ▼
Frontend (HTML / CSS / JavaScript)
 │
 │ REST API Requests
 ▼
FastAPI Backend
 │
 ├── Authentication Module
 │      • User Signup
 │      • Login
 │      • OTP Verification
 │      • Password Reset
 │
 ├── Chat Orchestrator
 │      • Controls chat pipeline
 │      • Handles conversation flow
 │
 ├── NLP Processing Module
 │      • Intent Classification
 │      • Entity Recognition
 │      • Sentiment Analysis
 │
 ├── Response Engine
 │      ├ Rule-Based Response System
 │      └ LLM Response Generator
 │            (Ollama + Llama3)
 │
 ├── Memory Manager
 │      • Conversation Context Builder
 │      • Chat History Retrieval
 │
 ├── Feedback System
 │      • Like / Dislike response feedback
 │
 └── Analytics Engine
        • Chat usage statistics
        • Intent distribution
        • Sentiment distribution
        • Feedback insights
                 │
                 ▼
           SQLite Database
                 │
                 ├── Users
                 ├── Chat History
                 ├── Conversations
                 └── Feedback
```

---

# ⚙️ Technology Stack

### Backend
- **FastAPI**
- Python
- Pydantic
- Uvicorn

### Frontend
- HTML
- CSS
- JavaScript

### AI & NLP
- SpaCy
- NLTK
- Scikit-learn
- Llama3 (via Ollama)

### Database
- SQLite

### Visualization
- Matplotlib
- Seaborn

---

# 📂 Project Structure

```
dynamic-ai-chatbot/
│
├── app/
│   │
│   ├── main.py                 # FastAPI application entry point
│   │
│   ├── api/
│   │   └── routes.py           # Chat API endpoints
│   │
│   ├── auth/
│   │   ├── auth_routes.py      # Authentication APIs
│   │   ├── otp_service.py      # OTP verification
│   │   └── security.py         # Password hashing & JWT
│   │
│   ├── core/
│   │   ├── chat_orchestrator.py # Main chatbot pipeline
│   │   └── memory.py            # Conversation context builder
│   │
│   ├── db/
│   │   ├── database.py         # Database connection
│   │   └── chat_queries.py     # Chat database operations
│   │
│   ├── models/
│   │   └── llm.py              # Llama3 integration (Ollama)
│   │
│   ├── nlp/
│   │   ├── processor.py        # NLP pipeline controller
│   │   ├── intent.py           # Intent classification
│   │   ├── sentiment.py        # Sentiment analysis
│   │   └── ner.py              # Named entity recognition
│   │
│   └── analytics/
│       ├── routes.py           # Analytics API endpoints
│       └── service.py          # Dashboard data processing
│
│
├── frontend/
│   │
│   ├── css/
│   │   └── app.css             # Chat UI styling
│   │
│   ├── js/
│   │   ├── chat.js             # Chat UI logic
│   │   ├── api.js              # API request handler
│   │   └── dashboard.js        # Analytics dashboard
│   │
│   └── html/
│       ├── login.html
│       ├── signup.html
│       ├── verify_otp.html
│       └── app.html            # Main chatbot interface
│
│
├── data/
│   └── chatbot.db              # SQLite database
│
├── requirements.txt            # Python dependencies
│
└── README.md                   # Project documentation


```

---

# 🧪 Chat Processing Pipeline

When a user sends a message:

1️⃣ User sends a message via frontend UI  
2️⃣ Message is sent to **FastAPI backend**  
3️⃣ NLP module processes the message:
   - Intent detection
   - Entity extraction
   - Sentiment analysis

4️⃣ If intent matches predefined rules → return rule-based response  
5️⃣ If intent is **Fallback** → generate response using **Llama3 LLM**  
6️⃣ Chat is stored in database with conversation ID  
7️⃣ Response is returned to frontend and displayed in chat UI

---

# 🖥 Installation Guide

## 1️⃣ Clone the repository

```
git clone https://github.com/yourusername/dynamic-ai-chatbot.git
cd dynamic-ai-chatbot
```

## 2️⃣ Create virtual environment
```
python -m venv venv
```
Activate it:

Windows
```
venv\Scripts\activate
```
Linux / Mac
```
source venv/bin/activate
```
## 3️⃣ Install dependencies
```
pip install -r requirements.txt
```
## 4️⃣ Install NLP models
```
python -m spacy download en_core_web_sm
```
## 5️⃣ Install Ollama
Download from:
```
https://ollama.com⁠
```
Then pull the Llama3 model:
```
ollama pull llama3
```
## 6️⃣ Start backend server
```
uvicorn app.main:app --reload
```
Server runs at:
```
http://127.0.0.1:8000
```
Swagger API documentation:
```
http://127.0.0.1:8000/docs
```
## 7️⃣ Launch frontend
Open:
```
frontend/app.html
```
in your browser.

---

## 📊 Analytics Dashboard

The dashboard provides insights such as:

- Total chats  
- Daily chat trends  
- Intent distribution  
- Sentiment distribution  
- User feedback statistics  

These analytics help monitor chatbot performance and user engagement.

---

## 🧩 Future Improvements

- Context-aware long conversation memory  
- Voice-based chatbot interaction  
- Chat export functionality  
- Multi-language support  
- Model fine-tuning with feedback data  

---

## 📜 License

This project is developed for educational and internship purposes.
