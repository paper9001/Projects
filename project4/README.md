Wikipedia Text Generation App

This Streamlit app allows users to generate well-structured, academic-style summaries of a topic or document. 
It uses OpenAI's GPT model and SerpAPI-powered Google search results to provide contextual, referenced outputs. 
Users can upload a PDF/TXT file or input a query directly.

---

Features

-  Accepts either a search query or uploaded document (PDF/TXT).
- Uses OpenAI GPT (via openai` Python library) to generate academic summaries.
- 🌐 Integrates with SerpAPI to fetch live search results for citations.
- 📄 Extracts text from PDFs using PyPDF2.
- 🧠 Automatically summarizes uploaded documents before sending them to SerpAPI for reference generation.

---



1. Clone the repository:
   ```bash
   git clone https://github.com/paper9001/Projects.git
   first do cd Projects
   then do cd project4
