from crewai_tools import PDFSearchTool, DirectoryReadTool
from .subprocess_tools import SubprocessTool

tools_dict = {
    "pdf_tool": PDFSearchTool(
        pdf="./knowledge_base/threat-intelligence/TLP-CLEAR-CB-24-03.pdf"
    ),
    "docs_tool": DirectoryReadTool(directory="./threat-intelligence"),
    "subprocess_tool": SubprocessTool(),
}
