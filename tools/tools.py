from crewai_tools import PDFSearchTool, DirectoryReadTool

from .subprocess_tools import SubprocessTool
from .file_tools import FileTools
from .api_tools import APITools

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
    "read_task_history_log_tool": FileTools.read_task_history_log,
    "caldera_api_get_agents_tool": APITools.caldera_api_get_agents,
    "caldera_api_available_models_tool": APITools.caldera_api_available_models,
    "caldera_api_available_functions_tool": APITools.caldera_api_available_functions,
    "caldera_execute_command_on_agent_tool": APITools.caldera_execute_command_on_agent,
    "caldera_api_get_operation_info_tool": APITools.caldera_api_get_operation_info,
}
