import os, sys, commands, re, tarfile, stat
import ftp_config
from ftplib import FTP
from ftp_common import FTPCommon
from release_common import ReleaseCommon

ftp_common = FTPCommon()
release_common = ReleaseCommon()

def ftp_transfer( server = ftp_config.ftp_server, target_dir = ftp_config.ftp_target_dir ):
  FINCAD_ROOT = os.getcwd()
  # parameters format: ( source_folder, archive_folder )
  bld_prod_dirs = { os.path.join( FINCAD_ROOT, 'build', 'stage' ) : os.path.join( 'build_stage', release_common.get_build_type(), release_common.get_bit_count() ),
                    os.path.join( FINCAD_ROOT, 'build', 'doc', 'stage' ) : os.path.join( 'doc_stage' ),
                    os.path.join( FINCAD_ROOT, 'src', 'iflayer', 'fcf3', 'include', 'public', 'fcf3' ) : os.path.join( 'include' ) }

  tgz_folder = release_common.get_tgz_dir( FINCAD_ROOT )
  create_tgz( tgz_folder, bld_prod_dirs, FINCAD_ROOT )

  release_folder_name = 'r' + release_common.get_revision( FINCAD_ROOT )
  username = 'uploader'
  password = 'P0s1t1ve'

  ftp = ftp_common.ftp_connect( server, username, password )
  release_common.setup_dir_for_transfer( FINCAD_ROOT, ftp, target_dir, release_folder_name )
  # to specify different target dir on ftp server change '' to 'new_dir'
  release_common.transfer_build_artifacts( FINCAD_ROOT, ftp, target_dir, release_folder_name, { tgz_folder : '' } )

  ftp_common.ftp_quit( ftp )

def create_tgz( tgz_folder, bld_prod_dirs, FINCAD_ROOT ):
  if os.path.exists( tgz_folder ):
    release_common.safe_rmdir( tgz_folder )

  release_common.safe_mkdir( tgz_folder )

  tgz_file = os.path.join( tgz_folder, str( release_common.build_generic_tgz_name( FINCAD_ROOT ) ) )
  print "Creating " + tgz_file
  tgz = tarfile.open( tgz_file, "w:gz" )

  for bld_prod_dir in bld_prod_dirs:
    if os.path.exists( bld_prod_dir ):
      os.chdir( os.path.dirname( bld_prod_dir ) )
      tgz.add( os.path.basename( bld_prod_dir ), bld_prod_dirs[ bld_prod_dir ] )
  tgz.close()

if __name__ == '__main__':
  if len( sys.argv ) > 0 and len( sys.argv ) < 4:
    ftp_transfer( *sys.argv[1:] )
  else:
    print "Usage: python 100generic_transfer.py {server} {target_dir}"
