import os, sys

# The following function solves the problem of trying to isolate the copy command exit code
# from the scons build. This also allows scons $SOURCE, and $TARGET to be passed in as arguments.
def copy( src, dest ):
  if sys.platform.startswith( 'win' ):
    win_src = src.replace( '/', '\\' )
    win_dest = dest.replace( '/', '\\' )
    os.system( 'copy /Y ' + win_src + ' ' + win_dest )
  else:
    os.system( 'cp -f ' + src + ' ' + dest )

if __name__ == '__main__':
  if len( sys.argv ) == 3:
    copy( sys.argv[1], sys.argv[2] )
  else:
    print "Usage: python copy.py <src> <dest>"
