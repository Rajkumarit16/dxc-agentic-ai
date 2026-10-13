import asyncio
from pathlib import Path

from fastmcp import Client


async def main() -> None:
    server_path = Path(__file__).with_name("gatekeeper_server.py")
    async with Client(server_path) as client:
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]
        print(f"LIST_TOOLS {'PASS' if {'route_ticket', 'needs_approval'} <= set(tool_names) else 'FAIL'}")

        route_cases = [
            ("route_ticket", {"text": "Password reset for EMP-1001"}, "Access"),
            ("route_ticket", {"text": "wifi outage and internet issue"}, "Network"),
            ("route_ticket", {"text": "Laptop screen is flickering"}, "Hardware"),
        ]

        for name, payload, expected in route_cases:
            result = await client.call_tool(name, payload)
            actual = result.data
            ok = actual == expected
            print(f"{'PASS' if ok else 'FAIL'} {name}: expected={expected!r}, actual={actual!r}")

        approval_cases = [
            ("needs_approval", {"action": "search_kb", "user_id": "EMP-1001", "hour": 9}, True),
            ("needs_approval", {"action": "grant_access", "user_id": "EMP-9999", "hour": 22}, True),
            ("needs_approval", {"action": "get_ticket", "user_id": "EMP-5555", "hour": 12}, False),
        ]

        for name, payload, expected in approval_cases:
            result = await client.call_tool(name, payload)
            actual = result.data
            ok = actual == expected
            print(f"{'PASS' if ok else 'FAIL'} {name}: expected={expected!r}, actual={actual!r}")


if __name__ == "__main__":
    asyncio.run(main())
