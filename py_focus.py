import subprocess
import sys
import re

def normalize_window_id(win_id):
    return hex(int(win_id, 16))

def get_windows_stacked():
    output = subprocess.check_output("xprop -root | grep '_NET_CLIENT_LIST_STACKING(WINDOW)'", shell=True).decode("utf-8")
    return [normalize_window_id(word.strip(',')) for word in output.split() if word.startswith("0x")]

def get_stats(id):
    # Regular expressions to match the geometry components
    output = subprocess.check_output(["xwininfo", "-wm", "-stats", "-id", id]).decode("utf-8")
    x_match = re.search(r'Absolute upper-left X:\s+(\d+)', output)
    y_match = re.search(r'Absolute upper-left Y:\s+(\d+)', output)
    width_match = re.search(r'Width:\s+(\d+)', output)
    height_match = re.search(r'Height:\s+(\d+)', output)
    desktop_match = re.search(r'Displayed on desktop (\d+)', output)


    if x_match and y_match and width_match and height_match and desktop_match:
        # Extract values and convert them to integers
        x = int(x_match.group(1))
        y = int(y_match.group(1))
        width = int(width_match.group(1))
        height = int(height_match.group(1))
        desktop = int(desktop_match.group(1))
        
        return {
            "id": id,
            "desktop": desktop,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
    else:
        raise ValueError("Could not parse geometry from the output")

# Get the list of windows with wmctrl
def get_windows():
    return [get_stats(id) for id in get_windows_stacked()]

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
        if is_window_viewable(win["id"]) and not is_window_minimized(win["id"]):
            visible_windows.append(win)
    return visible_windows

def calculate_overlap_area(win1, win2):
    x1, y1, w1, h1 = win1["x"], win1["y"], win1["width"], win1["height"]
    x2, y2, w2, h2 = win2["x"], win2["y"], win2["width"], win2["height"]

    # Determine the coordinates of the overlapping rectangle
    overlap_x1 = max(x1, x2)
    overlap_y1 = max(y1, y2)
    overlap_x2 = min(x1 + w1, x2 + w2)
    overlap_y2 = min(y1 + h1, y2 + h2)

    # Calculate the width and height of the overlapping rectangle
    overlap_width = max(0, overlap_x2 - overlap_x1)
    overlap_height = max(0, overlap_y2 - overlap_y1)

    # If there is no overlap, the area will be zero
    return overlap_width * overlap_height

def find_obscured_windows(windows):
    """
    Find windows that are obscured by more than 15% by any window higher in the stacking order.
    """
    obscured_windows = []

    # Iterate over windows from bottom to top
    for i, win in enumerate(windows):
        total_area = win["width"] * win["height"]  # Total area of the current window
        obscured_area = 0  # Track total obscured area

        for higher_win in windows[i+1:]:  # Compare with all windows higher in the stack
            overlap_area = calculate_overlap_area(win, higher_win)

            # Add the overlap area to the total obscured area
            obscured_area += overlap_area

            # Check if obscured area exceeds 15% of the window's total area
            if obscured_area > 0.15 * total_area:
                obscured_windows.append(win["id"])
                break  # No need to check further if we've found enough overlap

    return obscured_windows

# Find the next window in the given direction
def find_next_window(direction, windows, current_win):
    obscured = find_obscured_windows(windows)

    current_x, current_y = current_win["x"], current_win["y"]
    if direction == 'left':
        candidates = [win for win in windows if win["x"] < current_x and win["id"] not in obscured]
        if candidates:
            return max(candidates, key=lambda win: win["x"])  # Focus on the rightmost of the left candidates
    elif direction == 'right':
        candidates = [win for win in windows if win["x"] > current_x and win["id"] not in obscured]
        if candidates:
            return min(candidates, key=lambda win: win["x"])  # Focus on the leftmost of the right candidates
    elif direction == 'up':
        candidates = [win for win in windows if win["y"] < current_y and win["id"] not in obscured]
        if candidates:
            return max(candidates, key=lambda win: win["y"])  # Focus on the bottom-most of the above candidates
    elif direction == 'down':
        candidates = [win for win in windows if win["y"] > current_y and win["id"] not in obscured]
        if candidates:
            return min(candidates, key=lambda win: win["y"])  # Focus on the topmost of the below candidates
    return None

# Main function to handle switching focus
def switch_focus(direction):
    windows = get_windows()

    active_win_id = get_active_window()
    active_window = [win for win in windows if win["id"] == active_win_id]
    if not active_window:
        print("No active window found!")
        return
    active_window = active_window[0]

    # filter out windows not on current desktop (workspace) 
    windows_on_current_desktop = [win for win in windows if win["desktop"] == active_window["desktop"]]

    # Further filter out minimized or background windows
    visible_windows = filter_visible_windows(windows_on_current_desktop)

    # Find the current window
    active_window = [win for win in windows_on_current_desktop if win["id"] == active_win_id]

    for w in visible_windows:
        print(w["id"])

    # Get the best match for next window 
    next_window = find_next_window(direction, visible_windows, active_window[0])

    if next_window:
        focus_window(next_window["id"])
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
