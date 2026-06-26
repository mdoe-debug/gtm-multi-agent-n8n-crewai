from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from .mcp_tools import get_docs_tools


class DocsWriteInput(BaseModel):
    doc_title: str = Field(..., description="Title of the document")
    markdown_content: str = Field(..., description="Markdown content to save")


class DocsWriteTool(BaseTool):
    name: str = "docs_write"
    description: str = "Save the final GTM plan as a document. Provide a doc_title and markdown_content."
    args_schema: type[BaseModel] = DocsWriteInput

    def _run(self, doc_title: str, markdown_content: str) -> str:
        underlying_tools = get_docs_tools()
        raw_tool = underlying_tools[0]
        result = raw_tool.run(title=doc_title, markdown_content=markdown_content)
        return str(result)
