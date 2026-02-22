

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from typing import TypedDict
from typing_extensions import Annotated

import os
from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('groq_api_key')
os.environ['LANGSMITH_API_KEY'] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "testproject"

# define input state schema
class State(TypedDict):
    messages : Annotated[list, add_messages]

# defining the model
llm = init_chat_model(model= "groq:llama-3.1-8b-instant")


def build_graph():

    @tool
    def add_number1(a:int, b:int)->int:
        """ add given numbers"""
        return (a+b) 

    tools = [add_number1]
    llm_tool = llm.bind_tools(tools)
    def chatbot(state:State):
        return {"messages": llm_tool.invoke(state['messages'])}
    

    # building the graph
    graph_builder = StateGraph(State)

    #add nodes
    graph_builder.add_node('llm_tool', chatbot)
    graph_builder.add_node('tools', ToolNode(tools))

    # add adges
    graph_builder.add_edge(START, 'llm_tool')
    graph_builder.add_conditional_edges('llm_tool', tools_condition)
    graph_builder.add_edge('tools', 'llm_tool')

    graph= graph_builder.compile()
    return graph

agent = build_graph()

