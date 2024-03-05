import copy
import json
import os

import tiktoken
from dotenv import load_dotenv
from utilities import config_utils, logging_utils

load_dotenv(verbose=True, override=True)
OPENAI_INFERENCE_MODEL_NAME = os.getenv("OPENAI_INFERENCE_MODEL_NAME", "")


MAX_GPT_RETRIES = 3
ENCODER = tiktoken.encoding_for_model("gpt-4")


def run_llm_query(full_prompt):

    logging_utils.logger.info(
        "Analyzing using GPT... [%d tokens]",
        len(ENCODER.encode(full_prompt)),
    )

    response = config_utils.AZURE_OPENAI_CLIENT.chat.completions.create(
        model=OPENAI_INFERENCE_MODEL_NAME,
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
