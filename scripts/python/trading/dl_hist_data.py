# Req: Python > 3
import os, sys, time, urllib.request

def main():
  stockSyms = { 	"DJI" : "%5EDJI", \
                        "VIX" : "%5EVIX", \
			"INX" : "%5EGSPC", \
			"COMP" : "%5EIXIC", \
                         # Automotive
			"F" : "F", \
			# Battaries
			"ABAT" : "ABAT", \
			"AONE" : "AONE", \
			"CBAK" : "CBAK", \
			# Energy
			"CHK" : "CHK", \
			"CPN" : "CPN", \
			"KWK" : "KWK", \
			"UNG" : "UNG", \
			# Financial
			"C" : "C", \
			"FNM" : "FNM", \
			"FRE" : "FRE", \
			# Health Care
			"ACAD" : "ACAD", \
			"AET" : "AET", \
			"AUXL" : "AUXL", \
			"MYGN" : "MYGN", \
			"OSIR" : "OSIR", \
			"PFE" : "PFE", \
			"SQNM" : "SQNM", \
			#Tech: Network
			"ADCT" : "ADCT", \
			"ALVR" : "ALVR", \
			"BRCM" : "BRCM", \
			"CIEN" : "CIEN", \
			"CLWR" : "CLWR", \
			"CSCO" : "CSCO", \
			#Tech: Semiconductor
			"EMC" : "EMC", \
			"MU" : "MU", \
			"RMBS" : "RMBS", \
			"SMTL" : "SMTL", \
			"SNDK" : "SNDK", \
			"STEC" : "STEC", \
                        "STX" : "STX", \
			"TQNT" : "TQNT", \
			#Tech: Software
                        "CMCSA" : "CMCSA", \
                        "GE" : "GE", \
                        "IACI" : "IACI", \
			"INTC" : "INTC", \
                        "MSFT" : "MSFT", \
                        "VMW" : "VMW", \
			# Potential
			"JACK" : "JACK", \
			"HTZ" : "HTZ", \
			}

  tgtFolder = "C:\\Trading"
  startDay, startMonth, startYear = getStartDate()
  endDay, endMonth, endYear = getEndDate()

  for stockSym in stockSyms:
    url = buildURL( stockSyms[ stockSym ], startDay, startMonth, startYear, endDay, endMonth, endYear )
    download( url, os.path.join( tgtFolder, stockSym + ".csv" ) )

def getStartDate():
  # Start date set to beginning for 2007
  startDay = "01"
  startMonth = "01"
  startYear = "2007"

  return startDay, startMonth, startYear

def getEndDate():
  # End date set to today
  endDay = time.strftime( "%d" )
  endMonth = time.strftime( "%m" )
  endYear = time.strftime( "%Y" )

  return endDay, endMonth, endYear

def buildURL( stockSym, startDay, startMonth, startYear, endDay, endMonth, endYear ):
  url = "http://ca.rd.yahoo.com/finance/quotes/internal/historical/download/*http://ichart.finance.yahoo.com/table.csv?" \
  + "s=" + stockSym \
  + "&a=" + startDay \
  + "&b=" + startMonth \
  + "&c=" + startYear \
  + "&d=" + endDay \
  + "&e=" + endMonth \
  + "&f=" + endYear \
  + "&g=d&ignore.csv"

  return url

def download( url, filename ):
  print( "Downloading " + filename )
  webFile = urllib.request.urlopen( url )
  parsedContent = parseWebFile( webFile )
  localFile = open( filename, 'w' )
  for line in parsedContent:
    if line == parsedContent[ -1 ]:
      localFile.write( line )
    else:
      localFile.write( line + "\n" )
  webFile.close()
  localFile.close()

def parseWebFile( webFile ):
  lines = []
  for line in webFile.readlines():
    lines.append( str( line ).split( "'" )[1].split( "\\")[0] )
  lines.sort()
  lines.pop() # removing header which is the last item
  return lines

if __name__ == '__main__':
  if len( sys.argv ) == 1:
    main()
  else:
    print( "Usage: python dl_hist_data.py" )