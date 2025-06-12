
# detect_mcm_packages

affects: `detect_mcm_packages.py`, `external_files/makefile_top`

Mechanism to arbitrarily include "mcm latex packages" into the latex project.  
Like for instance a framework for createnig tikz images in general, or block 
diagrams in tikz.

A "mcm latex package" is a collection of latex source files, that at the top 
level has a file `mcm_package.yml`, which at least has a field `name`.  
A package **can** have a makefile, called `makefile` or `Makefile`. The purpose 
of the makefile could be providing test targets that only have to do with the 
specific package. Going back to our example, that could be a target to compile 
one only one figure and generate a standalone pdf file, during 
development/coding of that figure. The makefile is automatically included in the 
project top level makefile (see below). Packages need to be located in 
`<project_top>/mcm_packages`.

## package processing

The script `detect_mcm_packages.py` is invoked **during every parsing** (see 
section *invocation*) of the top-level makefile. It scans `<project_top>
/mcm_packages` for package directories, and creates/updates 2 files. Both files 
are created even if they end up being empty, such that no file existence check 
is necessary when including them:
- `<project_dir>/mcm_packages/mcm_package_defs.tex`
- `<project_dir>/mcm_packages/include_packages.mk`

### <project_dir>/mcm_packages/mcm_package_defs.tex

for every package, defines a latex variable `\path<name>Pkg`, which holds the 
path to the package top level directory, relative to the project top level 
directory (yes, that might be a bit over-engineered, but names of git 
directories containing git submodules can theoretically be whatever they want).
`<name>` is **exactly** the `name` field of `package.yml`. So it makes sense to 
provide that field in camel-case, to match the variable style, like `name: 
"TikzFigures"`.

The point of this variable is that inside the package latex code, you should use 
it for any reference to a file within a package. `mcm_package_defs.tex` is 
included by the project's default `main.tex` as one of the first files, so 
assuming that `main.tex` includes package files just after that, the variable is 
available. And if in some scenario one wants to run code in the package only, 
not embedded into a top level project, one just defines the variable in the 
respective tex main file. The paths would need to be relative to the package 
location then anyways (assuming that is the pwd for latex), instead of relative 
to a top level project directory.

Relative paths exclusively, because I'm running my latex inside a docker 
container, into which I only map the current project's top level directory, so 
that method can't work with absolute paths anywhere in the latex code.

### <project_dir>/mcm_packages/include_packages.mk

Per package that contains `makefile`/`Makefile`, this file contains three lines 
of code:
```
DIR_PKG_TIKZFIGURES_TOP_ABS := /.../<project_top_dir>/mcm_packages/<package_dir>
DIR_PKG_TIKZFIGURES_TOP_REL := mcm_packages/<package_dir>
include mcm_packages/<package_dir>/<makefile>
```

The top level includes only this file. In doing so:
* all package makefiles get included, and are available at the project top level 
  (notice that in the case of equal-named targets, top level overwrites the 
  package targets)
* the package makefiles automatically have absolute and project-relative path 
  variables to their location at their disposal, for example for setting 
  a `${PKG_TOP}`. Which does not prevent them from defining these, or any 
  derived variables, themselves, if the paths are not present (`?=`), such that 
  the package makefiles can both operate embedded, or standalone.

## Invocation

Since the generated files affect the makeflow itself, not only the source code 
(in that `include_packages.mk` likely makes targets accessible), ideally the 
files would be generated **before** running any make target. That is "sort of" 
achieved by calling the script inside a dummy variable definition in the top 
level makefile, which makes the call part of the makefile parsing, prior to 
execution. So the package targets are accessible right-away, but they won't show 
up in auto-completion if the package has just be added. (Another note, yes I do 
note that it's not really necessary to re-generate the files every time that any 
make target is called, but I just considered the overhead neglectable)

The dummy invocation:
```
DUMMY_PREPARE_MCM_PKGS := $(shell python3 ${SCRIPT_DETECT_MCM_PKGS} ${DIR_PRJ_TOP})
```

## Roadmap

### Dependencies

An idea for the future is to support a `dependency` field in `package.yml`, via 
which would allow one package to safely import latex code or make targets from 
another one. But I haven't put too much thought into that yet, on if that 
actually solves any problem at some point, and what would need to be done for 
that. But it's kind of the logical step when speaking about any sort of package 
system, isn't it?

