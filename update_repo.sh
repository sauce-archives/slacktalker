set -x
if ! [ -n "$SSH_AUTH_SOCK" ]; then
    echo "SSH Agent Forwarding not detected.  Try reconnecting with -A"
    exit 1
fi
setfacl -m sauce:x   $(dirname "$SSH_AUTH_SOCK")
setfacl -m sauce:rwx "$SSH_AUTH_SOCK"
sudo -iu sauce bash -c 'cd ~/slacktalker && git pull'
setfacl -x sauce   $(dirname "$SSH_AUTH_SOCK")
setfacl -x sauce "$SSH_AUTH_SOCK"
