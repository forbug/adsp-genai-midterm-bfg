
import streamlit as st
import sys
import os
import asyncio
import nest_asyncio
import base64

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dsi_rag_qa.rag_framework.basic_graph import create_basic_workflow
from dsi_rag_qa.utils.data_ingestion_utils import load_docs_from_url, BASE_URL
from dsi_rag_qa.utils.embedding_utils import create_faiss_retriever
from dsi_rag_qa.utils.prompt_utils import base_system_prompt, create_response_chain
from langchain.callbacks.tracers.langchain import LangChainTracer
nest_asyncio.apply()

from dotenv import load_dotenv
# Load environment variables
# Ensure you have a .env file with the necessary variables
load_dotenv()

st.set_page_config(layout="wide")

@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

tracer = LangChainTracer(project_name="adsp-genai-midterm",  # Or omit to use "default"
                         )

css_md = """
<style>
    /* General Styles */
    .stApp {
        background-color: #ffffff;
        color: #4a4a4a
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: "Georgia", "Times New Roman", serif;
        color: #4a4a4a; /* Default dark color for headers */
    }
    h1 {
        color: #990000; /* Maroon for main titles */
    }

    /* Top Red Bar */
    .top-bar {
        background-color: #990000;
        height: 10px;
        width: 100%;
    }

    /* Header */
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
    }
    .header .logo img {
        height: 50px;
    }
            
    /* Links */        
    .st-key-nav a {
        margin: 0 15px;
        text-decoration: none;
        color: #4a4a4a;
        font-weight: bold;
        text-align: right;
    }
    .st-key-nav a:hover {
        text-decoration: underline;
    }

    /* Question Box Section */
    .st-key-qb {
        background-color: rgba(128, 0, 0, 0.8);
        padding: 2rem;
        max-width: 50%;
        border-radius: 5px;
        color: #ffffff;
    }

    /* Response Box Section */
    .st-key-rb {
        background-color: rgba(128, 0, 0, 0.8);
        padding: 2rem;
        border-radius: 5px;
        color: #ffffff;
    }

    /* Chat Section */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #4a4a4a;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .stButton > button {
        background-color: #990000;
        color: white;
        border-radius: 5px;
    }

</style>
"""


st.markdown(css_md, unsafe_allow_html=True)

@st.cache_resource
def load_rag_pipeline():
    """Loads the RAG pipeline and caches it."""
    docs = asyncio.run(load_docs_from_url(url=BASE_URL))
    vector_retriever, _ = create_faiss_retriever(docs)
    response_chain = create_response_chain(prompt=base_system_prompt)
    workflow = create_basic_workflow()
    return workflow, vector_retriever, response_chain

def get_response(workflow, vector_retriever, response_chain, query):
    """Invokes the RAG workflow and returns the response."""
    start_state = {
        "query": query,
        "vector_retriever": vector_retriever,
        "response_chain": response_chain,
    }
    response = workflow.invoke(start_state, config={"callbacks": [tracer]})
    return response

# Load the RAG pipeline
try:
    workflow, vector_retriever, response_chain = load_rag_pipeline()
    pipeline_loaded = True
except Exception as e:
    st.error(f"Failed to load the RAG pipeline: {e}")
    pipeline_loaded = False

# Top Red Bar
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
# Header
with col1:
    st.image("images/dsi_logo.svg", use_container_width=False)

with col2:
    st.markdown("""
        <div class="st-key-nav" style="text-align: right">
            <a href="https://datascience.uchicago.edu/about/">About</a>
            <a href="https://datascience.uchicago.edu/research/">Research</a>
            <a href="https://datascience.uchicago.edu/education/">Education</a>
            <a href="https://datascience.uchicago.edu/outreach/">Partnerships</a>
            <a href="https://datascience.uchicago.edu/about/leadership-staff/">People</a>
            <a href="https://datascience.uchicago.edu/news-events/news/">News & Events</a>
        </div>
    """, unsafe_allow_html=True)


# Question Section with Chat
with col1:
    with st.container(key="qb"):
        st.title("Elevate Your Expertise in Data Science")
        st.write("""
        The University of Chicago's MS in Applied Data Science program equips you with in-demand
        expertise and an unparalleled network of global alumni. Take the next step and start your
        application today.
        """)

        question = st.text_input("Ask a question to learn more:")
        
        button_clicked = st.button("Get Answer")
with col2:
    st.markdown('<br></br>', unsafe_allow_html=True)
    if button_clicked:
        if not pipeline_loaded:
            st.error("The RAG pipeline is not available. Please check the logs.")
        elif question:
            with st.spinner("Finding the answer..."):
                try:
                    response = get_response(workflow, vector_retriever, response_chain, question)
                    with st.container(key="rb"):
                        st.write(response["response"].replace("$", "\$"))
                    st.subheader("Sources:")
                    unique_sources = list(set([source.metadata['source'] for source in response['source_documents']]))
                    for source in unique_sources:
                        st.markdown(f"- [{source}]({source})")
                except Exception as e:
                    st.error(f"An error occurred while getting the answer: {e}")
        else:
            st.warning("Please enter a question.")

# Programs Section
st.header("Programs")
st.write("Choose from full- and part-time options in our In-Person and Online programs.")

with st.container(key="nav"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("images/in_person.jpg", use_container_width=True)
        st.subheader("In-Person Program")
        st.write("If you are an early career professional or need to complete a master's in one year, the In-Person program is for you.")
        st.markdown('<a href="https://datascience.uchicago.edu/education/masters-programs/ms-in-applied-data-science/in-person-program/">Learn More &rarr;</a>', unsafe_allow_html=True)
    with col2:
        st.image("images/online.jpg", use_container_width=True)
        st.subheader("Online Program")
        st.write("If you want 360° flexibility and the same rigorous curriculum and outcomes as an in-person degree, the Online Program is for you.")
        st.markdown('<a href="https://datascience.uchicago.edu/education/masters-programs/ms-in-applied-data-science/online-program/%20">Learn More &rarr;</a>', unsafe_allow_html=True)
    with col3:
        st.image("images/mba_ms.jpg", use_container_width=True)
        st.subheader("MBA/MS Program")
        st.write("The joint degree with UChicago's Booth School of Business is ideal for ambitious students looking to supplement their MBA studies with a cutting-edge education in data science.")
        st.markdown('<a href="https://www.chicagobooth.edu/mba/joint-degree/mba-ms-applied-data-science?sc_lang=en">Learn More &rarr;</a>', unsafe_allow_html=True)

