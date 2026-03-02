import os
from dotenv import load_dotenv
import tiktoken
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

load_dotenv(".env")
os.environ['OPENAI_API_KEY'] = os.environ.get('API_KEY')
MODEL_NAME = "gpt-4o-mini"

class State(TypedDict):
    messages: Annotated[list, add_messages]

def build_graph():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "data", "pdf")

    loader = DirectoryLoader(pdf_path, glob="./*.pdf", loader_cls=PyPDFLoader)
    
    documents = loader.load()
    
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        tiktoken.encoding_for_model(MODEL_NAME).name
    )
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    vectorstore = Chroma.from_documents(texts, embeddings)
    retriever_tool = create_retriever_tool(
        vectorstore.as_retriever(),
        "dog_medical_procedurer",
        "반려견의 건강, 질병, 사내 반려견 동반 규정 등을 검색합니다."
    )

    search_tool = TavilySearchResults(max_results=2)
    tools = [retriever_tool, search_tool]

    llm = ChatOpenAI(model=MODEL_NAME).bind_tools(tools)
    
    def chatbot(state: State):
        return {"messages": [llm.invoke(state["messages"])]}

    builder = StateGraph(State)
    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_conditional_edges("chatbot", tools_condition)
    builder.add_edge("tools", "chatbot")
    builder.set_entry_point("chatbot")

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

app_graph = build_graph()