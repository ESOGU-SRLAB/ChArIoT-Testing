def write_to_file(file, diff_list):
    file.write("-------------------------------\n")
    for i in range(diff_list.__len__()):
        file.write(str(diff_list[i]) + "\n")
    file.write("-------------------------------")