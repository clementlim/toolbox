# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

export PATH=$PATH:$HOME/bin

export MYREPO=http://my-svn.assembla.com/svn/clementlim
export SVN_EDITOR=emacs