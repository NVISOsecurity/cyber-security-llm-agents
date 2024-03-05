import copy
import json
import os

import tiktoken
from dotenv import load_dotenv
from openai import AzureOpenAI
from utilities import config_utils, logging_utils

load_dotenv(verbose=True, override=True)
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME", "")


MAX_GPT_RETRIES = 3
ENCODER = tiktoken.encoding_for_model("gpt-4")


def run_llm_query(query):
    full_prompt = config_utils.GENERATE_COMMANDS_PROMPT + str(query)

    logging_utils.logger.info(
        "Analyzing using GPT... [%d tokens]",
        len(ENCODER.encode(full_prompt)),
    )

    response = config_utils.AZURE_OPENAI_CLIENT.chat.completions.create(
        model=OPENAI_DEPLOYMENT_NAME,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": full_prompt,
            },
        ],
    )
    return str(response.choices[0].message.content)
