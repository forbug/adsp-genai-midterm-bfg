from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


# Define chat model
DEFAULT_LLM = ChatOllama(model="mistral", temperature=0.1)

base_system_prompt = """
    You are an assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer
    the question. If you don't know the answer, say that you
    don't know. Use three sentences maximum and keep the
    answer concise.

    IMPORTANT RULES:
    Do not make up any information that is not in the context. 

    Context:
    {context}

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