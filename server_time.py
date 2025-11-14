from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP(
    name = "Demo 🚀")

@mcp.tool(description="Get the current server time in ISO format.")
def get_current_time(format: str = "iso") -> str:
    return datetime.now().isoformat()

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)