""" Lexico grapher
    Lexico grapher separates abstracted python source codes into tokens with the python tokenizer. In this way, it creates the dictionary structure of the data set.
    tokenize_abst_files takes the abstracted source code and starts the tokenization process. Obtained tokens are kept in token_dict.
    The token_dict keeps the token and its usage frequency in the dictionary structure. Finally, it creates the vocabulary by writing this data to the a txt file.
"""

import os
import tokenize


def tokenize_abst_files(
    file_type, token_dict, token_list, abstract_folder_path, action_type
):
    """
    tokenize_abst_files functions tokenize abstracted files and create vocabulary
    :param file_type: type of file
    :param token_dict: dictionary of tokens
    :param token_list: list of tokens
    :param abstract_folder_path: path of abstracted files' folder
    """
    with open(
        "commit_tp/" + action_type + "/indexlist.txt", mode="r", encoding="utf-8"
    ) as indexfile:
        indexlist = indexfile.read().splitlines()
    for index in indexlist:
        if os.path.exists(abstract_folder_path + index.__str__() + ".txt"):
            flag = 0
            file_name = abstract_folder_path + index.__str__() + ".txt"
            with open(file_name, mode="rb") as current_file:
                tokens = tokenize.tokenize(
                    current_file.readline
                )  # The source code is opened in read binary mode and split into tokens with the python tokenizer.
                enum = 0
                for i in tokens:
                    if enum == 0:
                        enum += 1
                        continue

                    token_list.append(i[1])
                    enum += 1
                if flag == 1:
                    token_list.clear()
                    current_file.close()
                    continue
                else:
                    # Checks if the token already exists. If the token already exists, its frequency is increased 1, if not, it is added to the dictionary.
                    for i in token_list:
                        if i in token_dict.keys():
                            token_dict[str(i)] += 1
                        else:
                            token_dict[str(i)] = 1
                    token_list.clear()
    # if file_type == 'fixed':
    #     # fixedvocab = open('fixedvocab.txt', 'a+', encoding = 'utf-8')
    #     with open('fixedvocab.txt', mode = 'a+',encoding = 'utf-8') as fixedvocab:
    #         fixedvocab.truncate(0)
    #         fixedvocab.seek(0)
    #         token_dict = dict(
    #             sorted(
    #                 token_dict.items(),
    #                 key=lambda item: item[1],
    #                 reverse=True))
    #         for key,value in token_dict.items():
    #             fixedvocab.write(str(key) + ' ' + str(value))
    #             fixedvocab.write("\n")
    #         fixedvocab.close()
    # elif file_type == 'buggy':
    #     with open('buggyvocab.txt', mode = 'a+',encoding = 'utf-8') as buggyvocab:
    #         buggyvocab.truncate(0)
    #         buggyvocab.seek(0)
    #         token_dict = dict(
    #             sorted(
    #                 token_dict.items(),
    #                 key=lambda item: item[1],
    #                 reverse=True))
    #         for i in token_dict.keys():
    #             buggyvocab.write(str(i) + ' ' + str(token_dict[i]))
    #             buggyvocab.write("\n")
    #         buggyvocab.close()
    write_vocab(file_type, token_dict, action_type)
    return token_dict


def write_vocab(file_type, token_dict, action_type):
    """
    write_vocab creates a vocabulary by writing the obtained token and token frequencies into a txt file.
    :param file_type: type of dataset (fixed-buggy)
    :param token_dict: dictionary structure where all tokens are held
    """
    if file_type == "fixed":
        # fixedvocab = open('fixedvocab.txt', 'a+', encoding = 'utf-8')
        with open(
            "commit_tp/" + action_type + "/fixedvocab.txt", mode="a+", encoding="utf-8"
        ) as fixedvocab:
            # resets the cursor of the txt file
            fixedvocab.truncate(0)
            fixedvocab.seek(0)
            token_dict = dict(
                sorted(token_dict.items(), key=lambda item: item[1], reverse=True)
            )
            # In the token dictionary structure, it walks on the key and values.
            for key, value in token_dict.items():
                fixedvocab.write(str(key) + " " + str(value))
                fixedvocab.write("\n")
            fixedvocab.close()
    elif file_type == "buggy":
        with open(
            "commit_tp/" + action_type + "/buggyvocab.txt", mode="a+", encoding="utf-8"
        ) as buggyvocab:
            # resets the cursor of the txt file
            buggyvocab.truncate(0)
            buggyvocab.seek(0)
            token_dict = dict(
                sorted(token_dict.items(), key=lambda item: item[1], reverse=True)
            )
            # In the token dictionary structure, it walks on the key and values.
            for key, value in token_dict.items():
                buggyvocab.write(str(key) + " " + str(value))
                buggyvocab.write("\n")
            buggyvocab.close()


def create_vocab(file_type, abstract_folder_path, action_type):
    """
    create_vocab functions calls tokenize_abst_files function.
    :param file_type: type of file
    :param abstract_folder_path: path of abstracted files' folder
    """
    token_dict = {}
    token_list = []
    new_list = []
    token_dictionary = tokenize_abst_files(
        file_type, token_dict, token_list, abstract_folder_path, action_type
    )
    # Tokens with more than 50 in the token dictionary must be eliminated. So this check is done inside the for loop.
    for key in token_dictionary:
        if token_dictionary[key] < 50:
            new_list.append(key)
    token_dict.clear()
    return new_list
