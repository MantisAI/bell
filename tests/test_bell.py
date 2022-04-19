import subprocess

import pytest

from bell import bell


def test_bell():
    bell("slack webhook url")


def test_bell_command():
    command_args = "python -c \"print('hello')\"".split()
    bell("slack webhook url", *command_args)


def test_bell_bad_command():
    command_args = """ python -c "print('hello' """.split()
    with pytest.raises(subprocess.CalledProcessError):
        bell("slack webhook url", *command_args)
