#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_review.settings")
    try:
        from django.core.management import execute_from_command_line
        from django.db.utils import OperationalError
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    try:
        execute_from_command_line(sys.argv)
    except OperationalError as err:
        if err.args != ('near "SCHEMA": syntax error',):
            raise err


if __name__ == "__main__":
    main()
