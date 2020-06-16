#!/bin/bash

# in some areas, we usually can not use go get -u /url/to/golang-packet to get some useful golang tools(eg. code insight for IDE)
# this script get these tools from source code.
# and toollist is base on vscode-golang-recommend, so we can add other tools we like.
# has some todo!!!

hasCommand() {
    if type $1 >/dev/null 2>&1; then
        return 0 # succ
    else
        return 1 # err
    fi
}
# or can check this like following:
# type $1 >/dev/null 2>&1 || { echo >&2 "xxx."; exit 1; } 
# type or command -v is ok, do not use which, because which may not shell builtin.
# because not 0 mean err, so 1 || any equals true.

hasCommand go
if ! [ 0 -eq $? ]; then
    echo "[-] Can't find command go!" >&2
    echo '    please install golang or export /path/to/bin/go to $PATH' >&2
    exit 1
fi

hasCommand git
if ! [ 0 -eq $? ]; then
    echo "[-] Can't find command git!" >&2
    echo '    please install git or export /path/to/bin/git to $PATH' >&2
    exit 1
fi

# todo: 1. check go version
#   go version go1.8.1 linux/amd64 > 1.10!!!

# if ! [ -x type go >/dev/null 2>&1 ]; then
#     it seems that is not working, why?
# fi

if [ ! -d "$(go env GOPATH)/src" ]; then
    mkdir -p "$(go env GOPATH)/src"
fi
pushd "$(go env GOPATH)/src" > /dev/null

# for more detail, please see https://github.com/Microsoft/vscode-go/wiki/Go-tools-that-the-Go-extension-depends-on
toollist=(
    golang.org/x/net
    golang.org/x/xerrors
    golang.org/x/tools # gorename for renaming symbols
                       # guru for the Find all References feature
                       # godoc for the documentation that appears on hover
                       #     has 2 dependency: (1)golang.org/x/net (2)golang.org/x/xerrors
    golang.org/x/lint  # golint or megacheck or golangci-lint or revive for linting
    github.com/mdempsky/gocode # for auto-completion (not needed if using language server)
    github.com/uudashr/gopkgs # for auto-completion of unimported packages
                              # has 2 dependency: (1)github.com/karrick/godirwalk (2)github.com/pkg/errors
    github.com/ramya-rao-a/go-outline # for symbol search in the current file
    github.com/acroca/go-symbols # for symbol search in the current workspace
    # github.com/cweill/gotests # for generating unit tests
    github.com/fatih/gomodifytags # for modifying tags on structs
    github.com/josharian/impl # for generating stubs for interfaces
    github.com/davidrjenni/reftools # refactoring tools for Go (just use cmd/fillstruct)
    # github.com/skratchdot/open-golang
    # github.com/haya14busa/goplay # for running current file in the Go playground
    #                              # has 1 dependency: (1)github.com/skratchdot/open-golang
    # github.com/godoctor/godoctor # The Golang Refactoring Engine
    github.com/go-delve/delve # for debugging
    # github.com/stamblerre/gocode # For a version of gocode that works with Modules
    github.com/rogpeppe/godef # for the Go to Definition feature (not needed if using language server)
    github.com/zmb3/gogetdoc  # for the documentation that appears on hover (not needed if using language server)
)

# todo: 2. check git succ? =No=> skip some work(go install && dependency)
#       3. make a log: stdout and stderr!
#       4. opt the toollist, make the connection between toollist and git/go cmd.

# must install tools and lint firstly
git clone https://github.com/golang/net.git golang.org/x/net --depth=1
git clone https://github.com/golang/xerrors.git golang.org/x/xerrors --depth=1
git clone https://github.com/golang/tools.git golang.org/x/tools --depth=1
git clone https://github.com/golang/lint.git golang.org/x/lint --depth=1
go install golang.org/x/tools/cmd/gorename
go install golang.org/x/tools/cmd/guru
go install golang.org/x/tools/cmd/godoc
go install golang.org/x/lint/golint

git clone https://github.com/mdempsky/gocode.git  github.com/mdempsky/gocode --depth=1
go install github.com/mdempsky/gocode

git clone https://github.com/karrick/godirwalk.git github.com/karrick/godirwalk --depth=1 # don't install
git clone https://github.com/pkg/errors.git github.com/pkg/errors --depth=1 # don't install
git clone https://github.com/uudashr/gopkgs.git github.com/uudashr/gopkgs --depth=1 # has 2 dependency
go install github.com/uudashr/gopkgs/cmd/gopkgs

git clone https://github.com/ramya-rao-a/go-outline.git github.com/ramya-rao-a/go-outline --depth=1
go install github.com/ramya-rao-a/go-outline

git clone https://github.com/acroca/go-symbols.git github.com/acroca/go-symbols --depth=1
go install github.com/acroca/go-symbols

# git clone https://github.com/cweill/gotests.git github.com/cweill/gotests --depth=1
# go install github.com/cweill/gotests

git clone https://github.com/fatih/gomodifytags.git github.com/fatih/gomodifytags --depth=1
go install github.com/fatih/gomodifytags

git clone https://github.com/josharian/impl.git github.com/josharian/impl --depth=1
go install github.com/josharian/impl

git clone https://github.com/davidrjenni/reftools.git github.com/davidrjenni/reftools --depth=1
go install github.com/davidrjenni/reftools/cmd/fillstruct
	
# git clone https://github.com/skratchdot/open-golang.git github.com/skratchdot/open-golang --depth=1 # don't install
# git clone https://github.com/haya14busa/goplay.git github.com/haya14busa/goplay --depth=1 # has 1 dependency
# go install github.com/haya14busa/goplay/cmd/goplay

# git clone https://github.com/godoctor/godoctor.git github.com/godoctor/godoctor --depth=1
# go install github.com/godoctor/godoctor

git clone https://github.com/go-delve/delve.git github.com/go-delve/delve --depth=1
go install github.com/go-delve/delve/cmd/dlv
	
# git clone https://github.com/stamblerre/gocode.git github.com/stamblerre/gocode --depth=1
# go install github.com/stamblerre/gocode

git clone https://github.com/rogpeppe/godef.git github.com/rogpeppe/godef --depth=1
go install github.com/rogpeppe/godef

git clone https://github.com/zmb3/gogetdoc.git github.com/zmb3/gogetdoc --depth=1
go install github.com/zmb3/gogetdoc

popd > /dev/null


# issue:
# Q: golang.org/x/tools/go/internal/gcimporter/bexport.go:212: obj.IsAlias undefined (type *types.TypeName has no field or method IsAlias)
# A: just support go version > 1.9(https://github.com/golang/lint/issues/421)
#
