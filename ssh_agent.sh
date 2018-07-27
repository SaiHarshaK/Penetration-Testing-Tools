#Checks for SSH agent. Uses it if on. Starts another if not.

export SSH_AUTH_SOCK=/home/USER/.ssh-socket

ssh-add -l >/dev/null 2>&1
if [ $? = 2 ]; then
   rm -rf $SSH_AUTH_SOCK
   ssh-agent -a $SSH_AUTH_SOCK >/tmp/.ssh-script
   source /tmp/.ssh-script
   echo $SSH_AGENT_PID > ~/.ssh-agent-pid
   rm /tmp/.ssh-script
fi