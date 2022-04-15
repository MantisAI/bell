# 🛎 Bell

A tool to send you alerts from your AWS instances

# Quickstart

Install

```
pip install git+https://github.com/MantisAI/bell.git
```

Use in an EC2 instance

```
bell SLACK_WEBHOOK
```

You can read how to setup a slack webbook [here](https://api.slack.com/incoming-webhooks)

The way we use this at Mantis is to setup a cron job at the instance to send
information about the status of the instance in our slack alerts channel.

# CLI

```
Usage: bell [OPTIONS] WEBHOOK_URL

Arguments:
  WEBHOOK_URL  [required]

Options:
  --help                          Show this message and exit.
```
