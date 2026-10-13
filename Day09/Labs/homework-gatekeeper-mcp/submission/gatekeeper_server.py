import argparse

from fastmcp import FastMCP

from gatekeeper import needs_approval as gatekeeper_needs_approval
from gatekeeper import route as gatekeeper_route

mcp = FastMCP("AskIT Gatekeeper")


@mcp.tool(
    description="Route a support ticket description to the correct team based on the keywords it contains."
)
def route_ticket(text: str) -> str:
    return gatekeeper_route(text)


@mcp.tool(
    description="Decide whether a requested action requires approval for the given user at the specified hour."
)
def needs_approval(action: str, user_id: str, hour: int) -> bool:
    return bool(gatekeeper_needs_approval(action, user_id, hour)["approval"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AskIT Gatekeeper MCP server")
    parser.add_argument("--http", action="store_true", help="Run the server over HTTP on port 8778")
    args = parser.parse_args()

    if args.http:
        mcp.run(transport="http", host="127.0.0.1", port=8778, show_banner=False)
    else:
        mcp.run(transport="stdio", show_banner=False)
