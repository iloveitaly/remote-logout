chmod +x logout.py
mv logout.py logout.command
osascript -e 'tell application "System Events" to make login item at end with properties {path:"$PWD/logout.command", hidden:true}'