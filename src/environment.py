import argparse
import os
import logging

### @package environment
#
# Interacitons with the environment variables.
#


def load_env(key: str, default: str, args_dict=None) -> str:
    """!
    os.getenv() wrapper that handles the console-args as well as env-variables\n
    Returns default value when nothing else is given.\n
    Prefers args over env-variables

    @param key: name of env variable to load
    @param default: default value if variable couldn't be loaded
    @param args_dict: dict containing the args passed in via console arguments
    @return value of env variable or default value
    """
    if args_dict is not None:
        arg_val = args_dict.get(key.lower(), None)  # args are lowercase but have the same name
        if arg_val:
            return arg_val

    value = os.getenv(key)
    if value:
        return value

    logger.warning(f"Can't load env-variable for: '{key}' - falling back to DEFAULT {key}='{default}'")
    return default


logger = logging.getLogger('my-bot')

# setup argparse and register parameters
parser = argparse.ArgumentParser("a quiz bot for discord")
parser.add_argument("-t", "--token", help="Token for the bot if not set using env variable", required=False)
parser.add_argument("-p", "--prefix", help="Prefix the bot listens to", required=False)
parser.add_argument("-v", "--version", help="Version of the bot that is running", required=False)
parser.add_argument("-l", "--language", help="Language dates are processed in", required=False)
parser.add_argument("-n", "--owner_name", help="Name of the bot owner e.g. pi#3141", required=False)
parser.add_argument("-i", "--owner_id", help="Discord-ID of the bot owner", required=False)
parser.add_argument('-q', "--questions", help="Path to the json with questions", required=False)
parser.add_argument("-d", "--allowed_delta", "--delta",
                    help="Time (seconds) the questions stay open after a question was answered", required=False)

_args = parser.parse_args()
_args_dict = vars(_args)

TOKEN = load_env("TOKEN", "", args_dict=_args_dict)  # reading in the token from config.py file

# loading optional env variables
PREFIX = load_env("PREFIX", "q!", args_dict=_args_dict)
VERSION = load_env("VERSION", "unknown", args_dict=_args_dict)  # version of the bot
LANGUAGE = load_env("LANGUAGE", "en", args_dict=_args_dict)  # language for date parsing
OWNER_NAME = load_env("OWNER_NAME", "unknown", args_dict=_args_dict)   # owner name with tag e.g. pi#3141
OWNER_ID = int(load_env("OWNER_ID", "100000000000000000", args_dict=_args_dict))  # discord id of the owner
QUIZ_FILE = load_env("QUESTIONS", "data/questions.json", args_dict=_args_dict)
ALLOWED_DELTA = float(load_env("ALLOWED_DELTA", "2.0", args_dict=_args_dict))
