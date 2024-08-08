#!/usr/bin/env python3

# Scan all subdirectories of src, interpret them as chapters and write 
# chapters.tex to include all of these chapters. Additionally, a file for every 
# subdirectory is added in src to define the chapter in latex and include the 
# files in the according chapter directory. This way, building the document via 
# makefile will always automatically include every new file if there is one on a 
# tool or feature that had no type of documentation or note to this point.
# TODO: think about if it is useful to somewhere specify the order of the added 
# chapters. So far, it will just be straightforward alphabetically.

import os
import glob

file_chapters_tex = "chapters.tex"


def str_to_title(string):
    '''
    In principle just take the string and capitalize the first letter (as 
    directory names are nicer if written non-capitalized and the chapter names 
    are taken from the list of src directories). Can also handle multi-word 
    strings: "first_chapter" -> "First Chapter"
    '''

    list_string = string.split('_')
    title = " ".join(
            [s[0].capitalize() + s[1:] for s in list_string])

    return title


def write_chapter_file(chapter, chapter_folder=""):
    if not chapter_folder:
        chapter_folder = chapter

    with open(f"src/{chapter}.tex", 'w') as f_chapter:
        f_chapter.write(
"""% !!! This file has been automatically generated by include_chapters.py. Do not 
% edit it because your edits are very likely to soon be overwritten !!!

\chapter{""" + str_to_title(chapter) + """}
\label{cha:""" + chapter.lower() + """}

""")

        files_sections = glob.glob(f"src/{chapter_folder}/*.tex")
        for file_section in files_sections:
            f_chapter.write("\input{" + file_section+ "}\n")


def write_chapter_include_file(chapters):
    with open(file_chapters_tex, 'w') as f_chapters:
        f_chapters.write(
"""% !!! This file has been automatically generated by include_chapters.py. Do not 
% edit it because your edits are very likely to soon be overwritten !!!

""")

        for chapter in chapters:
            f_chapters.write("\input{src/" + chapter + ".tex}\n")


def main():
    # DETECT CHAPTERS
    chapters_unordered = [ch for ch in os.listdir("src/{ch}")]

    # FINAL CHAPTER LIST IN ORDER
    # 1. take every entry from the order file as the first chapters
    # 2. if any detected chapters are left, append them to the chapter list in 
    # whatever order
    with open("chapter_order", 'r') as f_chapter_order:
        chapters = f_chapter_order.readlines()
        chapters = [s.removesuffix('\n') for s in chapters]

    remaining_chapters = [chapter for chapter in chapters_unordered if chapter
                          not in chapters]
    if remaining_chapters:
        chapters.append(remaining_chapters)

    # TOP-LEVEL TEX FILES
    # write chapter top-level tex files
    print(chapters)
    for chapter in chapters:
        write_chapter_file(chapter)

    # CHAPTER INCLUDE FILE
    # write chapter include file
    write_chapter_include_file(chapters)


if __name__ == "__main__":
    main()
