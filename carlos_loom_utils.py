import nuke
import os
import nukescripts
import glob

# Add more projects here 
PROJECT_COMP_NAMES = {"POS-30608-Love_Language":"LOV",
              "POS-30642-Bucking_Fastard":"BFA",
              "POS-30590-Sleeping_Trees":"SLT",
              "POS-30633-Lolavie - DC":"LOL",
              "POS-30633-Lolavie":"LOL"  }

# On MacOS change to /Volumes/vfx 
VFX_PATH = "v:"

def open_loom_comp():
    
    escaped_projects = ['"{}"'.format(p) for p in PROJECT_COMP_NAMES.keys()]

    # Create a dropdown panel
    p = nuke.Panel("Open New Project")
    p.addEnumerationPulldown("Project", " ".join(escaped_projects))
    p.addSingleLineInput("Sequence (sq)", "")
    p.addSingleLineInput("Shot", "")
    p.addSingleLineInput("Version", "")
    p.addSingleLineInput("Artist", "")

    # Show the panel and get values
    if not p.show():
        return 

    project = p.value("Project")
    sq = p.value("Sequence (sq)").zfill(4)
    shot = p.value("Shot").zfill(4)
    version = p.value("Version")
    artist = p.value("Artist")
    shot_name = f"{PROJECT_COMP_NAMES[project]}_Sq{sq}_Sh{shot}"

    file_path = get_latest_comp(project, sq, shot_name, version, artist)
    if file_path is not None:
        switch_open_project(file_path)
        return
    nuke.message(f"File not found:\n{file_path}")

def get_latest_comp(project, sq, shot_name, version="", artist=""):
    search_dir= f"{VFX_PATH}/{project}/050_Production/020_Comps/Sq{sq}/{shot_name}/020_Projects/060_FinalComp"

    if version == "":
        version = "???"
    else:
        version = str(version).zfill(3)

    if artist == "":
        artist = "??"
    else:
        artist = artist.upper()

    file_pattern = f"{shot_name}_v{version}_{artist}.nk"
    pattern = os.path.join(search_dir, file_pattern)
    print("Pattern:  " + pattern)
    matching_files = glob.glob(pattern)
    matching_files.sort(reverse=True)
    if(not matching_files):
        return None
    return matching_files[0]

def switch_open_project(file_path):
    if nuke.root().modified():
        if nuke.ask("Save current script before closing?"):
            nukescripts.scriptSave()

    nuke.scriptClose()
    nuke.scriptOpen(file_path)

def create_read_from_write():
    # Get selected nodes
    selected_nodes = nuke.selectedNodes()
    
    if not selected_nodes:
        nuke.message("Please select a Write node.")
        return

    write_node = None
    for node in selected_nodes:
        if node.Class() == 'Write':
            write_node = node
            break
    
    if not write_node:
        nuke.message("No Write node selected.")
        return

    file_path = write_node['file'].value().replace('/Volumes/VFX/', 'v:/')
    colorspace = write_node['colorspace'].value()

    if not file_path:
        nuke.message("Selected Write node has no file path.")
        return

    # Create Read node
    read_node = nuke.createNode('Read')
    read_node['file'].setValue(file_path)
    read_node['colorspace'].setValue(colorspace)
    read_node['first'].setValue(nuke.root().firstFrame())
    read_node['last'].setValue(nuke.root().lastFrame())

    read_node.setXpos(write_node.xpos())
    read_node.setYpos(write_node.ypos() + 100)

