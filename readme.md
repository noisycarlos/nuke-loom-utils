
## Installation ##
- Copy the 'carlos_loom_utils.py' file to you .nuke dir.
- Add the following to your menu.py (remove the keyboard shortcuts if you don't want them):


```
import carlos_loom_utils

utils_menu = toolbar.addMenu("Carlos Loom Utils")
utils_menu.addCommand("Open Loom Comp", "carlos_loom_utils.open_loom_comp()", "ctrl+shift+o")
utils_menu.addCommand("Create read from write node", "carlos_loom_utils.create_read_from_write()", "ctrl+shift+r")
```

## Usage ##
To open a comp select Open Loom Comp from the toolbar (or press the keyboard shortcut).

Specify the Project, Sequence (sq), and shot number. Artist and version number are optional. If you don't specify them it will open the latest version.
