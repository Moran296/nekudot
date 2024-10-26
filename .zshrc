export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(git tmux zsh-github-copilot)

# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# # Initialization code that may require console input (password prompts, [y/n]
# # confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
 fi


# for tmux to use utf8 (equivalent to running tmux -u)
export LC_ALL=en_IN.UTF-8
export LANG=en_IN.UTF-8

source $ZSH/oh-my-zsh.sh

source /usr/share/doc/fzf/examples/completion.zsh
source /usr/share/doc/fzf/examples/key-bindings.zsh

alias ls='exa' # just replace ls by exa and allow all other exa arguments
alias l='exa -lbF' #   list, size, type
alias ll='exa -la' # long, all
alias open='xdg-open'
xbindkeys

function gitpull() { echo "git pull"; git pull}
zle -N gitpull
bindkey '^gp' gitpull

function gitcheckout() { echo "git checkout ."; git checkout .}
zle -N gitcheckout
bindkey '^g.' gitcheckout

function gitstatus() { echo "git status"; git status}
zle -N gitstatus
bindkey '^gs' gitstatus

function gitdiff() { echo "git diff"; git diff; zle reset-prompt; zle redisplay}
zle -N gitdiff
bindkey '^gd' gitdiff

function gitshow() { echo "git show"; git show; zle reset-prompt}
zle -N gitshow
bindkey '^gh' gitshow

function gitlog() { echo "git log --oneline"; git log --oneline; zle reset-prompt}
zle -N gitlog
bindkey '^gl' gitlog

# copilot
bindkey '^[|' zsh_gh_copilot_explain  # bind Alt+shift+\ to explain
bindkey '^[\' zsh_gh_copilot_suggest  # bind Alt+\ to suggest
eval "$(gh copilot alias -- zsh)"

eval "$(zoxide init zsh)"

set editing-mode emacs

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

