""" This module downloads the diff files of the commits in the commit list file and saves them to the diffTexts folder."""

import os
import time
import requests


def delete_lines_by_index(line_list, index: int):
    """Delete the lines in the list up to the given index.

    Args:
        line_list: List of lines.
        index (int): Index to delete.
    """
    del line_list[: index + 1]


def save_diff(repository_name: str, commit_hash: str, index_list) -> int:
    """Download the diff file of the commit and save it to the diffTexts folder.

    Args:
        repository_name (str): Repository name of the commit.
        commit_hash (str): Commit hash number.
        index_list: List of indexes to keep track of the number of files downloaded.

    Returns:
        int: Returns 1 if the file is downloaded, 0 if not.
    """

    # Create the url of the diff file.
    url = "https://github.com/" + repository_name + "/commit/" + commit_hash + ".diff"

    try:
        # Get the diff file.
        req = requests.get(url, allow_redirects=True)

        # If the diff file is found.
        if req.status_code == 200:

            i = req.text.find("\n")  # Find the first line break.

            # If the diff file is empty.
            if i == -1:

                index_list[0] += 1  # Increase the index.

                return 0  # Return 0 because the file is not downloaded.

            # If the diff file is not empty and the file extension is .py using the last 3 characters.
            if req.text[i - 3] + req.text[i - 2] + req.text[i - 1] == ".py":

                # Create the file name.
                file_name = "commit_tp/diffTexts/" + str(index_list[1]) + ".txt"
                # Create the file and write the diff file to it.
                with open(file_name, mode="w+", encoding="utf-8") as file:
                    file.write(req.text)

                index_list[1] += 1  # Increase the file index.
                index_list[0] += 1  # Increase the index.

                return 1  # Return 1 because the file is downloaded.

            index_list[0] += 1  # Increase the index.

            return 0  # Return 0 because the file is not downloaded.

        index_list[0] += 1  # Increase the index.

        return 0  # Return 0 because the file is not downloaded.

    except requests.ConnectionError:  # If the connection is lost.
        return 0  # Return 0 because the file is not downloaded.


def commit_to_diff(diff_file_name: str, diff_folder_name: str):
    """Download the diff files of the commits in the commit list file and save them to the diffTexts folder.

    Args:
        diff_file_name (str): Diff file name.
        diff_foldername (str): Diff folder name.
    """

    # Create the diffTexts folder if it does not exist.
    if not os.path.exists(diff_folder_name):
        os.makedirs(diff_folder_name)

    # Create the indexInfo folder if it does not exist.
    if not os.path.exists("commit_tp/diffTexts/indexInfo"):
        os.makedirs("commit_tp/diffTexts/indexInfo")

    # Create the indexInfo.txt file if it does not exist.
    if not os.path.exists("commit_tp/diffTexts/indexInfo/indexInfo.txt"):
        # Create the indexInfo.txt file and write the indexes to it.
        with open(
            "commit_tp/diffTexts/indexInfo/indexInfo.txt", mode="w+", encoding="utf-8"
        ) as index_file:
            index_file.write(
                "0\n0"
            )  # The first line is the index of the commit list file, the second line is the index of the diff file.

    index_list = []  # List of indexes to keep track of the number of files downloaded.

    # Read the indexes from the indexInfo.txt file.
    with open(
        "commit_tp/diffTexts/indexInfo/indexInfo.txt", mode="r", encoding="utf-8"
    ) as index_file:
        index = int(index_file.readline())  # Read the index of the commit list file.
        file_index = int(index_file.readline())  # Read the index of the diff file.

    index_list.append(index)  # Add the index of the commit list file to the list.
    index_list.append(file_index)  # Add the index of the diff file to the list.

    # Read the commit list file.
    with open(diff_file_name, mode="r", encoding="utf-8") as file:
        lines = file.readlines()  # Read the lines of the file.
        line_list = lines.splitlines()  # type: ignore # Split the lines of the file.

    # Delete the lines in the list up to the given index.
    delete_lines_by_index(line_list, index_list[0])

    line = line_list[0]  # Get the first line.
    line_list.pop(0)  # Delete the first line.

    start_time = time.time()  # Start time.

    # While there is a line in the list.
    while line != "":
        # In the file where the commit information is located, the information in which a commit is found is kept as 'commit hash number, repository name'. This information is obtained with split(,).
        before_comma, after_comma = line.split(",")

        # Download the diff file of the commit and save it to the diffTexts folder.
        save_diff(after_comma, before_comma, index_list)

        print(index_list)  # Print the index list.

        line = line_list[0]  # Get the first line.
        line_list.pop(0)  # Delete the first line.

        # Write the indexes to the indexInfo.txt file.
        with open(
            "commit_tp/diffTexts/indexInfo/indexInfo.txt", mode="w+", encoding="utf-8"
        ) as index_file:
            index_file.write(
                str(index_list[0]) + "\n" + str(index_list[1])
            )  # Write the indexes to the file.

    end_time = time.time()  # End time.

    print(
        str(index_list[0])
        + " files downloaded in "
        + str(end_time - start_time)
        + " seconds."
    )  # Print the number of files downloaded and the time it took to download them.
