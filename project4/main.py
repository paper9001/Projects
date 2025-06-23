import streamlit as st
import PyPDF2
import os
import io
from openai import OpenAI
from dotenv import load_dotenv
from serpapi import GoogleSearch
import PyPDF2

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY=os.getenv("SERPAPI_API_KEY")
def extract_from_pdf(pdf_file):
    pdf_extracted = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_extracted.pages:
        text += page.extract_text() + "\n"
    return text
def extract_from_file(file):
    if (file.type == "application/pdf"):
        return extract_from_pdf(io.BytesIO(file.getvalue()))
    return file.getvalue().decode("utf-8")

def ask_gpt(client, input, sources):
    prompt = f'''Please analyze this topic and provide an in depth summary on {input}.
    Focus on the following aspects:
    1. Content and clarity
    2. Details and impact of the subject
    Please provide the summary in a clear, well-structured format
    The References must copy exactly the full source text and URLs provided in {sources}'''
    response = client.chat.completions.create(
        model = "gpt-4o-mini", 
        messages = [{"role" : "system", "content" : f'''Given the topic of {input}, and these sources {sources} 
                     you will generate an academic summary as output and cite the sources used from the ones provided.
                     The References must copy exactly the full source text and URLs provided above'''},
                {"role" : "system", "content" : prompt}], 
            temperature = 0.7, max_tokens = 1000
               
        )
    return response.choices[0].message.content
def serpAPI(query):
    parameters = {
        "engine" : "google", 
        "q" : query,
        "api_key" : SERPAPI_API_KEY,
    }
    search = GoogleSearch(parameters)
    results = search.get_dict()
    return results.get("organic_results", [])

def provide_sources(results):
    sources = ""
    for i, result in enumerate(results):
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")
        sources += f"{i + 1}. {title}\n{snippet}\nURL: {link}\n\n"
    return sources
def summarize(client, file_contents):
    prompt = f"Please provide a short summary in a clear, well-structured format on the contents of {file_contents}"
    response = client.chat.completions.create(
        model = "gpt-4o-mini", 
        messages = [{"role" : "system", "content" : "You are a helpful assistant that summarizes documents."},
                {"role" : "system", "content" : prompt}], 
            temperature = 0.7, max_tokens = 1000
               
    )
    return response.choices[0].message.content



def main():
    st.set_page_config(page_title = "Wikipedia Text generation", page_icon = None, layout = "centered")
    st.title("Wikipedia Text generation")
    st.write("Ask a question regarding an academic article")
    input = st.text_input("Enter your query here else input a file into the file uploader")
    file = st.file_uploader("Choose a file (PDF or TXT)", type = ["pdf","txt"])
    button = st.button("Generate Response")
    if (button and input):
        try:
            client = OpenAI(api_key = OPENAI_API_KEY)
            serpResults = serpAPI(input)
            sources = provide_sources(serpResults)
            response = ask_gpt(client, input, sources)
            ##used serpAPI here
            st.markdown(response) #shows the response occuring on the page
        except Exception as e:
            st.error(f"An error occured {str(e)}")
    elif (button and file):
        try:
            file_contents = extract_from_file(file)
            if not file_contents.strip():
                st.error("Empty File...")
                st.stop()
            client = OpenAI(api_key = OPENAI_API_KEY)
            summary = summarize(client, file_contents)
            serpResults = serpAPI(summary)
            sources = provide_sources(serpResults)
            response = ask_gpt(client, summary, sources) # need to summarize the content since serpAPi is meant to take short queries
            ##used serpAPI here
            st.markdown(response) # same as prev comment above
        except Exception as e:
            st.error(f"An error occured {str(e)}")

if __name__ == "__main__":
    main()



