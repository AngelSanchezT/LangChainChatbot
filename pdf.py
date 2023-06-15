import streamlit as st
from dotenv import load_dotenv
from htmlcss import bot_template, user_template, css
from PyPDF2 import PdfReader, PdfWriter
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

def get_pdf_pages(pdf_docs):
    all_pages = []
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        with open(pdf.name, 'wb') as output_file:
            pdf_writer.write(output_file)
        text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        loader = PyPDFLoader(pdf.name)
        pdf_pages = loader.load_and_split(text_splitter=text_splitter)
        all_pages += pdf_pages
    return all_pages

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat con multiples PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    st.header("Chat con multiples PDFs :books:")
    user_question = st.text_input("Pregúntale lo que quieras a tus documentos PDFs:")
    with st.sidebar:
        st.subheader("Tus documentos")
        pdf_docs = st.file_uploader("Sube tus PDFs aquí y haz click en 'Procesar'", accept_multiple_files=True)


if __name__ == '__main__':
    main()
