import os, sys
from ftplib import FTP

class FTPCommon:
  def ftp_connect( self, server, username, password ):
    ftp = FTP( server )
    print "Connecting to " + server
    print ftp.login( username, password )
    ftp.set_pasv( True )
    return ftp

  def ftp_quit( self, ftp ):
    print ftp.quit()

  def get_ftp_dirs_files( self, ftp, dir ):
    dir_listing = []
    # using LISTS -a instead of dir() to list invisible files and directories
    ftp.retrlines( 'LIST -a ' + dir, dir_listing.append )

    # removing current and parent directory entries as they are not really directories e.g. '.' and '..' )
    for f in [ f for f in dir_listing if f.startswith( 'd' ) and ( f.endswith( '.' ) or f.endswith( '..' ) ) ]:
      dir_listing.remove( f )

    files = [ f.split( None, 8 )[ -1 ] for f in dir_listing if f.startswith( '-' ) ]
    dirs = [ f.split( None, 8 )[ -1 ] for f in dir_listing if f.startswith( 'd' ) ]

    return ( files, dirs )

  def safe_cwd( self, ftp, dir ):
    ( _, dirs )= self.get_ftp_dirs_files( ftp, ftp.pwd() )
    if not dir in dirs:
      print "Creating directory: " + dir
      ftp.mkd( dir )
    ftp.cwd( dir )

  def get_dsk_dirs_files( self, dir ):
    # unbroken symbolic links will be resolved as files and transferred as such;
    # all broken symbolic links are discarded.
    dir_listing = os.listdir( dir )
    files = [ f for f in dir_listing if os.path.isfile( os.path.join( dir, f ) ) ]
    dirs = [ f for f in dir_listing if os.path.isdir( os.path.join( dir, f ) ) ]
    return ( files, dirs )

  def download_ftp_file( self, ftp, dest_dir, file ):
    print "Downloading " + file
    tgt_file = open( os.path.join( dest_dir, file ), 'wb' )
    ftp.retrbinary( 'RETR ' + file, tgt_file.write )
    tgt_file.close()

  def upload_ftp_dir( self, ftp, src_dir ):
    ( files, dirs ) = self.get_dsk_dirs_files( src_dir )

    if dirs:
      for dir in dirs:
        ( _, ftp_dirs ) = self.get_ftp_dirs_files( ftp, ftp.pwd() )
        if dir not in ftp_dirs:
          print "Creating FTP folder: " + dir
          ftp.mkd( dir )
        ftp.cwd( dir )
        self.upload_ftp_dir( ftp, os.path.join( src_dir, dir ) )
        ftp.cwd( '..' )

    for file in files:
      print "Transferring file: " + os.path.join( src_dir, file )
      f = open( os.path.join( src_dir, file ), 'rb' )
      try:
        ftp.storbinary( 'STOR ' + file, f )
      except:
        print "Error transferring " + file
        sys.exit( 1 )
      f.close()

    return
  
  def delete_ftp_file( self, ftp, target_file ):
    ftp.delete( target_file )

  def delete_ftp_dir( self, ftp, target_dir ):
    target_dir = self.sanatize_path( target_dir )
    ( files, dirs ) = self.get_ftp_dirs_files( ftp, target_dir )

    # if no files or sub-dirs, delete target dir and return
    if not files and not dirs:
        print "Deleting folder: " + target_dir
        ftp.rmd( target_dir )
        return

    for dir in dirs:
        print "Entering folder: " + os.path.join(target_dir, dir )
        self.delete_dir( ftp, os.path.join( target_dir, dir ) )

    for file in files:
        file_abspath = os.path.join( target_dir, file )
        file_abspath = self.sanatize_path( file_abspath )
        print "Deleting file: " + file_abspath
        ftp.delete( file_abspath )

    print "Deleting folder: " + target_dir
    ftp.rmd( target_dir )
