from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain.agents import create_agent

import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
groq_API = os.getenv('groq_api_key')

async def main():
    client = MultiServerMCPClient(
       { 
           "math":{
            "command" : "python",
            "args" : ["mathserver.py"],
            "transport": "stdio",
        },
        "weather": {
                    "url": "http://localhost:8000/mcp",
                    "transport": "streamable_http",
                }
                } )

    tools = await client.get_tools()
    model = ChatGroq(
            model="llama-3.1-8b-instant",
        )
    
    agent = create_agent(model= model, tools= tools)

    math_response =  await agent.ainvoke(
        input= {"messages": [{"role": "user", "content": "what's (3+5) x 12 ?"}]}
        )
    print("math_repsone :",  math_response['messages'][-1].content)

    weather_response =  await agent.ainvoke(
        input= {"messages": [{"role": "user", "content": "what is weather in india"}]}
        )
    print("weather_response :",  weather_response['messages'][-1].content)

    for msg in weather_response["messages"]:
        print(type(msg))
        print(msg)
        print("------")
asyncio.run(main())