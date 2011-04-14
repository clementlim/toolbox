#! /bin/bash
#
# @(#) $HOME/.bash_aliases
# $Id$
#

#--------------------------------------- http://tldp.org/LDP/abs/html/sample-bashrc.html

# cut last n lines in file, 10 by default.
cuttail()
{
    nlines=${2:-10}
    sed -n -e :a -e "1,${nlines}!{P;N;D;};N;ba" $1
}

# find a file with pattern $1 in name and execute $2 on it:
fe()
{
    find . -type f -iname '*'$1'*' -exec "${2:-file}" {} \;  
}

# find a file with a pattern in name:
ff()
{
    find . -type f -iname '*'$1'*' -ls
}

# find pattern in a set of files and highlight them:
fstr()
{
    OPTIND=1
    local case=""
    local usage="\
fstr: find string in files.
Usage: fstr [-i] \"pattern\" [\"filename pattern\"] "

    while getopts :it opt
    do
        case "$opt" in
            i)  case="-i "
                ;;
            *)  echo "$usage"
                return
                ;;
        esac
    done

    shift $(( $OPTIND - 1 ))
    if [ "$#" -lt 1 ]
    then
        echo "$usage"
        return;
    fi

    local SMSO=$(tput smso)
    local RMSO=$(tput rmso)

    find . -type f -name "${2:-*}" -print0 |    \
        xargs -0 grep -sn ${case} "$1" 2>&- |   \
            sed "s/$1/${SMSO}\0${RMSO}/gI" | more
}

# csh compatibility
setenv()
{
    export $1=$2
}

#--------------------------------------- The End
