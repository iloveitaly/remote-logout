# Logout of a macOS User Remotely

Mac OS allows you to set up another user on your computer which can be logged in remotely. Combine this with the amazing
powers of Tailscale and it enables you to securely access your computer remotely regardless of where you are.

However, this functionality in MacOS is a little buggy. The user can get into a strange state where it's impossible to
log in and you get stuck on the login screen without a password input.

This little tool enables you to create a server with a single entry point which logs out of the user that this tool is executed under.

## Installation

1. Make the script executable
2. Use `.command` for the execution, which opens up a terminal window and runs the script.
3. Add it to your login items

[install.sh](./install.sh) does this for you:

```shell
git clone https://github.com/iloveitaly/remote-logout
cd remote-logout
./install.sh
```

## When Screensharing Breaks Your Window Manager

Just getting beeping when attempting to use a window manager like Raycast or Rectangle?

TODO detail attempts to fix this

## Inspiration

* https://superuser.com/questions/229773/run-command-on-startup-login-mac-os-x
* https://apple.stackexchange.com/questions/126761/way-to-logout-a-user-from-the-command-line-in-os-x-10-9

## TODO

- [ ] the `.command` approach works fine for my needs, but launchctl file probably is a better approach