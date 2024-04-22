from crewai_tools import (
    PDFSearchTool,
    DirectoryReadTool,
    GithubSearchTool,
    ScrapeWebsiteTool,
)

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
    "website_scrape_tool": ScrapeWebsiteTool(),
    "mimikatz_github_search_tool": GithubSearchTool(
        github_repo="https://github.com/gentilkiwi/mimikatz",
        content_types=["code"],
        gh_token=config_utils.GITHUB_TOKEN,
    ),
    "caldera_api_available_models_tool": APITools.caldera_api_available_models,
    "caldera_api_available_functions_tool": APITools.caldera_api_available_functions,
    "caldera_execute_command_on_agent_tool": APITools.caldera_execute_command_on_agent,
}