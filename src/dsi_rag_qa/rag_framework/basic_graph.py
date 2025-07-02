from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class GraphState(TypedDict):
    """State for the RAG system."""
    query: str
    response: str
    source_documents: list[dict]
    vector_retriever: any
    response_chain: any


def retrieve_docs(state: GraphState) -> GraphState:
    """Generate a response based on the state."""
    
    # Retrieve relevant documents
    docs = state['vector_retriever'].invoke(state['query'])

    state['source_documents'] = docs

    return state


def generate_response(state: GraphState) -> GraphState:
    """Generate a response based on the retrieved documents."""
    response = state['response_chain'].invoke({
        "query": state['query'],
        "context": [doc.page_content for doc in state['source_documents']],
    })
    state['response'] = response
    return state



def create_basic_workflow() -> StateGraph:
    """Create a basic workflow for the RAG system."""
    

    response_builder = StateGraph(GraphState)
    response_builder.add_node("retrieve_docs", retrieve_docs)
    response_builder.add_node("generate_response", generate_response)

    response_builder.add_edge(START, "retrieve_docs")
    response_builder.add_edge("retrieve_docs", "generate_response")
    response_builder.add_edge("generate_response", END)

    response_workflow = response_builder.compile()

    return response_workflow