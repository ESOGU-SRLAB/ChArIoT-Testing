""" Diff to tp
    The separate diff function opens the text files with the commit differences one by one.
    It then calls the sep_file function to get the buggy and fixed version of each file.
    While performing this operation, each buggy and fixed source code pair must be numbered the same.
    Global variables are needed in order for the numbering process to be regular.
"""

import os
import pathlib
import re
import natsort

# Global variables are defined for orderly enumeration of buggy and fixed source code pairs.
FIXED_COUNTER = 0
BUGGY_COUNTER = 0
IS_FUNCTION = False


def sep_file(filepath, bugfixed_path):
    """
    This function separates the bugfixed and buggy versions of the source code.

    Args:
        filepath: The path of the commit diff file.
        bugfixed_path: The path of the folder where the bugfixed and buggy versions of the source code will be saved.
    """
    try:  # If the bugfixed folder does not exist, it is created.
        with open(
            filepath, mode="r", encoding="utf-8"
        ) as file:  # The commit diff file is opened.
            skip_first_lines(
                file
            )  # The first 4 lines of the commit diff file are skipped.
            fixed_file = None  # The fixed_file variable is defined as None.
            buggy_file = None  # The buggy_file variable is defined as None.
            for line in file:  # The commit diff file is read line by line.
                global FIXED_COUNTER  # The FIXED_COUNTER variable is defined as global.
                global BUGGY_COUNTER  # The BUGGY_COUNTER variable is defined as global.
                global IS_FUNCTION  # The IS_FUNCTION variable is defined as global.
                # The '@@' sign is used to seperate methods from each other.
                if (
                    line[0] == "@" and line[1] == "@"
                ):  # If the line starts with '@@', the following operations are performed.
                    IS_FUNCTION = False  # The IS_FUNCTION variable is defined as False.
                    split_line = re.split(
                        "@@|\\)", line
                    )  # The line is split by the '@@' and ')' signs.
                    # Function-based filtering control is performed.
                    if (
                        line.find("def") != -1 and split_line[-1][0] == ":"
                    ):  # If the line contains 'def' and ends with ':', the following operations are performed.
                        IS_FUNCTION = (
                            True  # The IS_FUNCTION variable is defined as True.
                        )
                        # Creates different files to write each bugfix to different files.
                        """
                        with open(cwd
                            + "/bugfixed/fixed_files/fixed"
                            + FIXED_COUNTER.__str__()
                            + ".txt",
                            "w+",
                            encoding="utf-8",) as fixed_file, open(
                            cwd
                            + "/bugfixed/buggy_files/buggy"
                            + BUGGY_COUNTER.__str__()
                            + ".txt",
                            "w+",
                            encoding="utf-8",
                        ) as buggy_file:
                        """

                        fixed_file = open(
                            bugfixed_path
                            + "/fixed_files/fixed"
                            + FIXED_COUNTER.__str__()
                            + ".txt",
                            "w+",
                            encoding="utf-8",
                        )  # The fixed file is opened.
                        buggy_file = open(
                            bugfixed_path
                            + "/buggy_files/buggy"
                            + BUGGY_COUNTER.__str__()
                            + ".txt",
                            "w+",
                            encoding="utf-8",
                        )  # The buggy file is opened.
                        FIXED_COUNTER += (
                            1  # The FIXED_COUNTER variable is increased by 1.
                        )
                        BUGGY_COUNTER += (
                            1  # The BUGGY_COUNTER variable is increased by 1.
                        )
                        fixed_file.write(
                            split_line[2][1:] + "):\n"
                        )  # The fixed file is written.
                        buggy_file.write(
                            split_line[2][1:] + "):\n"
                        )  # The buggy file is written.
                    else:  # If the line does not contain 'def' and does not end with ':', the following operations are performed.
                        continue  # The loop is continued.
                if (
                    IS_FUNCTION
                ):  # If the IS_FUNCTION variable is True, the following operations are performed.
                    # If 3 '-' or 3 '+' appears, it will not be accepted.
                    if (
                        line[0] != "+" and line[0] != " " and line[0] != "-"
                    ):  # If the line does not start with '+' or ' ' or '-', the following operations are performed.
                        continue  # The loop is continued.
                    elif (
                        line[0]
                        == "+"  # If the line starts with '+', the following operations are performed.
                    ):  # Writes the fixed line of code to the fixed.txt file.
                        if (
                            line[1] != "+"
                        ):  # If the line does not start with '++', the following operations are performed.
                            fixed_file.write(
                                " " + line[1:]
                            )  # The fixed file is written.
                    elif (
                        line[0]
                        == "-"  # If the line starts with '-', the following operations are performed.
                    ):  # Writes the wrong line of code to the buggy.txt file.
                        if (
                            line[1] != "-"
                        ):  # If the line does not start with '--', the following operations are performed.
                            buggy_file.write(
                                " " + line[1:]
                            )  # The buggy file is written.
                    else:  # If the line starts with ' ', the following operations are performed.
                        fixed_file.write(line)  # The fixed file is written.
                        buggy_file.write(line)  # The buggy file is written.

            file_close(fixed_file, buggy_file)  # The file_close function is called.
            # if fixed_file:
            # fixed_file.close()
            # if buggy_file:
            # buggy_file.close()
    except (
        Exception
    ) as e:  # If an error occurs, the following operations are performed.
        print(e)  # The error is printed.
        IS_FUNCTION = False  # The IS_FUNCTION variable is defined as False.


def file_close(fixed_file, buggy_file):
    """
    file_close function closes the files.

    Args:
        fixed_file: The fixed file to be processed.
        buggy_file: The buggy file to be processed.
    """
    if fixed_file:  # If the fixed file is not empty, it is closed.
        fixed_file.close()  # The fixed file is closed.
    if buggy_file:  # If the buggy file is not empty, it is closed.
        buggy_file.close()  # The buggy file is closed.


def skip_first_lines(file):
    """
    skip_first_lines function skips the first 4 lines in the commit diff file.

    Args:
        file: The commit diff file to be processed.
    """
    skipcount = 0  # The number of lines to be skipped is kept.
    while skipcount < 4:  # The first 4 lines are skipped.
        file.readline()  # The line is read.
        skipcount += 1  # The number of lines to be skipped is increased.


def check_dir_exists(fullpath):
    """
    check_dir_exists function checks if the bugfixed folder exists in the project folder.

    Args:
        fullpath: The path of the project folder to be processed.
    """
    os.chdir(fullpath)  # The path of the project folder is taken.
    os.chdir("../")  # The path of the project folder is taken.
    if not os.path.exists(
        "bugfixed"
    ):  # If the bugfixed folder does not exist, it is created.
        os.makedirs("bugfixed")  # The bugfixed folder is created.
        fullpath = (
            os.getcwd() + "/bugfixed"
        )  # The path of the bugfixed folder is taken.
        os.chdir(fullpath)  # The path of the bugfixed folder is taken.
        if not os.path.exists(
            "buggy_files"
        ):  # If the buggy_files folder does not exist, it is created.
            os.makedirs("buggy_files")  # The buggy_files folder is created.
        if not os.path.exists(
            "fixed_files"
        ):  # If the fixed_files folder does not exist, it is created.
            os.makedirs("fixed_files")  # The fixed_files folder is created.
        os.chdir("../")  # The path of the project folder is taken.


def seperate_diffs(folder_name):
    """
    seperate_diffs function seperates diff files to buggy and fixed files and writes them to the files folder in the bugfixed folder in the project folder.

    Args:
        folder_name: The name of the project folder to be processed.
    """
    path = pathlib.Path(
        __file__
    ).parent.resolve()  # The path of the project folder is taken.
    if not os.path.exists(
        str(path) + "/commit_tp/index_of_TP.txt"
    ):  # If the index_of_TP.txt file does not exist, it is created.
        with open(
            str(path) + "/commit_tp/index_of_TP.txt", mode="w+", encoding="utf-8"
        ) as index_file:  # The index_of_TP.txt file is created and the index values are written to the file.
            index_file.write("-1\n0")  # The index values are written to the file.
    with open(
        str(path) + "/commit_tp/index_of_TP.txt", mode="r", encoding="utf-8"
    ) as index_file:  # The index_of_TP.txt file is opened and the index values are read from the file.
        commit_index = int(
            index_file.readline()
        )  # The commit index value is read from the file.
        tp_index = int(
            index_file.readline()
        )  # The tp index value is read from the file.

    global BUGGY_COUNTER, FIXED_COUNTER  # The global variables are defined.
    BUGGY_COUNTER = (
        FIXED_COUNTER
    ) = tp_index  # The tp index value is assigned to the global variables.
    bugfixed_path = (
        str(path) + "/commit_tp/bugfixed"
    )  # The path of the bugfixed folder is assigned to the variable.
    fullpath = (
        str(path) + "/" + folder_name
    )  # The path of the project folder is assigned to the variable.
    const_path = fullpath  # The path of the project folder is assigned to the variable.
    os.chdir(fullpath)  # The path of the project folder is assigned to the variable.
    check_dir_exists(fullpath)  # The check_dir_exists function is called.
    os.chdir(const_path)  # The path of the project folder is assigned to the variable.
    file_list = (
        os.listdir()
    )  # The list of files in the project folder is assigned to the variable.
    file_list = natsort.natsorted(
        file_list
    )  # The list of files in the project folder is sorted.
    for dosya in file_list:  # The files in the project folder are processed.
        if dosya.endswith(
            ".txt"
        ):  # If the file is a txt file, it is processed and the diff files are separated into buggy and fixed files.
            if (
                int(dosya[:-4]) > commit_index
            ):  # If the commit index value is less than the file name, the file is processed.
                file_path = f"{const_path}/{dosya}"  # The path of the file is assigned to the variable.
                sep_file(file_path, bugfixed_path)  # The sep_file function is called.
                commit_index = int(
                    dosya[:-4]
                )  # The commit index value is assigned to the variable.
                tp_index = BUGGY_COUNTER  # The buggy counter value is assigned to the variable.
                with open(
                    str(path) + "/commit_tp/index_of_TP.txt",
                    mode="w+",
                    encoding="utf-8",
                ) as index_file:  # The index_of_TP.txt file is opened and the index values are written to the file.
                    index_file.write(
                        commit_index.__str__() + "\n" + tp_index.__str__()
                    )  # The index values are written to the file.
                if (
                    commit_index % 588021
                ) == 0 and commit_index != 0:  # If the commit index value is a multiple of 588021, the index values are written to the file.
                    exit()  # The program is terminated.

    os.chdir("../")  # The path of the project folder is assigned to the variable.
