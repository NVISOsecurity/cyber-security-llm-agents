from crewai import Agent, Task
from . import config_utils


def get_task(task_list, task_id) -> Task:  # type: ignore
    for task in task_list:
        if task["ID"] == task_id:
            return task["task"]


def get_agent(agent_list, agent_id) -> Agent:  # type: ignore
    for agent in agent_list:
        if agent["ID"] == agent_id:
            return agent["agent"]


def truncate_output(output):
    if len(output) > config_utils.MAX_TASK_RESPONSE_SIZE:
        return output[
            : config_utils.MAX_TASK_RESPONSE_SIZE
        ] + "... [%s characters truncated]" % (
            len(output) - config_utils.MAX_TASK_RESPONSE_SIZE
        )
    else:
        return output


def log_agent_action(agent_actions):
    for agent_action in agent_actions:
        # Log the agent action to the agent action log
        with open(
            config_utils.LLM_WORKING_FOLDER + "/agent_action_log.txt", "a"
        ) as log_file:
            log_file.write(str(agent_action) + "\n-----------------------\n")


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
