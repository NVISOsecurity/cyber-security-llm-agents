from crewai import Agent, Task
from . import config_utils
from datetime import datetime


def get_task(task_list, task_id) -> Task:  # type: ignore
    for task in task_list:
        if task["ID"] == task_id:
            return task["task"]


def get_agent(agent_list, agent_id) -> Agent:  # type: ignore
    for agent in agent_list:
        if agent["ID"] == agent_id:
            return agent["agent"]


def truncate_output_end(output):
    if len(output) > config_utils.MAX_TASK_RESPONSE_SIZE:
        return output[
            : config_utils.MAX_TASK_RESPONSE_SIZE
        ] + "... [%s characters truncated]" % (
            len(output) - config_utils.MAX_TASK_RESPONSE_SIZE
        )
    else:
        return output


def truncate_output_beginning(output):
    max_size = config_utils.MAX_TASK_RESPONSE_SIZE
    if len(output) > max_size:
        truncated_part = output[-max_size:]  # Keep the last max_size characters
        return "... [%s characters truncated] %s" % (
            len(output) - max_size,
            truncated_part,
        )
    else:
        return output


def log_agent_actions(agent_actions):
    for agent_action in agent_actions:
        # Log the agent action to the agent action log
        with open(
            config_utils.LLM_WORKING_FOLDER + "/agent_action_log.txt", "a"
        ) as log_file:
            # Add timestamp
            if ("TASK_SUCCEEDED" in str(agent_action)) or (
                "TASK_FAILED" in str(agent_action)
            ):
                current_timestamp = datetime.now()
                # Format the timestamp to include only the date and time (hours and minutes)
                formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                log_file.write("\n")
                log_file.write(formatted_timestamp)
                log_file.write("\n===================\n")
                log_file.write(str(agent_action))
                log_file.write("\n")


def replace_agent_action_log(log_file_str):
    with open(
        config_utils.LLM_WORKING_FOLDER + "/agent_action_log.txt", "w"
    ) as log_file:
        log_file.write(log_file_str)


def agent_action_log():
    with open(
        config_utils.LLM_WORKING_FOLDER + "/agent_action_log.txt", "r"
    ) as log_file:
        return log_file.read()


def wipe_agent_action_log():
    with open(
        config_utils.LLM_WORKING_FOLDER + "/agent_action_log.txt", "w"
    ) as log_file:
        log_file.write("")
