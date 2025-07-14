# 🤖 Reddit Persona Extractor

Generate detailed psychological and behavioral personas from any public Reddit user's activity — powered by GPT and deployed via Streamlit.

![Streamlit](https://img.shields.io/badge/Deployed%20with-Streamlit-red?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square)
![OpenAI](https://img.shields.io/badge/LLM-GPT--4-lightgreen?style=flat-square)

---

## 🚀 Overview

This tool scrapes a Reddit user's public posts and comments, analyzes their language and behavior using GPT, and outputs a **detailed user persona**. The application can be used through a **command-line interface** or via an intuitive **Streamlit web app**.

Ideal for:
 User research
 Behavioral analytics
 Social profiling
 LLM-powered persona generation

---

## ✨ Features

- 🔍 Scrapes posts & comments from any Reddit profile  
- 🧠 Generates persona traits using OpenAI GPT (with citations)  
- 📄 Outputs clean, human-readable text files  
- 🖥️ Built-in web app using Streamlit  
- ⚙️ Easy setup and extensible codebase  
- ✅ Follows PEP8 and best practices  

---

## 🛠️ Tech Stack

| Component       | Tool |
|----------------|------|
| Backend         | Python 3.10+ |
| Reddit API      | [PRAW](https://praw.readthedocs.io/) |
| LLM Integration | [GEMINI-PRO](https://airstudio.google.com/) |
| UI              | [Streamlit](https://streamlit.io) |
| Env Management  | `python-dotenv` |


### 🔐 .env Configuration

Create a `.env` file in the root directory and add the following:

```env
# Reddit API (required for scraping)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=PersonaScraper/1.0 by u/your_reddit_username

# Gemini API (required for persona generation)
GEMINI_API_KEY=your_gemini_api_key
