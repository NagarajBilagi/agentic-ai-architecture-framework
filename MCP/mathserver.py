from mcp.server.fastmcp import FastMCP


mcp = FastMCP('MATH')

@mcp.tool()
def add(a:int,b:int):
    """add two numbers"""
    return (a+b)


@mcp.tool()
def multiply(a:int, b:int):
    """ multiply two numbers"""
    return (a*b)

if __name__ == "__main__":
    mcp.run(transport='stdio')     # using stdio to define standard input/output methods to recive and respond to tool function calls