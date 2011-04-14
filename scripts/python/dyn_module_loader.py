import imp

def cfg_loader( name, path ):
  file, pathname, description = imp.find_module( name, [ path ] )
  try:
    module = imp.load_module( name, file, pathname, description )
  finally:
    if file:
      file.close()
  return module
