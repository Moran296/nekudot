export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
plugins=(git tmux zsh-github-copilot)

source $ZSH/oh-my-zsh.sh

source /usr/share/doc/fzf/examples/completion.zsh
source /usr/share/doc/fzf/examples/key-bindings.zsh

alias ls='exa' # just replace ls by exa and allow all other exa arguments
alias l='exa -lbF' #   list, size, type
alias ll='exa -la' # long, all
alias open='xdg-open'
xbindkeys

function gitpull() { echo "git pull"; git pull; zle reset-prompt; zle redisplay}
zle -N gitpull
bindkey '^gp' gitpull

function gitcheckout() { echo "git checkout ."; git checkout .; zle reset-prompt; zle redisplay}
zle -N gitcheckout
bindkey '^g.' gitcheckout

function gitdiff() { echo "git diff"; git diff; zle reset-prompt; zle redisplay}
zle -N gitdiff
bindkey '^gd' gitdiff

function gitstatus() { echo "git status"; git status; zle reset-prompt; zle redisplay}
zle -N gitstatus
bindkey '^gs' gitstatus

function gitshow() { echo "git show"; git show; zle reset-prompt; zle redisplay}
zle -N gitshow
bindkey '^gh' gitshow

function gitlog() { echo "git log --oneline"; git log --oneline; zle reset-prompt; zle redisplay}
zle -N gitlog
bindkey '^gl' gitlog

# copilot
bindkey '^[|' zsh_gh_copilot_explain  # bind Alt+shift+\ to explain
bindkey '^[\' zsh_gh_copilot_suggest  # bind Alt+\ to suggest
eval "$(gh copilot alias -- zsh)"

