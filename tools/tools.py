from crewai_tools import PDFSearchTool, DirectoryReadTool
from langchain_community.tools import ShellTool

from .subprocess_tools import SubprocessTool
from .file_tools import FileTools
from .api_tools import APITools
from .coordinator_tools import CoordinatorTools

from utilities import config_utils

tools_dict = {
    "knowledge_directory_tool": DirectoryReadTool(
        directory="./" + config_utils.LLM_KNOWLEDGE_FOLDER
    ),
    "working_directory_tool": DirectoryReadTool(
        directory="./" + config_utils.LLM_WORKING_FOLDER
    ),
    "subprocess_tool": SubprocessTool(),
    "search_pdf_tool": PDFSearchTool(),
    "read_pdf_tool": FileTools.read_pdf_content,
    "write_file_tool": FileTools.write_file,
    "caldera_api_get_agents_tool": APITools.caldera_api_get_agents,
    "caldera_api_available_models_tool": APITools.caldera_api_available_models,
    "caldera_api_available_functions_tool": APITools.caldera_api_available_functions,
    "caldera_update_ability_api_request": APITools.caldera_update_ability_api_request,
    "caldera_api_request_tool": APITools.caldera_api_request,
    "shell_tool": ShellTool(),
    "retrieve_progress_tool": CoordinatorTools.retrieve_progress_file,
    "write_progress_tool": CoordinatorTools.add_task_results_to_progress_file,
}
