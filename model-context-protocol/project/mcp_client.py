"""
A Model Context Protocol (MCP) client implementation.

This module provides an MCPClient class to connect to and interact with
an MCP server using standard input/output (stdio) communication.
"""

import sys
import asyncio
from typing import Optional, Any
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


class MCPClient:
    """A client for interacting with an MCP server via stdio."""

    def __init__(
        self,
        command: str,
        args: list[str],
        env: Optional[dict] = None,
    ):
        """Initialize the MCPClient with server parameters."""
        self._command = command
        self._args = args
        self._env = env
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

    async def connect(self):
        """Connect to the MCP server using stdio."""
        server_params = StdioServerParameters(
            command=self._command,
            args=self._args,
            env=self._env,
        )
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        _stdio, _write = stdio_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_stdio, _write)
        )
        await self._session.initialize()

    def session(self) -> ClientSession:
        """Get the active client session."""
        if self._session is None:
            raise ConnectionError(
                "Client session not initialized or cache not populated. "
                "Call connect_to_server first."
            )
        return self._session

    async def list_tools(self) -> list[types.Tool]:
        """List available tools provided by the server."""
        return (await self.session().list_tools()).tools

    async def call_tool(
        self, tool_name: str, tool_input: dict
    ) -> types.CallToolResult | None:
        """Call a specific tool provided by the server."""
        # TODO: Call a particular tool and return the result
        return None

    async def list_prompts(self) -> list[types.Prompt]:
        """List available prompts provided by the server."""
        # TODO: Return a list of prompts defined by the MCP server
        return []

    async def get_prompt(self, prompt_name, args: dict[str, str]):
        """Get a specific prompt provided by the server."""
        # TODO: Get a particular prompt defined by the MCP server
        return []

    async def read_resource(self, uri: str) -> Any:
        """Read a specific resource from the server."""
        # TODO: Read a resource, parse the contents and return it
        return []

    async def cleanup(self):
        """Clean up resources and close the session."""
        await self._exit_stack.aclose()
        self._session = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()


# For testing
async def main():
    """Main entry point for testing the MCP client."""
    async with MCPClient(
        # If using Python without UV, update command to 'python' and remove "run" from args.
        command="uv",
        args=["run", "mcp_server.py"],
    ) as _client:
        pass


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
