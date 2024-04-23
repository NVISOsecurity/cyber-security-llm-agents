from typing_extensions import Annotated
from pypdf import PdfReader
from bs4 import BeautifulSoup

import utils.constants

import subprocess

PDF_WORKING_FOLDER = utils.constants.LLM_WORKING_FOLDER + "/pdf"


def download_pdf_report(
    url: Annotated[
        str,
        "The URL of the PDF report to download",
    ]
) -> Annotated[str, "The content of the PDF report"]:

    # Download PDF report to a local folder
    subprocess.check_output(
        f"curl -sS {url} -o {PDF_WORKING_FOLDER}/tmp.pdf",
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )

    reader = PdfReader(f"{PDF_WORKING_FOLDER}/tmp.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def download_web_page(
    url: Annotated[
        str,
        "The URL of the web page to download",
    ]
) -> Annotated[str, "The content of the web page"]:

    raw_output = subprocess.check_output(
        f"curl -sS {url}",
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )

    soup = BeautifulSoup(raw_output, "html.parser")
    return soup.get_text(strip=True)
