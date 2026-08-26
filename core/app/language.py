from fastapi import Header


def get_language(accept_language: str = Header(default="en")):
    if accept_language not in ["fa", "en"]:
        return "en"
    return accept_language
