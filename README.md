# 🚀 Project Setup Guide

## 1. Clone the Repository

```bash
git clone https://github.com/karimno3man/lang-graph-trial.git
cd lang-graph-trial
```

---

## 2. Create `.env` File

Create a `.env` file in the root directory and add the following:

```env
OPENAI_API_KEY="sk-...."

LANGSMITH_API_KEY="ls...."
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=any name
```

---

## 3. Create Virtual Environment

Make sure you are using **Python > 3.10 and < 3.14**

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### On Windows:

```bash
venv\Scripts\activate
```

### On Mac/Linux:

```bash
source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Run the Server

```bash
python server.py
```

---

## ✅ You're Ready!

Your application should now be running 🚀
