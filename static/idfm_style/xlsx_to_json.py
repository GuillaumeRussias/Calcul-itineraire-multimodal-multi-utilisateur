import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import pandas

file = pandas.read_excel(currentdir+"/table_connection.xlsx").set_index('route_name').transpose()
new_file = open(currentdir+"/table_connection.js","w")
new_file.write("var icons_table = ")
file.to_json(new_file)
new_file.close()
