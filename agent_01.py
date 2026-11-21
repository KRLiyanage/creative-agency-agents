import os
import glob
import shutil
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import SystemMessage, HumanMessage

MODEL = "gpt-5.4-nano"
db_name = "vector_db"
knowledge_base = "knowledge-base"   # knowledge-base/<company>/<file>.pdf
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=openai_api_key)
# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatOpenAI(model=MODEL, openai_api_key=openai_api_key)


def company_id(company_name):
    # "Sunny Lane Cafe" -> "sunny_lane_cafe"  (used as folder name + doc_type)
    return company_name.strip().lower().replace(" ", "_")

def load_documents():
    folders = glob.glob(f"{knowledge_base}/*")
    documents = []  # langchain document objects

    for folder in folders:
        if not os.path.isdir(folder):
            continue  # skip loose files; PDFs must be in knowledge-base/<company>/
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(folder, glob="**/*.pdf", loader_cls=PyPDFLoader)
        folder_docs = loader.load()

        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)

    return documents

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks

def save_to_vector_db(chunks):
    if os.path.exists(db_name):
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
    print(f"RAG AGENT: vector db built with {vectorstore._collection.count()} chunks", flush=True)
    return vectorstore

def build_vector_db():
    documents = load_documents()           # Part A
    chunks = split_documents(documents)    # Part B
    save_to_vector_db(chunks)              # Part C

SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable assistant for a creative digital marketing agency.
You are answering questions about our client company using their own documents.
Answer questions using only the given context. Do not use outside knowledge.
If the context does not contain the answer, say that you don't know.
Do not make up names, numbers, dates, or other details.
Context:
{context}
"""

def ask_company(company_name, question):
    print(f"RAG AGENT: asking about {company_name}: {question}", flush=True)
    vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10, "filter": {"doc_type": company_id(company_name)}})

    docs = retriever.invoke(question)
    if not docs:
        return f"No data saved for {company_name}. Ask the user to upload their company PDF."

    text = []
    for doc in docs:
        text.append(doc.page_content)
    context = "\n".join(text)

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)
    system_message = SystemMessage(content=system_prompt)
    human_message = HumanMessage(content=question)
    response = llm.invoke([system_message, human_message])
    return response.content

def save_company_pdf(pdf_path, company_name):
    print(f"RAG AGENT: saving {pdf_path} for {company_name}", flush=True)
    folder = os.path.join(knowledge_base, company_id(company_name))
    os.makedirs(folder, exist_ok=True)
    if os.path.abspath(os.path.dirname(pdf_path)) != os.path.abspath(folder):
        shutil.copy(pdf_path, folder)

    build_vector_db()

    # Analyze the company so the planner knows who the customer is
    return ask_company(company_name, "Give a short profile of this company: what they sell, "
                                     "target audience, brand voice, brand colours, unique selling points "
                                     "and any marketing goals mentioned.")
