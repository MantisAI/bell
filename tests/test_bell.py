import subprocess

import pytest

from bell import bell


@pytest.fixture
def slack_webhook_url():
    return "http://www.slack.com"


def test_bell(slack_webhook_url):
    bell(slack_webhook_url)


def test_bell_command(slack_webhook_url):
    command_args = "python -c \"print('hello')\"".split()
    bell(slack_webhook_url, False, *command_args)


def test_bell_bad_command(slack_webhook_url):
    command_args = """ python -c "print('hello' """.split()
    with pytest.raises(AttributeError):
        bell(slack_webhook_url, False, *command_args)
