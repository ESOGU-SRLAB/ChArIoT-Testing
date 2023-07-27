""" ex_abs_main.py provides to execute all stages of tool step by step with user input."""

import pathlib
import os
import shutil
import tokenize
from commit_to_diff import commit_to_diff
from diff_to_tp import seperate_diffs
from edit_actions import create_diff_files
from abstraction import ASTNodeVisitor
from lexico_grapher import create_vocab
from refactor import refactor_duplicate
from refactor import refactor_abstracted_files


def execute_abstraction():
    abstraction(
        cwd + "/commit_tp/" + action_type + "/bugfixed/fixed_files",
        cwd + "/commit_tp/" + action_type + "/bugfixed/buggy_files",
    )
    #fixed_list = create_vocab("fixed", abstract_fixedpath, action_type)
    #buggy_list = create_vocab("buggy", abstract_buggypath, action_type)
    #refactor_abstracted_files(fixed_list, buggy_list, action_type)
    #refactor_duplicate(action_type)
    #create_vocab("fixed", abstract_fixedpath, action_type)
    #create_vocab("buggy", abstract_buggypath, action_type)


def arranging_files(action_type, input_stage, state_type):
    stage_list = ["commit_to_diff", "diff_to_tp", "edit_actions", "abstraction"]
    cwd = os.getcwd()

    # try:
    if input_stage == stage_list[0]:  # Commit to Diff
        if state_type == 1:
            if os.path.exists(cwd + "/commit_tp"):
                shutil.rmtree(cwd + "/commit_tp", ignore_errors=True, onerror=None)

        commit_to_diff(COMMITS_FILE_NAME, DIFFS_FOLDER_NAME)
        seperate_diffs(DIFFS_FOLDER_NAME)
        create_diff_files(action_type, state, stage)
        execute_abstraction()

    if input_stage == stage_list[1]:  # Diff to TP
        if state_type == 1:
            if os.path.exists(cwd + "/commit_tp/" + action_type):
                shutil.rmtree(
                    cwd + "/commit_tp/" + action_type, ignore_errors=True, onerror=None
                )
            if os.path.exists(cwd + "/commit_tp/bugfixed"):
                shutil.rmtree(
                    cwd + "/commit_tp/bugfixed", ignore_errors=True, onerror=None
                )
            if os.path.exists(cwd + "/commit_tp/index_of_TP.txt"):
                os.remove(cwd + "/commit_tp/index_of_TP.txt")
        seperate_diffs(DIFFS_FOLDER_NAME)
        create_diff_files(action_type, state, stage)
        execute_abstraction()

    if input_stage == stage_list[2]:  # Edit Actions
        if state_type == 1:
            if os.path.exists(cwd + "/commit_tp/" + action_type):
                shutil.rmtree(
                    cwd + "/commit_tp/" + action_type, ignore_errors=True, onerror=None
                )
            if os.path.exists(
                cwd + "/commit_tp/" + action_type + "/index_of_Edit_Actions.txt"
            ):
                os.remove(
                    cwd + "/commit_tp/" + action_type + "/index_of_Edit_Actions.txt"
                )
        os.chdir(cwd + "/commit_tp/")
        create_diff_files(action_type, state, stage)
        execute_abstraction()

    if input_stage == stage_list[3]:  # Abstraction
        if os.path.exists(cwd + "/commit_tp/" + action_type + "/abstarctedbuggyfiles"):
            shutil.rmtree(
                cwd + "/commit_tp/" + action_type + "/abstarctedbuggyfiles",
                ignore_errors=True,
                onerror=None,
            )
        if os.path.exists(cwd + "/commit_tp/" + action_type + "/abstarctedfixedfiles"):
            shutil.rmtree(
                cwd + "/commit_tp/" + action_type + "/abstarctedfixedfiles",
                ignore_errors=True,
                onerror=None,
            )
        dir_name = cwd + "/commit_tp/" + action_type + "/"
        test = os.listdir(dir_name)
        for item in test:
            if item.endswith(".txt"):
                os.remove(os.path.join(dir_name, item))
        execute_abstraction()

    # except:
    #     print("Error in arranging_files function!")


path = pathlib.Path(__file__).parent.resolve()
stage_list = ["commit_to_diff", "diff_to_tp", "edit_actions", "abstraction"]
action_list = ["update", "delete", "insert"]

stage = int(
    input(
        "[1]- Extraction\n[2]- Transform\n[3]- Classifier\n[4]- Abstraction\n"
        "Please choose the value corresponding to the beginning stage: "
    )
)

if 1 > stage > 4:
    print("Wrong input ERROR!")
    exit()
else:
    stage_type = stage_list[stage - 1]

action = int(
    input(
        "[1]- Update\n[2]- Delete\n[3]- Insert\n"
        "Please choose the value corresponding to the action type: "
    )
)

if 1 > action > 3:
    print("Wrong input ERROR!")
    exit()
else:
    action_type = action_list[action - 1]

state = int(
    input(
        "[1]- Restart (Deletes existing files.)\n[2]- Repair (Keeps running on existing files.)\n"
        "Please choose the value corresponding to the mode: "
    )
)

if 1 > state > 2:
    print("Wrong input ERROR!")
    exit()

# Parameters
COMMITS_FILE_NAME = "bq-results-20211015-151804-czobr355m7xe.txt"
DIFFS_FOLDER_NAME = "commit_tp/diffTexts"
cwd = os.getcwd()
abstract_fixedpath = (
    cwd + "/commit_tp/" + action_type + "/abstractedfixedfiles/abstfixed"
)
abstract_buggypath = (
    cwd + "/commit_tp/" + action_type + "/abstractedbuggyfiles/abstbuggy"
)

# Executing Tool
arranging_files(action_type, stage_type, state)
