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
- ctrl + right/left (ctrl+caps+hl) are for windows

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

### py_focus.py
Use shortcut to move between windows that are not minimized across the same desktop
- add following shirtcuts in settings -> keyboard shortcuts
	- focus right
	- nohup python3 /home/user/nekudot/py_focus.py right > /dev/null 2>&1 &
	- SUPER + L

	- focus left
	- nohup python3 /home/user/nekudot/py_focus.py left > /dev/null 2>&1 &
	- SUPER + H


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

