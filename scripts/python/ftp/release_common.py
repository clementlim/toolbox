import os, sys, re
from ftp_common import FTPCommon

ftp_common = FTPCommon()

class ReleaseCommon:
  def setup_dir_for_transfer( self, FINCAD_ROOT, ftp, target_dir, release_folder_name ):
    ftp_common.safe_cwd( ftp, target_dir )
    ftp_common.safe_cwd( ftp, self.get_branch( FINCAD_ROOT ) )
    ftp_common.safe_cwd( ftp, release_folder_name )

    ( files, _ ) = ftp_common.get_ftp_dirs_files( ftp, ftp.pwd() )
    tgz_file = self.build_tgz_name( FINCAD_ROOT )
    if tgz_file in files:
        ftp_common.delete_file( ftp, tgz_file )

  def transfer_build_artifacts( self, FINCAD_ROOT, ftp, target_dir, release_folder_name, bld_prod_dirs ):
    for src_dir in bld_prod_dirs:
        if os.path.exists( src_dir ) and not bld_prod_dirs[ src_dir ] == '':
            print "Creating folder: " + bld_prod_dirs[ src_dir ]
            ftp.mkd( bld_prod_dirs[ src_dir ] )
            ftp.cwd( bld_prod_dirs[ src_dir ] )
            ftp_common.transfer_dir( ftp, src_dir )
            ftp.cwd( '..' )
        else:
            ftp_common.transfer_dir( ftp, src_dir )
    
  def safe_rmdir( self, dir ):
    if not os.path.exists( dir ):
        return

    child_folders = [ entry for entry in os.listdir( dir ) if os.path.isdir( os.path.join( dir, entry ) ) ]
    child_files = [ entry for entry in os.listdir( dir ) if entry not in child_folders ]

    for child_file in child_files:
        os.remove( os.path.join( dir, child_file ) )

    for child_folder in child_folders:
        self.safe_rmdir( os.path.join( dir, child_folder ) )

    os.rmdir( dir )

  def safe_mkdir( self, dir ):
    if os.path.exists( dir ):
        return

    self.safe_mkdir( os.path.dirname( dir ) )
    os.mkdir( dir )

  def get_hostname( self ):
    hostname_raw = os.popen( "hostname", 'r' ).read()
    hostname = hostname_raw.split( '.' )[0].rstrip()

    return hostname

  def get_revision( self, FINCAD_ROOT ):
    svn_info = os.popen( "svn info " + FINCAD_ROOT, 'r' ).read()
    revision = ''
    for line in svn_info.splitlines():
        if re.match( 'Revision: ', line ):
            revision = line.split( ':' )[1].lstrip()
    return revision

  def get_branch( self, FINCAD_ROOT ):
    svn_info = os.popen( "svn info " + FINCAD_ROOT, 'r' ).read()
    branch = ''
    for line in svn_info.splitlines():
        if re.match( 'URL: ', line ):
            branch = line.split( '/' )[-1]
    return branch

  def get_tgz_dir( self, FINCAD_ROOT ):
    return os.path.join( FINCAD_ROOT, 'build', 'tgz' )

  def build_tgz_name( self, FINCAD_ROOT ):
    return 'f3_' + self.build_type_info( FINCAD_ROOT ) + '.tgz'

  def build_generic_tgz_name( self, FINCAD_ROOT ):
    return 'f3_generic_' + self.build_type_info( FINCAD_ROOT ) + '.tgz'  

  def build_type_info( self, FINCAD_ROOT ):
    if self.get_build_type() == 'doc':
        return self.get_build_type() + '_' + self.get_bit_count()
    else:
        return self.get_build_type() + '_' + self.get_bit_count() + '_bin'

  def get_bit_count( self ):
    if os.environ.has_key('F3_BIT_COUNT'):
        return os.environ['F3_BIT_COUNT']
    return "unknown"

  def get_build_type( self ):
    if os.environ.has_key('F3_BUILD_TYPE'):
        return os.environ['F3_BUILD_TYPE']
    return "unknown"
