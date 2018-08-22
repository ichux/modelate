import os
import re


TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(TESTS_DIR, '..'))
CONFIG = os.path.join(PARENT_DIR, 'bash', 'dev', 'variables.sh')


def set_env_variables():
    """
    Sets all the necessary environment variables.
    :return:
    """
    if os.path.exists(CONFIG):
        pattern = re.compile("export (\w+)(?:=)(.*)$", re.MULTILINE)

        with open(CONFIG, "r") as file_in:
            for key, value in re.findall(pattern, file_in.read()):
                os.environ[key] = value
