""" refactor
    refactor_duplicate function removes duplicate rows in the final dataset and enables dataset quality.
    refactor_abstracted_files defines the data that needs to be deleted by limiting the vocabulary and updates the dataset.
"""
import tokenize
import os


def refactor_duplicate(action_type):
    """
    Function to delete duplicate lines in buggy and fixed files.
    """
    without_duplicate_index_list = []
    index_list = []
    old_buggy_file = open(
        "commit_tp/" + action_type + "/buggy.txt", "r", encoding="utf-8"
    )
    new_buggy_file = open(
        "commit_tp/" + action_type + "/buggy_new.txt", "a+", encoding="utf-8"
    )
    old_fixed_file = open(
        "commit_tp/" + action_type + "/fixed.txt", "r", encoding="utf-8"
    )
    new_fixed_file = open(
        "commit_tp/" + action_type + "/fixed_new.txt", "a+", encoding="utf-8"
    )
    with open(
        "commit_tp/" + action_type + "/indexlist.txt", "r", encoding="utf-8"
    ) as index_file:
        index_list = index_file.read().splitlines()

    buggy_lines_seen = set()
    fixed_lines_seen = set()

    # fixed_line value searchs in old_fixed_file list to fix the line
    for fixed_line in old_fixed_file:
        if fixed_line not in fixed_lines_seen:
            buggy_line = old_buggy_file.readline()
            if buggy_line not in buggy_lines_seen:
                new_fixed_file.write(fixed_line)
                new_buggy_file.write(buggy_line)
                fixed_lines_seen.add(fixed_line)
                buggy_lines_seen.add(buggy_line)
                without_duplicate_index_list.append(index_list.pop(0))
                continue
        index_list.pop(0)

    with open(
        "commit_tp/" + action_type + "/indexlist.txt", "w+", encoding="utf-8"
    ) as index_file:
        index_file.truncate(0)
        for line in without_duplicate_index_list:
            index_file.write(line.__str__() + "\n")

    old_buggy_file.close()
    new_buggy_file.close()
    old_fixed_file.close()
    new_fixed_file.close()


def refactor_abstracted_files(fixed_list, buggy_list, action_type):
    """
    Function to delete duplicate lines in Abstract Buggy and Abstract Fixed files.
    :param fixed_list: Recall words from fixed.txt file.
    :param buggy_list: Recall words from buggy.txt file.
    """
    with open(
        "commit_tp/" + action_type + "/indexlist.txt", "r+", encoding="utf-8"
    ) as file:
        indexlist = file.read().splitlines()
    fixed = open("commit_tp/" + action_type + "/fixed.txt", "a+", encoding="utf-8")
    buggy = open("commit_tp/" + action_type + "/buggy.txt", "a+", encoding="utf-8")
    fixed_tokenlist = []
    buggy_tokenlist = []
    new_indexlist = []
    for i in indexlist:
        fixed_tokenlist.clear()
        buggy_tokenlist.clear()
        flag = 0
        with open(
            "commit_tp/" + action_type + "/abstractedfixedfiles/abstfixed" + i + ".txt",
            "r+",
            encoding="utf-8",
        ) as fixedfile, open(
            "commit_tp/" + action_type + "/abstractedbuggyfiles/abstbuggy" + i + ".txt",
            "r+",
            encoding="utf-8",
        ) as buggyfile:
            print(i)
            fixed_token = tokenize.generate_tokens(fixedfile.readline)
            # The source code of the data eliminated from the dictionary is determined and this data is deleted from the data set.
            for token in fixed_token:
                fixed_tokenlist.append(token[1])
            for string_fixed_list in fixed_list:
                if string_fixed_list in fixed_tokenlist:
                    fixedfile.truncate(0)
                    buggyfile.truncate(0)
                    # The content of the txt file that needs to be deleted is replaced with OUT OF BOUNDS.
                    fixedfile.write("OUT OF BOUNDS")
                    buggyfile.write("OUT OF BOUNDS")
                    flag = 1
                    break
            if flag == 0:
                # The source code of the data eliminated from the dictionary is determined and this data is deleted from the data set.
                buggy_token = tokenize.generate_tokens(buggyfile.readline)
                for token in buggy_token:
                    buggy_tokenlist.append(token[1])
                for string_buggy_list in buggy_list:
                    if string_buggy_list in buggy_tokenlist:
                        fixedfile.truncate(0)
                        buggyfile.truncate(0)
                        # The content of the txt file that needs to be deleted is replaced with OUT OF BOUNDS.
                        fixedfile.write("OUT OF BOUNDS")
                        buggyfile.write("OUT OF BOUNDS")
                        flag = 1
                        break
                if flag == 0:
                    fixedfile.seek(0)
                    buggyfile.seek(0)
                    list_fixedlines = fixedfile.read().split()
                    new_str = " ".join(list_fixedlines)
                    fixed.write(new_str + "\n")
                    list_buggylines = buggyfile.read().split()
                    new_str = " ".join(list_buggylines)
                    buggy.write(new_str + "\n")
                    new_indexlist.append(i)
    with open(
        "commit_tp/" + action_type + "/indexlist.txt", "a+", encoding="utf-8"
    ) as file:
        file.truncate(0)
        for index in new_indexlist:
            file.write(index.__str__() + "\n")

    fixed.close()
    buggy.close()
