# Hi Handsome
- clone to home
- source the different dot files
- follow instructions for other configs

## requirements
- python
- zsh
- fzf
- rust
- xdotools
- xbindkeys
- exa
- wmctrl
- copyq

## Other commands to run
- `git config --global core.editor vi`
- `sudo apt insall cmake vim gnome-tweaks gnome-shell-extensions fzf tmux xsel tig fonts-powerline gh`
- `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh` for rust
- `git clone https://github.com/Moran296/WinFoc.git`
- `cargo install exa`
- `cargo install onefetch`
- `cargo install binsider`

## DOTS

### zsh
- in ~/.zshrc you need `source ~/nekudot/.zshrc`
- should be installed:
	- oh my zsh
	- git
	- github, github copilot (follow docs)
	- exa (installed with cargo)
	- tmux

### tmux
- tpm needs to be installed with `git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm`
- in ~/.tmux.conf add line `source-file ~/nekudot/.tmux.conf`
- ctrl + hjkl are for panes
- alt + right/left are for windows

### xbindkeys
XbindKeys does not have a source command like other dotfiles so you need to create a a file manually and add the required commands
- `xbindkeys --defaults > ~/.xbindkeysrc && vim ~/.xbindkeysrc`
- add the following at the end of the file

```
"transset -p --inc 0.05"
  alt + b:4

"transset -p --dec 0.05"
  alt + b:5

"transset -a --inc 0.05"
  alt + equal

"transset -a --dec 0.05"
  alt + minus
```

## SCRIPTS:

### WinFoc
- clone WinFoc, build and follow instructions for SUPER +H\L


## COPYQ
- install copyq
- add the next custom shortcut in gnome settings -> keyboard shortcuts
	- copyq
	- copyq -e "toggle()"
	- Super + V



## Other Gnome keyboard Settings
- Move to workspace above 			- Ctrl+Super+K
- Move to workspace below 			- Ctrl+Super+J
- Move window one monitor to the left 		- Super+Shift+H
- Move window one monitor to the right 		- Super+Shift+L
- Move window one workspace down 		- Super+Ctrl+Shift+J
- Move window one workspace up 			- Super+Ctrl+Shift+K
- Copy a screenshot of an area to clipboard 	- Super+Shift+S
- Copy a screenshot clipboard 			- Super+S
- Lock Screen					- Ctrl+Alt+L
- Show the notification list			- Disabled
- Show the overview				- Disabled
- Hide window					- Super+Space
- Maximize window				- Super+K
- Restore window				- Super+J
- View split on left				- Alt+Suer+H
- View split on right				- Alt+Suer+L
- zsh (custom command `gnome-terminal -- zsh`)  - Ctrl+Alt+Z


## XKB
The following lines must be added to `/usr/share/X11/xkb/symbols/us`

```
in the xkb_symbols "basic" {
	name[Group1]= "English (US)";
```

after all other keys

```
    key <AC06> {        [         h, H, Left            ]       };
    key <AC07> {        [         j, J, Down            ]       };
    key <AC08> {        [         k, K, Up              ]       };
    key <AC09> {        [         l, L, Right           ]       };
    key <AC03> {        [         d, D, Delete          ]       };

    key <SPCE> { [        space,        space,           BackSpace,     nobreakspace ] };

    key <CAPS> { [ ISO_Level3_Shift ] };
```

## VSCODE

Seems that currently vscode does not allow improting from different json files so..
Just copy the contents of vscode/settings.json and vscode/keybindings.json to .config/Code/User/...

## Powerlevel10k
- install powerline and nerd fonts
- `sudo apt-get install fonts-powerline`
- clone repo `git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k`
- source zsh with the theme `ZSH_THEME="powerlevel10k/powerlevel10k"`

## WEZTERM
- install wezterm
    - several ways, one is to add a gpg key and repo for it and use apt install or download a binary
- add `.wezterm.lua` file in the user folder and inside  just add this:
- `dofile('/home/<user>/nekudot/.wezterm.lua')`
- this should be enough. wallpapers can be added in wallpaper folder
