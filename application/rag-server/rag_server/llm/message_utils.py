def generate_message(prompt):
    if type(prompt) != str:
        raise ValueError(
            f"Tried to call message generate_message with non-string input: {prompt}"
        )

    return {"role": "user", "content": [{"type": "text", "text": prompt}]}


def generate_tool_message(fn_results):
    if not isinstance(fn_results, list):
        raise ValueError(
            f"Tried to call message generate_tool_message with non-list input: {fn_results}"
        )

    return {"role": "user", "content": fn_results}
