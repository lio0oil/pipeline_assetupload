cd $(cd $(dirname $0);pwd)

pip3 install -r requirements.txt

cd ~
mkdir ~/zsh_plugins
cd zsh_plugins
git clone https://github.com/zsh-users/zaw.git
echo "source ${PWD}/zaw/zaw.zsh" >> ~/.zshrc
echo "bindkey '^R' zaw-history" >> ~/.zshrc