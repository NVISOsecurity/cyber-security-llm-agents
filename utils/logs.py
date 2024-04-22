import pandas as pd
import sqlite3
import json


def get_log(dbname="logs.db", table="chat_completions"):
    con = sqlite3.connect(dbname)
    query = f"SELECT * from {table}"
    cursor = con.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return data


def str_to_dict(s):
    return json.loads(s)


def print_usage_statistics(logging_session_id):
    log_data = get_log()
    log_data_df = pd.DataFrame(log_data)

    log_data_df["total_tokens"] = log_data_df.apply(
        lambda row: str_to_dict(row["response"])
        .get("usage", {})
        .get("total_tokens", None),
        axis=1,
    )

    log_data_df["request"] = log_data_df.apply(
        lambda row: str_to_dict(row["request"])["messages"][0]["content"], axis=1
    )

    # Sum totoal tokens for all sessions
    total_tokens = log_data_df["total_tokens"].sum()

    # Sum total cost for all sessions
    total_cost = log_data_df["cost"].sum()

    # Total tokens for specific session
    session_tokens = log_data_df[log_data_df["session_id"] == logging_session_id][
        "total_tokens"
    ].sum()
    session_cost = log_data_df[log_data_df["session_id"] == logging_session_id][
        "cost"
    ].sum()

    print("==============================")
    print(
        "Total tokens for all sessions: "
        + str(total_tokens)
        + ", total cost: "
        + str(round(total_cost, 4))
    )
    print(
        "Total tokens for session "
        + str(logging_session_id)
        + ": "
        + str(session_tokens)
        + ", cost: "
        + str(round(session_cost, 4))
    )
