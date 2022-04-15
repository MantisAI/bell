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

# Cron

This tool is intended to be used with a scheduler like cron. Here is an example cron 
command which sends an alert every 2 hours

```
0 */2 * * * bell WEBHOOK_URL
```

In order for this to work cron needs to have access to both bell, python packages and AWS
credentials. For this reason we recommend you install a cron job under your user account
and not root, otherwise you might need to install the tool with sudo and ensure root has
access to AWS credentials.

Even in that case as it turns out cron has a different more minimal PATH
than what you see in the terminal if you run `echo $PATH`. For that reason, you should
probably define the same PATH in your cron job as the one you see when you test the 
tool.

# CLI

```
Usage: bell [OPTIONS] WEBHOOK_URL

Arguments:
  WEBHOOK_URL  [required]

Options:
  --help                          Show this message and exit.
```
