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

Note that cron's environment is different to your user or root environment. See troubleshooting
if you have problems setting up bell to work with cron.

# CLI

```
Usage: bell [OPTIONS] WEBHOOK_URL

Arguments:
  WEBHOOK_URL  [required]

Options:
  --help                          Show this message and exit.
```

# Troubleshooting

## Bell works when run manually but not through cron

In order for cron to work it needs to have access to both bell, python packages and AWS
credentials. For this reason we recommend you install a cron job under your user account
and not root, otherwise you might need to install the tool with sudo and ensure root has
access to AWS credentials.

Even in that case as it turns out cron has a different more minimal PATH
than what you see in the terminal if you run `echo $PATH`. For that reason, you should
probably define the same PATH in your cron job as the one you see when you test the
tool.

## Region not specified

We assume you have AWS credentials setup either through environment variables, aws configure
or proper IAM roles. We use boto under the hood to query AWS, see its documentation around
credentials [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)
