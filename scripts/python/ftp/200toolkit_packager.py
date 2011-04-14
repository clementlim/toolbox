import os, sys, shutil, tarfile
import ftp_config
from ftplib import FTP
from ftp_common import FTPCommon
from release_common import ReleaseCommon

ftp_common = FTPCommon()
release_common = ReleaseCommon()

def ftp_transfer( server = ftp_config.ftp_server, target_dir = ftp_config.ftp_target_dir ):
  FINCAD_ROOT = os.getcwd()
  release_folder_name = 'r' + release_common.get_revision( FINCAD_ROOT )

  uploader_username = 'uploader'
  uploader_password = 'P0s1t1ve'
  tgz_src_dir = release_common.get_tgz_dir( FINCAD_ROOT )
  packager_dir = os.path.join( os.path.dirname( tgz_src_dir ), 'packager' )
  packager_src_dir = os.path.join( packager_dir, 'src_unpack' )
  packager_tgz_dir = os.path.join( packager_dir, 'tgz' )

  # set up directories to working in
  if os.path.exists( packager_dir ):
    release_common.safe_rmdir( packager_dir )

  release_common.safe_mkdir( packager_src_dir )
  release_common.safe_mkdir( packager_tgz_dir )

  # extract files from generic tgz file
  tgz_src_file = release_common.build_generic_tgz_name( FINCAD_ROOT )
  
  if tgz_src_file in os.listdir( tgz_src_dir ):
    tgz = tarfile.open( os.path.join( tgz_src_dir, tgz_src_file ), "r:gz" )
    tgz_members = tgz.getmembers()
    for tgz_member in tgz_members:
      tgz.extract( tgz_member, packager_src_dir )

  # package necessary files
  bld_prod_dirs = { os.path.join( packager_src_dir, 'build_stage', release_common.get_build_type(), release_common.get_bit_count(), 'py' ) : os.path.join( 'bin', release_common.get_build_type(), release_common.get_bit_count() ), 
                    os.path.join( packager_src_dir, 'build_stage', release_common.get_build_type(), release_common.get_bit_count(), 'lib' ) : os.path.join( 'bin', release_common.get_build_type(), release_common.get_bit_count() ), 
                    os.path.join( packager_src_dir, 'build_stage', release_common.get_build_type(), release_common.get_bit_count(), 'lib', 'unprotected' ) : os.path.join( 'bin', release_common.get_build_type(), release_common.get_bit_count(), 'unprotected' ),
                    os.path.join( packager_src_dir, 'include' ) : os.path.join( 'include' ),
                    os.path.join( packager_src_dir, 'doc_stage', 'mathref', 'html' ) : os.path.join( 'docs', 'math', 'html' ),
                    os.path.join( packager_src_dir, 'doc_stage', 'mathref', 'txt' ) : os.path.join( 'docs', 'math', 'txt' ) }
  
  create_tgz( packager_tgz_dir, bld_prod_dirs, FINCAD_ROOT )

  ftp = ftp_common.ftp_connect( server, uploader_username, uploader_password )
  release_common.setup_dir_for_transfer( FINCAD_ROOT, ftp, target_dir, release_folder_name )
  release_common.transfer_build_artifacts( FINCAD_ROOT, ftp, target_dir, release_folder_name, { packager_tgz_dir : '' } )
  ftp_common.ftp_quit( ftp )

def create_tgz( tgz_folder, bld_prod_dirs, FINCAD_ROOT ):
  if os.path.exists( tgz_folder ):
    release_common.safe_rmdir( tgz_folder )

  release_common.safe_mkdir( tgz_folder )

  tgz_file = os.path.join( tgz_folder, str( release_common.build_tgz_name( FINCAD_ROOT ) ) )
  print "Creating " + tgz_file
  tgz = tarfile.open( tgz_file, "w:gz" )

  for bld_prod_dir in bld_prod_dirs:
    if os.path.exists( bld_prod_dir ):
      os.chdir( os.path.dirname( bld_prod_dir ) )
      if bld_prod_dir == os.path.join( FINCAD_ROOT, 'build', 'stage', 'lib' ):
        libs = [ file for file in os.listdir( bld_prod_dir ) if os.path.splitext( file )[-1] == '.lib' ]
        bins = [ file for file in os.listdir( bld_prod_dir ) if file not in libs and file != 'dsfincad_client.dll' ]
        if 'unprotected' in bins:
          bins.remove( 'unprotected' )
        for lib in libs:
          tgz.add( os.path.join( os.path.basename( bld_prod_dir ), lib ), os.path.join( 'lib', get_build_type(), get_bit_count(), lib ) )
        for bin in bins:
          tgz.add( os.path.join( os.path.basename( bld_prod_dir ), bin ), os.path.join( bld_prod_dirs[ bld_prod_dir ], bin ) )
      elif bld_prod_dir == os.path.join( FINCAD_ROOT, 'src', 'iflayer', 'fcf3', 'include', 'public', 'fcf3' ):
        tgz.add( os.path.join( os.path.basename( bld_prod_dir ), 'callf3function.hpp' ), os.path.join( bld_prod_dirs[ bld_prod_dir ], 'callf3function.hpp' ) )
      else:
        tgz.add( os.path.basename( bld_prod_dir ), bld_prod_dirs[ bld_prod_dir ] )

  tgz.close()

if __name__ == '__main__':
  if len( sys.argv ) == 1:
    ftp_transfer()
  elif len( sys.argv ) == 2:
    ftp_transfer( sys.argv[1] )
  elif len( sys.argv ) == 3:
    ftp_transfer( sys.argv[1], sys.argv[2] )
  else:
    print "Usage: python XXX<client>_packager.py {server} {target_dir}"
