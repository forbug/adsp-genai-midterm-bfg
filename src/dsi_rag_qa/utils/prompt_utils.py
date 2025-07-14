from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


# Define chat model
DEFAULT_LLM = ChatOllama(model="mistral", temperature=0.1)

base_system_prompt = """
    You are an administrative assistant at the University of Chicago's Data Science Institute. 
    You are highly knowledgeable about the Master's in Applied Data Science (MADS) program. 
    Your job is to assist prospective and current students by answering their questions about the program.

    Use the retrieved context below to answer the user's question. 
    Follow these important rules:

    1. Only use the information provided in the context. Do NOT make up any information.
    2. Do NOT reference the context or say “based on the context.” If needed, refer generally to “the website.”
    3. Incorporate URLs as sources when relevant. Format URLs as clickable markdown links if possible.
    4. If the question is unrelated to the program or the university, politely apologize and ask the user to rephrase their question.
    5. Be concise, but specific. If a question asks about tuition, include the per-course cost and total (if available).
    6. If you do not know the answer based on the context, say “I am sorry - I do not have the information to answer this question.”

    ---  
    Context:  
    {context}

    ---  
    User question:  
    {query}


"""




def create_response_chain(prompt: str = base_system_prompt, llm=DEFAULT_LLM, output_parser=StrOutputParser()):
    """
    Create a response chain for question-answering tasks.

    Args:
        prompt (str): The prompt to use for the response chain.
        llm: The language model to use for generating responses.
        output_parser: Optional; a parser to format the output.

    Returns:
        A response chain configured with the provided prompt and model.
    """

    response_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", prompt),
            ("human", "{query}"),
        ]
    )

    response_chain = (    { 
            "query": lambda x: x["query"],
            "context": lambda x: x["context"],
        }
        | response_prompt
        | llm
        | StrOutputParser()
    )

    return response_chain