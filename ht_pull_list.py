import codecs
import csv
import os
import pymssql

#========================================================================================================================
# Hashtag Pull List
# -----------------
# From the provided SQL, pulls the relevant data, converts it and constructs the HTML for the new Hashtag Word Cloud.
#========================================================================================================================

# Get CSV Function (from tools)
def get_csv(host,user,password,database,script):
  # Set working directory and alias
  dir = '/'.join(script.split('/')[:-1]) + '/'
  alias = script.split('/')[-1].split('.')[0]

  # Set connection parameters
  h = host
  u = user
  p = password
  d = database
  s = script

  # Connect to database
  conn = pymssql.connect(host=h,user=u,password=p,database=d)
  cur = conn.cursor()

  # Get script, run it
  file = open(s)
  sql = file.read()
  file.close()
  cur.execute(sql)

  # Write results to file
  encoding = 'ascii'
  out = codecs.open(dir + alias + '.csv','w',encoding)
  writer = csv.writer(out, delimiter=',')
  # writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL)

  line = [col.encode(encoding,'ignore').replace(',','').strip() if type(col) is unicode else str(col[0]).replace(',','').strip() for col in cur.description]
  writer.writerow(line)
  row = cur.fetchone()

  while row:
    line = [col.encode(encoding,'ignore') if type(col) is unicode else str(col) for col in row]
    writer.writerow(line)
    row = cur.fetchone()

  out.close()
  conn.close()

#========================================================================================================================
# M A I N
#========================================================================================================================

# Temp variables
ht_list_format = ''
i = 0

# Pull the Hashtag Data
get_csv('172.24.16.100:49207','kchiou','Ksje*#e74ksv','ReportingDB','sql/ht_pull.sql')

# Open the Pulled Hashtag Data
with open('sql/ht_pull.csv') as h:
	ht_list = [x.strip('\r\n') for x in h.readlines()]

# Construct the Pulled Hashtag Data in the correct format
for ht in ht_list:
	i = i + 1

	# Don't include the header
	if i != 1:
		ht_name = ht.strip('"').strip(",").split(",")[0]
		ht_val = ht.split(",")[1]

		# Construct in the format
		# Format: {'text': 'China', 'size': 112.35505232387254}
		ht_obj = "{'text': '" + ht_name + "', 'size': " + ht_val + "}"

		# Put together the list of hashtag elements that will be displayed
		ht_list_format = ht_list_format + ht_obj + ","

# Use the template HTML and populate the correct data
with open('ht_wordcloud.html', 'w') as html_towrite:
	with open('html/template_index.html', 'r') as htmltemplate:
		for line in htmltemplate:
			if "###ht_pull###" in line:
				html_towrite.write("words: [")
				html_towrite.write(ht_list_format[:-1])
				html_towrite.write("] })")
			else:
				html_towrite.write(line)


