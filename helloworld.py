from mcp.server.fastmcp import FastMCP

mcp = FastMCP("HelloWorld")

@mcp.tool()
def helloworld() -> str:
    """hello world"""
    return "hello world for mcp from 吉林大学通信工程学院 525实验室 GuanYingqi 20251003 - Updated!"

if __name__ == "__main__":
    mcp.run(transport="stdio")