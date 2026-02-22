from mcp.server.fastmcp import FastMCP

mcp = FastMCP('WEATHER')

@mcp.tool()
async def get_weather(location:str)->str:
    """
    get the weather location
    """
    return "its always raining in this india"


if __name__ =='__main__':
    mcp.run(transport= "streamable-http")