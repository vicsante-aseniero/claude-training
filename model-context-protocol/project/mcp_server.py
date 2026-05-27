"""
A Model Context Protocol (MCP) server for document management.

This module provides tools to read and edit virtual document contents
using the FastMCP framework.
"""

from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": (
        "This deposition covers the testimony "
        "of Angela Smith, P.E."
    ),
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": (
        "These financials outline the project's "
        "budget and expenditures."
    ),
    "outlook.pdf": (
        "This document presents the projected "
        "future performance of the system."
    ),
    "plan.md": (
        "The plan outlines the steps for the "
        "project's implementation."
    ),
    "spec.txt": (
        "These specifications define the technical "
        "requirements for the equipment."
    ),
}


@mcp.tool(
    name="read_document",
    description="Read the contents of a document",
)
def read_document(
    doc_id: str = Field(
        description="The ID of the document to read",
        enum=list(docs.keys())
    )
):
    """Read the contents of a specific document by its ID."""
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document",
)
def edit_document(
    doc_id: str = Field(
        description="The ID of the document to edit",
        enum=list(docs.keys())
    ),
    old_contents: str = Field(
        description=(
            "The old contents of the document. "
            "Must match exactly, including whitespace"
        )
    ),
    new_contents: str = Field(description="The new contents of the document"),
):
    """Edit the contents of a specific document."""
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_contents, new_contents)
    return docs[doc_id]


# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
