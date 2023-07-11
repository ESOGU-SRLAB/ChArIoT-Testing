""" Edit_actions
    Edit_actions is the python code that extracts the actions that occur during the conversion of the buggy code to the fixed code.
    create_diff_files function uses python parser to convert source codes to AST. Actions of source codes translated to Ast are obtained with xml_diff.
"""
import os
from xmldiff import main
import python_parser
import shutil


def write_to_file(file, diff_list):
    """
    write_to_file writes the actions to the file.

    Args:
        file: file to write
        diff_list: list of actions
    """
    file.write("-------------------------------\n") 
    for i in range(diff_list.__len__()): # diff_list is a list of actions
        file.write(str(diff_list[i]) + "\n") # write actions to file
    file.write("-------------------------------")


def check_dir_action(action_type, src, dst, state, stage):
    """
    check_dir_action checks the directory and creates the directory if it does not exist.

    Args:
        action_type: type of action
        src: source directory
        dst: destination directory
        state: state of action
        stage: stage of action
    """
    cwd = os.getcwd() # get current working directory
    print(cwd) # print current working directory
    if action_type == "update": # if action type is update
        if not os.path.exists(cwd + "/update"): # if update directory does not exist
            os.makedirs(cwd + "/update") # create update directory
        if not os.path.exists(cwd + "/update/editActions"): # if editActions directory does not exist
            os.makedirs(cwd + "/update/editActions") # create editActions directory
        if not os.path.exists(cwd + "/update/bugfixed"): # if bugfixed directory does not exist
            os.makedirs(cwd + "/update/bugfixed") # create bugfixed directory
        if stage == 3: # if stage is 3
            if state != 2: # if state is not 2
                shutil.copytree(
                    src,
                    dst,
                    symlinks=False,
                    ignore=None,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True,
                ) # copy tree
        else: # if stage is not 3
            shutil.copytree(
                src,
                dst,
                symlinks=False,
                ignore=None,
                ignore_dangling_symlinks=False,
                dirs_exist_ok=True,
            ) # copy tree
    elif action_type == "delete": # if action type is delete
        if not os.path.exists(cwd + "/delete"): # if delete directory does not exist
            os.makedirs(cwd + "/delete") # create delete directory
        if not os.path.exists(cwd + "/delete/editActions"): # if editActions directory does not exist
            os.makedirs(cwd + "/delete/editActions") # create editActions directory
        if not os.path.exists(cwd + "/delete/bugfixed"): # if bugfixed directory does not exist
            os.makedirs(cwd + "/delete/bugfixed") # create bugfixed directory
        if stage == 3: # if stage is 3
            if state != 2: # if state is not 2
                shutil.copytree(
                    src,
                    dst,
                    symlinks=False,
                    ignore=None,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True,
                ) # copy tree
        else: # if stage is not 3
            shutil.copytree(
                src,
                dst,
                symlinks=False,
                ignore=None,
                ignore_dangling_symlinks=False,
                dirs_exist_ok=True,
            ) # copy tree
    elif action_type == "insert": # if action type is insert
        if not os.path.exists(cwd + "/insert"): # if insert directory does not exist
            os.makedirs(cwd + "/insert") # create insert directory
        if not os.path.exists(cwd + "/insert/editActions"): # if editActions directory does not exist
            os.makedirs(cwd + "/insert/editActions") # create editActions directory
        if not os.path.exists(cwd + "/insert/bugfixed"): # if bugfixed directory does not exist
            os.makedirs(cwd + "/insert/bugfixed") # create bugfixed directory
        if stage == 3: # if stage is 3
            if state != 2: # if state is not 2
                shutil.copytree(
                    src,
                    dst,
                    symlinks=False,
                    ignore=None,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True,
                ) # copy tree
        else: # if stage is not 3
            shutil.copytree(
                src,
                dst,
                symlinks=False,
                ignore=None,
                ignore_dangling_symlinks=False,
                dirs_exist_ok=True,
            ) # copy tree


def create_diff_files(action_type, state, stage):
    """
    create_diff_files creates the diff files.

    Args:
        action_type: type of action
        state: state of action
        stage: stage of action

    Raises:
        BaseException: An error occurred when the file could not be opened.
    """
    actions = {} # actions is a dictionary
    action_list = [] # action_list is a list
    cwd = os.getcwd() # get current working directory
    print(cwd) # print current working directory
    src = cwd + "/bugfixed" # source directory
    dst = cwd + "/" + action_type + "/bugfixed" # destination directory
    check_dir_action(action_type, src, dst, state, stage) # check directory action
    if not os.path.exists(cwd + "/" + action_type + "/index_of_Edit_Actions.txt"): # if index_of_Edit_Actions.txt does not exist
        with open(
            cwd + "/" + action_type + "/index_of_Edit_Actions.txt",
            mode="w+",
            encoding="utf-8",
        ) as index_file: # open index_of_Edit_Actions.txt
            index_file.write("0\n0") # write 0 0
    with open(
        cwd + "/" + action_type + "/index_of_Edit_Actions.txt",
        mode="r",
        encoding="utf-8",
    ) as index_file: # open index_of_Edit_Actions.txt
        tp_index = int(index_file.readline()) # read line
        edit_action_index = int(index_file.readline()) # read line

    index = tp_index # index is tp_index
    counter = edit_action_index # counter is edit_action_index
    fixed_folder_path = cwd + "/" + action_type + "/bugfixed/fixed_files"   # fixed_folder_path is cwd + "/" + action_type + "/bugfixed/fixed_files"
    buggy_folder_path = cwd + "/" + action_type + "/bugfixed/buggy_files"  # buggy_folder_path is cwd + "/" + action_type + "/bugfixed/buggy_files"
    print(os.path) # print os path
    while os.path.exists(
        fixed_folder_path + "/fixed" + index.__str__() + ".txt"
    ) and os.path.exists(buggy_folder_path + "/buggy" + index.__str__() + ".txt"): # while fixed_folder_path + "/fixed" + index.__str__() + ".txt" and buggy_folder_path + "/buggy" + index.__str__() + ".txt" exist
        try:
            # python_parser converts source codes to AST
            fixed_ast = python_parser.main(
                fixed_folder_path + "/fixed" + index.__str__() + ".txt"
            ) # fixed_ast is python_parser.main(fixed_folder_path + "/fixed" + index.__str__() + ".txt")
            buggy_ast = python_parser.main(
                buggy_folder_path + "/buggy" + index.__str__() + ".txt"
            ) # buggy_ast is python_parser.main(buggy_folder_path + "/buggy" + index.__str__() + ".txt")
        except SystemExit: # if SystemExit
            # Source code pairs whose actions cannot be extracted are deleted.
            os.remove(buggy_folder_path + "/buggy" + index.__str__() + ".txt") # remove buggy_folder_path + "/buggy" + index.__str__() + ".txt"
            os.remove(fixed_folder_path + "/fixed" + index.__str__() + ".txt") # remove fixed_folder_path + "/fixed" + index.__str__() + ".txt"
            index += 1 # index + 1
            with open(
                cwd + "/" + action_type + "/index_of_Edit_Actions.txt",
                mode="w+",
                encoding="utf-8",
            ) as index_file: # open index_of_Edit_Actions.txt
                index_file.write(index.__str__() + "\n" + counter.__str__()) # write index.__str__() + "\n" + counter.__str__()
            if (index % 250000) == 0: # if index % 250000 == 0
                exit() # exit
            continue # continue

        valid = 1 # valid is 1
        try: # try
            actions = {} # actions is a dictionary
            # Actions between ASTs are obtained with xml_diff. The parameters used were determined by trying to be the most efficient.
            diff = main.diff_texts(
                fixed_ast,
                buggy_ast,
                diff_options={"F": 0.5, "ratio_mode": "faster", "fast_match": True},
            )
            print(len(diff)) # print len(diff)
            if len(diff) == 0: # if len(diff) == 0
                raise BaseException
            if action_type == "delete":
                valid = validation_of_delete_action(actions, diff, valid)
            elif action_type == "update":
                valid = validation_of_update_action(diff, valid)
            elif action_type == "insert":
                valid = validation_of_insert_action(actions, diff, valid)
        except BaseException:
            print("Diff index error!")
        if valid == 1:
            with open(
                cwd + "/" + action_type + "/editActions/" + counter.__str__() + ".txt",
                "w+",
                encoding="utf-8",
            ) as f_edit_actions:
                buggy_old_name = buggy_folder_path + "/buggy" + index.__str__() + ".txt"
                buggy_new_name = (
                    buggy_folder_path + "/buggy" + counter.__str__() + ".txt"
                )
                fixed_old_name = fixed_folder_path + "/fixed" + index.__str__() + ".txt"
                fixed_new_name = (
                    fixed_folder_path + "/fixed" + counter.__str__() + ".txt"
                )
                counter += 1
                os.rename(buggy_old_name, buggy_new_name)
                os.rename(fixed_old_name, fixed_new_name)
                write_to_file(f_edit_actions, diff)
        else:
            os.remove(buggy_folder_path + "/buggy" + index.__str__() + ".txt")
            os.remove(fixed_folder_path + "/fixed" + index.__str__() + ".txt")

        index += 1
        with open(
            cwd + "/" + action_type + "/index_of_Edit_Actions.txt",
            mode="w+",
            encoding="utf-8",
        ) as index_file:
            index_file.write(index.__str__() + "\n" + counter.__str__())
        if (index % 250000) == 0 and index != 0:
            exit()


def validation_of_delete_action(actions, diff, valid):
    """
    validation_of_detele_action checks whether the actions taken are suitable for delete action.
    :param actions: list of actions
    :param diff: list of diffs
    :param valid: validation variable
    """
    valid_update = 0
    for i in diff:
        difftxt = str.split(i.__str__(), "(")
        action = difftxt[0]
        if action in actions:
            actions[action] += 1
        else:
            actions[action] = 1
        if action == "MoveNode":
            valid_update = 1
        elif action == "UpdateAttrib":
            if valid_update == 0:
                valid = 0
                return valid
            elif valid_update == 1:
                valid_update = 0
    max_action = max(actions, key=actions.get)
    if max_action == "DeleteNode":
        valid = 1
    else:
        valid = 0
    return valid


def validation_of_update_action(diff, valid):
    """
    validation_of_update_action checks whether the actions taken are suitable for update action.
    :param diff: list of diffs
    :param valid: validation variable
    """
    for i in diff:
        difftxt = str.split(i.__str__(), "(")
        action = difftxt[0]

        if action == "UpdateAttrib":
            valid = 1
        else:
            valid = 0
            return valid
    return valid


def validation_of_insert_action(actions, diff, valid):
    """
    validation_of_detele_action checks whether the actions taken are suitable for delete action.
    :param actions: list of actions
    :param diff: list of diffs
    :param valid: validation variable
    """
    valid_update = 0
    for i in diff:
        difftxt = str.split(i.__str__(), "(")
        action = difftxt[0]
        if action in actions:
            actions[action] += 1
        else:
            actions[action] = 1
        if action == "MoveNode":
            valid_update = 1
        elif action == "UpdateAttrib":
            if valid_update == 0:
                valid = 0
                return valid
            elif valid_update == 1:
                valid_update = 0

    max_action = max(actions, key=actions.get)
    if max_action == "InsertNode":
        valid = 1
    else:
        valid = 0
    return valid
