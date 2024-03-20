from crewai_tools import PDFSearchTool, DirectoryReadTool
from langchain_community.tools import ShellTool

from .subprocess_tools import SubprocessTool
from .file_tools import FileTools
from .api_tools import APITools

from utilities import config_utils

tools_dict = {
    "pdf_tool": PDFSearchTool(
        pdf="./knowledge_base/threat-intelligence/NVISO_SparkCockpit_SparkTar_n-day_backdoors.pdf"
    ),
    "knowledge_directory_tool": DirectoryReadTool(
        directory="./" + config_utils.LLM_KNOWLEDGE_FOLDER
    ),
    "working_directory_tool": DirectoryReadTool(
        directory="./" + config_utils.LLM_WORKING_FOLDER
    ),
    "subprocess_tool": SubprocessTool(),
    "write_file_tool": FileTools.write_file,
    "api_request_tool": APITools.api_request,
    "shell_tool": ShellTool(),
}
