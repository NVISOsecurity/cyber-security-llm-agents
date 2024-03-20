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
