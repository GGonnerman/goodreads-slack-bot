# Goodreads Notifications for Slack

This program will check goodreads for any new books read by selected users. It will then send a message on slack to tell everyone that a user has completed a book.

## Setup

1. Create a new App on Slack to allow sending messages
    1. Go to [Your App](https://api.slack.com/apps) and click "Create New App" and "From scratch". Enter your app name and a workspace
    2. Go to "Incoming Webhooks" on the left side.
    3. Click the toggle to "Activate Incoming Webhooks"
    4. Click "Add New Webhook to Workspace", then select the channel and "Allow
    5. Copy the "Webhook URL"
2. Copy the file "example.env" to ".env" and replace the placeholder url with the one retrieved in Step 1.
3. Copy example-users.txt to users.txt and replace example url with any profile you wish to watch
4. Use any method you wish to automatically run this script every so often.
    1. E.g. add a cronjob that runs the script every 15 minutes
