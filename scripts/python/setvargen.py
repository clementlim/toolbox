#!/usr/bin/env python

import os, sys, stat

def setvargen( basename, args ):
    if sys.platform.startswith( 'win' ):
        platform = { 'script_ext' : '.bat',
                     'set_var_cmd' : 'set',
                     'echo_off_opt' : '@echo off',
                     'print_cmd' : 'echo' }        
    else:
        platform = { 'script_ext' : '.sh',
                     'set_var_cmd' : 'export',
                     'echo_off_opt' : '',
                     'print_cmd' : 'echo' }

    setvarname = basename + platform[ 'script_ext' ]

    f = open( setvarname, 'w' )
    f.write( platform[ 'echo_off_opt' ] + '\n' + platform[ 'print_cmd' ] + ' Setting environment variables...\n' )
    while args:
        f.write( platform[ 'print_cmd' ] + ' %s=%s\n' % tuple( args[:2] ) + platform[ 'set_var_cmd' ] + ' %s=%s\n' % tuple( args[:2] ) )
        del args[:2]
    f.write( platform[ 'print_cmd' ] + ' Done.\n' )
    f.close()
    os.chmod( setvarname, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO )

if __name__ == '__main__':
    if len( sys.argv ) > 2:
        setvargen( sys.argv[1], sys.argv[2:] )
    else:
        print "Usage: python setvargen.py <setvar_basename> var1 value1 var2 value2 ... varN valueN"
