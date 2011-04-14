import os, sys, stat

def delete( target ):
  if not ( os.path.exists( target ) or os.path.islink( target ) ):
    print target + " doesn't exists!"
  else:
    # make writable if read only
    mode = os.lstat( target )[stat.ST_MODE]
    if not mode & stat.S_IWRITE:
      os.chmod( target, stat.S_IWRITE )

    if os.path.isfile( target ) or os.path.islink( target ):
      os.remove( target )
    elif os.path.isdir( target ):
      items = os.listdir( target )
      for item in items:
        delete( os.path.join( target, item ) )
      os.rmdir( target )
    else:
      print "target is neither dir nor file, unsure of what to do!"

if __name__ == '__main__':
  if len( sys.argv ) == 2:
    delete( sys.argv[1] )
  else:
    print "Usage: python delete.py <target>"
