import os
import shutil
from pathlib import Path

source_controlled_sources_path = "e:/Devel/GitHub/"
shared_path = source_controlled_sources_path + "erogeGamesResources/"
destination_path_for_modules = "E:/Devel/GitHub/ErogeFrameworkTester_Simpler/PowerPlayFramework/"

modules_with_path = {
    "ACTIONS": {
        "path": "PowerPlayFramework/ACTIONS/Implementations/Python/",
    },
    "BODY": {
        "path": "PowerPlayFramework/BODY/Implementations/Python/",
    },
    "CHARACTERS_BASE": {
        "path": "PowerPlayFramework/CHARACTERS_BASE/Implementations/Python/",
    },
    "GAME_SCENES": {
        "path": "PowerPlayFramework/GAME_SCENES/Implementations/Python/",
    },
    "LOCATIONS": {
        "path": "PowerPlayFramework/LOCATIONS/Implementations/Python/",
    },
    "MIND": {
        "path": "PowerPlayFramework/MIND/Implementations/Python/",
    },
    "NAMES": {
        "path": "PowerPlayFramework/NAMES/Implementations/Python/",
    },
}

modules_with_path_keys = modules_with_path.keys()

def clean_destination_folder():
    _func_name = "clean_destination_folder()"
    print("-> STARTED: {0}\n".format(_func_name))
    if os.path.exists(destination_path_for_modules):
        shutil.rmtree(destination_path_for_modules)
    os.mkdir(destination_path_for_modules)
    Path(destination_path_for_modules + "_PROGRAMMATICALLY_CREATED_FOLDER_DO_NOT_EDIT_CONTENTS.md").touch()
    Path(destination_path_for_modules + "__init__.py").touch()
    print("<- DONE: {0}\n".format(_func_name))

def select_all_but_py_files(path, names):
    result = []
    for file_name in names:
        print("----- " + path + file_name)
        if os.path.isfile(path + file_name):
            if not file_name.endswith(".py"):
                result.append(file_name)
    return result

def copy_modules_to_local_directory_tree():
    _func_name = "copy_modules_to_local_directory_tree()"
    print("-> STARTED: {0}\n".format(_func_name))
    for module in modules_with_path_keys:
        print("+ Processing '{0}'".format(module))
        if "path" not in modules_with_path[module].keys():
            raise ValueError("Module '{0}' does not exist.".format(module))
        full_path = shared_path + modules_with_path[module]["path"]
        print("+ Path is '{0}'".format(full_path))
        if not os.path.exists(full_path):
            raise ValueError("Path '{0}' does not exist for module '{1}'.".format(full_path, module))
        shutil.copytree(full_path, destination_path_for_modules + module, ignore=select_all_but_py_files)
        Path(destination_path_for_modules + module + "/_PROGRAMMATICALLY_CREATED_FOLDER_DO_NOT_EDIT_CONTENTS.md").touch()
        Path(destination_path_for_modules + module + "/__init__.py").touch()
        print("< Processed")
    print("<- DONE: {0}\n".format(_func_name))

print("---> STARTED")
clean_destination_folder()
copy_modules_to_local_directory_tree()