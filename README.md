# dawg
### yo I heard you like notifications


Dawg Server is a process that allows you to trigger a push notification to be sent on a timed delay, as well as providing an endpoint to pre-emptively cancel that notification
It can be configured to send notifications via the Yo API (seriously) or [Pushover](https://pushover.net/).

Dawg Client uses [terminal-notifier](https://github.com/julienXX/terminal-notifier) in concert with Dawg Server to send a local notification, and then send a remote notification if it is not acknowledged quickly.

In combination, these two allow you to send yourself a notification locally (i.e. on your desktop), and then "escalate" the notification to your phone if you're AFK.

## Usage
1. Get pushover and terminal-notifier
2. Set `$DAWG_URL` to location of the server (slide into dms to just use mine) and `$DAWG_USER` to your device key with pushover
3. Call dawg-client when your tests/build/whatever finishes. Go to lunch if it's taking too long. It'll hit you up when it's ready.

## Implementation
The server is written in Python 3, uses [aiohttp](https://aiohttp.readthedocs.io/en/stable/) and python's type annotations. It might be overengineered just a bit.
