#!/usr/bin/env python3

# detect mcm latex packages in `<project_dir>/mcm_packages`, and set up a latex 
# file with relative path definitions that the latex codebase can use to 
# reference the packages
# packages are identified by being a directory in `<project_dir>/mcm_packages` 
# which hold a file called `mcm_package.yml`. No nesting, no other hierarchy 
# levels.
# `mcm_package.yml` holds information about the package, like 'name' (and FUTURE: 
# 'depends')
#
# $1: project top level directory absolute path
# It creates/updates 2 files (even if they end up being empty), such that the 
# main latex code and makefile can safely include these:
# - `<project_dir>/.mcm_package_defs.tex`
#   -> assuming there is
# - `<project_dir>/mcm_packages/include_packages.mk` which includes any 
# `makefile`/`Makefile` that was found in an mcm_package (FUTURE: in dependency 
# order, if any given in the yml)
#   -> allows packages to specify make commands that are accessible from the 
#   project top level, for example for standalone creating a specific tikz 
#   figure during development
#
# TODO: create the tex definitions and the makefile include files from the 
# packages list

import sys
import os
import yaml


DIRNAME_MCM_PKGS            = "mcm_packages"
FILENAME_MCM_PKG_DEFS_TEX   = ".mcm_package_defs.tex"


class McmPackage(object):

    """
    """

    def __init__(self, name="", path="", dict_pkg={}):
        """

        ('name' and 'path' fields each take precedence over their counterpart in 
        'dict_pkg')

        :dict_pkg: is meant to come from McmPackage.from_yaml
        """

        if not name and not dict_pkg:
            raise Exception("name and dict_pkg can't both be empty")

        if dict_pkg:
            self.name = dict_pkg["name"]
        if name:
            self.name = name

        if dict_pkg:
            self.path = dict_pkg["path"]
        if path:
            self.path = path

        # TODO: handle if dict_pkg contains a 'depends' field (but then also 
        # accept if it doesn't)

        # detect makefile (leave field empty if there is none)
        self.makefile = ""
        if os.path.isfile(os.path.join(self.path, "makefile")):
            self.makefile = "makefile"
        if os.path.isfile(os.path.join(self.path, "Makefile")):
            self.makefile = "Makefile"

    def __str__(self):
        return "name: " + self.name + " - path: " + self.path + \
                    " - makefile: " + self.makefile

    @classmethod
    def from_yaml(cls, yaml_file, relpath=True):
        """
        get McmPackage object from a detected mcm_package.yml

        :relpath: if True, sets up the McmPackage object with a relative path, 
        instead of just using the raw yaml_file path (which may or may not be 
        relative). relative path will be yaml_file, minus anything that preceeds 
        DIRNAME_MCM_PKGS, and minus the filename of course.
        """

        with open(yaml_file, 'r') as file_in:
            d_package = yaml.safe_load(file_in)
        if relpath:
            # https:
            # //stackoverflow.com/questions/33141595/how-can-i-remove-everything-in-a-string-until-a-characters-are-seen-in-python
            d_package['path'] = \
                    os.path.dirname(yaml_file[yaml_file.find(DIRNAME_MCM_PKGS):])
        else:
            d_package['path'] = os.path.dirname(yaml_file)

        return cls(dict_pkg=d_package)
        

def detect_packages(abs_path_prj_top):
    """
    Detect all packages in the given location (see file top comment about 
    detecting "packages")

    :dir_mcm_packages: TODO
    :returns: list of McmPackage objects (in no semantic order). Makes sure that 
    all objects are set up with relative paths, not absolute paths (if you 
    wanted to overengineer it even more you should make that parameterizable, 
    but I only need the relative path version because I'm running latex inside 
    a docker container, doesn't work with absolute paths)
    """

    abs_path_mcm_packages = os.path.join(abs_path_prj_top,DIRNAME_MCM_PKGS)
    l_package_candidate_dirs = os.listdir(abs_path_mcm_packages)

    l_mcm_packages = [ \
            McmPackage.from_yaml(os.path.join(abs_path_mcm_packages,x,"mcm_package.yml")) \
            for x in l_package_candidate_dirs if \
            os.path.isfile(os.path.join(abs_path_mcm_packages,x,"mcm_package.yml"))]

    return l_mcm_packages


def write_latex_path_defs(project_dir, l_mcm_packages):
    """
    generate <project_dir>/.mcm_package_defs.tex
    """


def main(abs_path_prj_top):
    l_mcm_packages = detect_packages(abs_path_prj_top)
    [print(x) for x in l_mcm_packages]
    pass


if __name__ == "__main__":
    abs_path_prj_top = sys.argv[1]
    main(abs_path_prj_top)
