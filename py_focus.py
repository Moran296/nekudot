import subprocess
import sys

def normalize_window_id(win_id):
    return hex(int(win_id, 16))

# Get the list of windows with wmctrl
def get_windows():
    output = subprocess.check_output(["wmctrl", "-lG"]).decode("utf-8")
    windows = []
    for line in output.splitlines():
        fields = line.split()
        win_id = normalize_window_id(fields[0])
        x = int(fields[2])
        y = int(fields[3])
        w = int(fields[4])
        h = int(fields[5])
        desktop = int(fields[1])
        title = " ".join(fields[7:])
        windows.append((win_id, x, y, w, h, desktop, title))
    return windows

def get_stacking_order():
    output = subprocess.check_output(["xwininfo", "-tree", "-root"]).decode("utf-8")
    stacking_order = []
    for line in output.splitlines():
        if "Window id" in line:
            win_id = line.split()[3]
            stacking_order.append(win_id)
    return stacking_order

# Find the active window
def get_active_window():
    output = subprocess.check_output(["xprop", "-root", "_NET_ACTIVE_WINDOW"]).decode("utf-8")
    active_win_id = output.split()[-1].strip()
    return normalize_window_id(active_win_id)

# Get window state using xprop
def get_window_state(win_id):
    output = subprocess.check_output(["xprop", "-id", win_id, "_NET_WM_STATE"]).decode("utf-8")
    return output

# Check if a window is minimized
def is_window_minimized(win_id):
    state = get_window_state(win_id)
    return "_NET_WM_STATE_HIDDEN" in state

def is_window_viewable(win_id):
    output = subprocess.check_output(["xwininfo", "-id", win_id]).decode("utf-8")
    for line in output.splitlines():
        if "IsViewable" in line:
            return True

# Switch focus to the window by window ID
def focus_window(win_id):
    subprocess.call(["wmctrl", "-ia", win_id])

# Filter out minimized or background windows
def filter_visible_windows(windows):
    visible_windows = []
    for win in windows:
        if is_window_viewable(win[0]) and not is_window_minimized(win[0]):
            visible_windows.append(win)
    return visible_windows

# Find the next window in the given direction
def find_next_window(direction, windows, current_win):
    current_x, current_y = current_win[1], current_win[2]
    if direction == 'left':
        candidates = [win for win in windows if win[1] < current_x]
        if candidates:
            return max(candidates, key=lambda win: win[1])  # Focus on the rightmost of the left candidates
    elif direction == 'right':
        candidates = [win for win in windows if win[1] > current_x]
        if candidates:
            return min(candidates, key=lambda win: win[1])  # Focus on the leftmost of the right candidates
    elif direction == 'up':
        candidates = [win for win in windows if win[2] < current_y]
        if candidates:
            return max(candidates, key=lambda win: win[2])  # Focus on the bottom-most of the above candidates
    elif direction == 'down':
        candidates = [win for win in windows if win[2] > current_y]
        if candidates:
            return min(candidates, key=lambda win: win[2])  # Focus on the topmost of the below candidates
    return None

# Main function to handle switching focus
def switch_focus(direction):
    windows = get_windows()
    active_win_id = get_active_window()
    active_window = [win for win in windows if win[0] == active_win_id]
    
    if not active_window:
        print("No active window found!")
        return

    active_window = active_window[0]
    active_desktop = active_window[5]
    # filter out windows not on current desktop (workspace) 

    windows_on_current_desktop = [win for win in windows if win[5] == active_desktop]

    # Further filter out minimized or background windows
    visible_windows = filter_visible_windows(windows_on_current_desktop)

    # Find the current window
    active_window = [win for win in windows_on_current_desktop if win[0] == active_win_id]

    # Get the best match for next window 
    next_window = find_next_window(direction, visible_windows, active_window[0])

    if next_window:
        focus_window(next_window[0])
    else:
        print(f"No window found in {direction} direction.")

def check_wmctrl_installed():
    try:
        subprocess.check_output(["wmctrl", "--version"])
    except FileNotFoundError:
        print("wmctrl is not installed. Please install it using 'sudo apt-get install wmctrl'")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("There was an issue running wmctrl. Please ensure it is installed correctly.")
        sys.exit(1)

if __name__ == "__main__":
    check_wmctrl_installed()
    direction = "left"

    if len(sys.argv) >= 2:
        direction = sys.argv[1].lower()
        if direction not in ['left', 'right', 'up', 'down']:
            print("Direction must be one of: left, right, up, down")
            sys.exit(1)

    
    switch_focus(direction)

    
# in gnome seetings add the following custom shortcuts to use the script:
# SUPER + H
# nohup python3 /home/username/py_focus.py left > /dev/null 2>&1 &
# SUPER + L
# nohup python3 /home/username/py_focus.py right > /dev/null 2>&1 &
