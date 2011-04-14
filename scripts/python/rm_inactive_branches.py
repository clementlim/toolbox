import os, sys, re, urllib2

def rm_inactive_branches( target_dir ):
  if not os.path.exists( target_dir ):
    print target_dir + " does not exists!"
    sys.exit(1)

  # json_filename: json_object_tag
  json_files = {'active_branches.json': '{"activebranches": {',
                'active_releases.json': '{"activereleases": {',
                'active_nightly.json': '{"activenightly": {',
                'active_licencing.json': '{"activelicencing": {'}
  json_base_url = "http://buildbot.financialcad.com/~buildbot/"

  active_branches=[ 'info', 'trunk' ]
  for json_file in json_files:
    active_branches = get_active_branches( json_base_url + json_file, json_files[ json_file ], active_branches )

  target_dirs=[]
  target_items = os.listdir( target_dir )
  for target_item in target_items:
    if os.path.isdir( os.path.join( target_dir, target_item ) ):
      target_dirs.append( target_item )

  dirs_to_be_deleted=[]
  for dir in target_dirs:
    found = 0
    for branch in active_branches:
      if  re.search( branch + '$', dir ):
        found = 1
        break
    if found != 1:
      dirs_to_be_deleted.append( dir )

  print "Directories to be deleted:"
  for dir in dirs_to_be_deleted:
    print dir
  print "=================================================================================="
  for dir in dirs_to_be_deleted:
    print "Deleting " + dir
    os.system( 'python delete.py ' + os.path.join( target_dir, dir ) )
  print "=================================================================================="
  print "Done."

def get_active_branches( json_path, json_object_tag, active_branches ):
  active_branches_raw = urllib2.urlopen( json_path ).read()

  if re.search( json_object_tag , active_branches_raw ):
    active_branches_raw = active_branches_raw[ len( json_object_tag ) : -3 ].split( ',' )

  # no active branches, return
  if active_branches_raw[0] == '':
    return active_branches

  for active_branch in active_branches_raw:
    [branch,_] = active_branch.split(':')
    sanitized_branch = branch.strip()[1:-1]
    if not sanitized_branch in active_branches:
      active_branches.append(sanitized_branch)

  return active_branches

if __name__ == '__main__':
  if len( sys.argv ) == 2:
    rm_inactive_branches( sys.argv[1] )
  else:
    print "Usage: python rm_inactive_branches.py <target_dir>"
