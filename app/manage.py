import sys

from django.core.management import execute_from_command_line
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
