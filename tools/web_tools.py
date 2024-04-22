from typing_extensions import Annotated
import subprocess


def download_web_page(
    url: Annotated[
        str,
        "The URL of the web page to download",
    ]
) -> Annotated[str, "The content of the web page"]:
    return subprocess.check_output(
        f"curl -sS {url}",
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )
