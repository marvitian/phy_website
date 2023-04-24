#!/usr/bin/python
import sqlite3
import csv
import re
import os
import time
import sys

##################################################################
#####        CREATE TABLE WITH LIST OF KEYS AS PARAMS        #####
##################################################################
def generate_table(new_table_name, keys):
	keys_string = ''
	key_names = ''
	count = 0
	for key in keys:
		key_names += key + ', '
		if count > 0 and key == 'MajorSystemMode':
			count+=1
			break
		if key == 'Baud_Rate':
			keys_string += key + ' INT, '
		else:
			keys_string+=key+' TEXT, '
	print 'Generating New Table: "%s"' % new_table_name
	db.execute('CREATE TABLE IF NOT EXISTS %s(Path TEXT, %s, UNIQUE(%s));' % (new_table_name, keys_string[:-2], key_names[:-2]))

##################################################################
#####     GET THE LIST OF KEYS AND VALUES FROM LOCAL LOG     #####
##################################################################
def get_keys(filename):
	global keys
	global values
	global labels
	keys=[]
	values=[]
	labels=[]
	with open(filename, 'r') as f:
		for line in f:
			if '[DPI_SV] [KEY=VALUE, LABEL]:' in line:
				split=line.split('[DPI_SV] [KEY=VALUE, LABEL]: --- ',1)
				line=re.sub(' ','',split[1])
				line1 = line
				line=line.split('=',1)
				key=line[0].split('_ch',1)
				try:
					value_label=line[1].split(',',1)
				except:
					next_line = f.next()[:-1]
					next_line += f.next()[:-1]
					line1 = line1[:-1] + next_line
					line1 = re.sub(' ', '', line1)
					line1=line1.split('=', 1)
					key=line1[0].split('_ch', 1)
					value_label = line1[1].split(',', 1)
				
				if keys.count(key[0]) == 0 or key[0] == keys[0] or keys.count(key[0]) < keys.count(keys[0]):
					keys.append(key[0])
					values.append(re.sub('[^0-9]','',value_label[0]))
					labels.append(re.sub('[ \n]','',value_label[1]))
				else:
					index = keys.index(key[0], 0)
					values[index] = re.sub('[^0-9]','',value_label[0])


##################################################################
#####      ADD VALUES FOR THE KEYS TO THE TABLE OF KEYS      #####
##################################################################
def insert_entry(table_name, values, keys, path):
	values_string=''
	keys_string=''
	table = db.execute('SELECT * FROM %s;' % (table_name))
	key_names= list(map(lambda x: x[0], table.description))
	for new_key in list(set(keys) - set(key_names)):
		db.execute('ALTER TABLE %s ADD COLUMN %s TEXT;' % (table_name, new_key))
		db.execute('UPDATE %s SET %s = "FUNCTIONAL_TEST" WHERE Path = "LABELS"' % (table_name, new_key))
	for i in range(len(values)):
		values_string+='"'+values[i]+'", '
		keys_string+=keys[i]+', '
		
	db.execute('INSERT OR IGNORE INTO %s (Path, %s) VALUES("%s", %s);' % (table_name, keys_string[:-2], path, values_string[:-2]))

##################################################################
#####      PRINT VALUES FROM A SPECIFIED TABLE TO A CSV      #####
##################################################################
def print_table(table_name):
	location = 'tables/' + table_name + '.csv'
	f = open(location, 'w')
	writer = csv.writer(f)
	table = db.execute('SELECT * FROM %s;' % (table_name))
	key_names= list(map(lambda x: x[0], table.description))
	writer.writerow(key_names)	
	for row in table:
		writer.writerow(row)
	f.close()


##################################################################
#####        CONVERT DFI PERIOD TO CK SPEED FOR TABLE        #####
##################################################################
def dfiperiod_to_ckspeed(dfiperiod, dfi2ckratio, MajorSystemMode):
	if MajorSystemMode == '4':
		rate = 4 - (int(dfi2ckratio) * 2)
		speed_to_ck = 2
	else:
		rate = 1
		speed_to_ck = 8
	ck_period = int(dfiperiod) / rate
	ck_freq = int(1000000 / ck_period)
	ck_speed = ck_freq * speed_to_ck

	return str(ck_speed)

##################################################################
#####      Main part of code, Runs the above functions       #####
##################################################################
def read_write(rootdir):
	try:
		config = re.search('CONFIG@r(.+?)_', rootdir).group(1)
		table_name = 'CONFIG_'+config
	except AttributeError:
		print 'Pattern CONFIG@r####_ not found in directory name: %s' % rootdir
		sys.exit()
	try:
		phy = re.search('CFG(.+?)_', rootdir).group(1)
	except AttributeError:
		print 'Pattern CFG_#_ not found in directory name: %s' % rootdir
		sys.exit()
	phy = re.sub('[^0-9]','',phy)

	print 'Scanning New Regression : "' + table_name+ '"'
	print 'Path : ' + rootdir
	#db.execute("DROP TABLE if exists %s;" % (table_name))

	# cursor=db.cursor()

	# cursor.execute('SELECT name FROM sqlite_master WHERE type = "table";')
	# tables = cursor.fetchall()
	# for i in range (0, len(tables)):
	# 	tables[i] = tables[i][0]
	

	extra_keys = ['Phy_Cfg', 'Baud_Rate']
	extra_labels = ['exta', 'extra']
	extra_vals = [phy]

	count = 0
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			if file == 'local_log.log':
				path = os.path.join(rootdir, subdir, file)
				get_keys(path)
		
				if len(keys) == 0:
					break


				if keys.count('MajorSystemMode') == 0:
					if count==0:
						count-=1

				elif keys.count('MajorSystemMode') == 1:
					dfi_index = keys.index('dfiperiod', 0)
					dfi2ck_index = keys.index('dfi2ckratio', 0)
					MajorSystemMode_index = keys.index('MajorSystemMode',0)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					keys[0:0] = extra_keys
					values[0:0] = extra_vals
					labels[0:0] = extra_labels
					extra_vals.pop()

					if count == 0 and table_name not in tables:
						generate_table(table_name, keys, phy)
						insert_entry(table_name, labels, keys, 'LABELS')
					insert_entry(table_name, values, keys, path)

				elif keys.count('MajorSystemMode') == 2:
					dfi_index = keys.index('dfiperiod', 0)
					dfi2ck_index = keys.index('dfi2ckratio', 0)
					MajorSystemMode_index = keys.index('MajorSystemMode', 0)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					keys[0:0] = extra_keys
					values[0:0] = extra_vals
					labels[0:0] = extra_labels
					extra_vals.pop()

					dfi_index = keys.index('dfiperiod', dfi_index + len(extra_keys) + 1)
					dfi2ck_index = keys.index('dfi2ckratio', dfi2ck_index + len(extra_keys) + 1)
					MajorSystemMode_index = keys.index('MajorSystemMode', MajorSystemMode_index + len(extra_keys) + 1)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					index = keys.index('MajorSystemMode', len(extra_keys) + 1)
					keys[index:index] = extra_keys
					values[index:index] = extra_vals
					labels[index:index] = extra_labels
					extra_vals.pop()

					if count == 0 and table_name not in tables:
						generate_table(table_name, keys[:index])
						insert_entry(table_name, labels[:index], keys[:index], 'LABELS')
					insert_entry(table_name, values[:index], keys[:index], path)
					insert_entry(table_name, values[index:], keys[index:], path)
				
				elif keys.count('MajorSystemMode') == 3:
					dfi_index = keys.index('dfiperiod', 0)
					dfi2ck_index = keys.index('dfi2ckratio', 0)
					MajorSystemMode_index = keys.index('MajorSystemMode', 0)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					keys[0:0] = extra_keys
					values[0:0] = extra_vals
					labels[0:0] = extra_labels
					extra_vals.pop()
					
					dfi_index = keys.index('dfiperiod', dfi_index+len(extra_keys) + 1)
					dfi2ck_index = keys.index('dfi2ckratio', dfi2ck_index + len(extra_keys) + 1)
					MajorSystemMode_index = keys.index('MajorSystemMode', MajorSystemMode_index + len(extra_keys) + 1)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					index1 = keys.index('MajorSystemMode', len(extra_keys) + 1)
					keys[index1:index1] = extra_keys
					values[index1:index1] = extra_vals
					labels[index1:index1] = extra_labels
					extra_vals.pop()
					
					dfi_index = keys.index('dfiperiod', dfi_index+len(extra_keys) + 1)
					dfi2ck_index = keys.index('dfi2ckratio', dfi2ck_index + len(extra_keys) + 1)
					MajorSystemMode_index = keys.index('MajorSystemMode', MajorSystemMode_index + len(extra_keys) + 1)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					index2 = keys.index('MajorSystemMode', index1 + len(extra_keys) + 1)
					keys[index2:index2] = extra_keys
					values[index2:index2] = extra_vals
					labels[index2:index2] = extra_labels
					extra_vals.pop()

					if count == 0 and table_name not in tables:
						generate_table(table_name, keys[:index1], phy)
						insert_entry(table_name, labels[:index1], keys[:index1], 'LABELS')
					insert_entry(table_name, values[:index1], keys[:index1], path)
					insert_entry(table_name, values[index1:index2], keys[index1:index2], path)
					insert_entry(table_name, values[index2:], keys[index2:], path)
				
				elif keys.count('MajorSystemMode') == 4:
					dfi_index = keys.index('dfiperiod', 0)
					dfi2ck_index = keys.index('dfi2ckratio', 0)
					MajorSystemMode_index = keys.index('MajorSystemMode', 0)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					keys[0:0] = extra_keys
					values[0:0] = extra_vals
					labels[0:0] = extra_labels
					extra_vals.pop()
					
					dfi_index = keys.index('dfiperiod', dfi_index+len(extra_keys) + 1)
					dfi2ck_index = keys.index('dfi2ckratio', dfi2ck_index + len(extra_keys) + 1)
					MajorSystemMode_index = keys.index('MajorSystemMode', MajorSystemMode_index + len(extra_keys) + 1)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					index1 = keys.index('MajorSystemMode', len(extra_keys) + 1)
					keys[index1:index1] = extra_keys
					values[index1:index1] = extra_vals
					labels[index1:index1] = extra_labels
					extra_vals.pop()
					
					dfi_index = keys.index('dfiperiod', dfi_index+len(extra_keys) + 1)
					dfi2ck_index = keys.index('dfi2ckratio', dfi2ck_index + len(extra_keys) + 1)
					MajorSystemMode_index = keys.index('MajorSystemMode', MajorSystemMode_index + len(extra_keys) + 1)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					index2 = keys.index('MajorSystemMode', index1 + len(extra_keys) + 1)
					keys[index2:index2] = extra_keys
					values[index2:index2] = extra_vals
					labels[index2:index2] = extra_labels
					extra_vals.pop()

					dfi_index = keys.index('dfiperiod', dfi_index + len(extra_keys) + 1)
					dfi2ck_index = keys.index('dfi2ckratio', dfi2ck_index + len(extra_keys) + 1)
					MajorSystemMode_index = keys.index('MajorSystemMode', MajorSystemMode_index + len(extra_keys) + 1)
					extra_vals.append(dfiperiod_to_ckspeed(values[dfi_index], values[dfi2ck_index], values[MajorSystemMode_index]))
					index3 = keys.index('MajorSystemMode', index2 + len(extra_keys) + 1)
					keys[index3:index3] = extra_keys
					values[index3:index3] = extra_vals
					labels[index3:index3] = extra_labels
					extra_vals.pop()

					if count == 0 and table_name not in tables:
						generate_table(table_name, keys[:index1], phy)
						insert_entry(table_name, labels[:index1], keys[:index1], 'LABELS')
					insert_entry(table_name, values[:index1], keys[:index1], path)
					insert_entry(table_name, values[index1:index2], keys[index1:index2], path)
					insert_entry(table_name, values[index2:index3], keys[index2:index3], path)
					insert_entry(table_name, values[index3:], keys[index3:], path)

				else:
					print
					print "More than 4 iterations of the keys is not allowed (2 fsp and 2 channel), %s were found" % keys.count('MajorSystemMode')
					print "Ignoring file: %s\n" %path
				count += 1
    
            input('continue')
	
	# cursor.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name="%s";' % table_name)
	# if cursor.fetchone()[0]==1:
	# 	print_table(table_name)
	# else:
	# 	print "%s has no keys. Table will be removed" % table_name



def main():
	global db
	db = sqlite3.connect('csrStructKeys.db')
	cursor = db.cursor()

	db.execute('CREATE TABLE IF NOT EXISTS CONFIG_MASTER (Directory TEXT NOT NULL);')
	for dirname in os.listdir('~/regressdb'):
		dirname = '~/regressdb/' + dirname
		
		c_time = os.path.getctime(dirname)

		config = re.search('CONFIG@r(.+?)_', dirname)
		phy_cfg = re.search('CFG(.+?)_', dirname)
		if config and phy_cfg and c_time > 1656637200:
			config=config.group(1)
			table_name = 'CONFIG_'+config
			
			cursor.execute('SELECT Directory FROM CONFIG_MASTER;')
			directories = cursor.fetchall()

			if not any(dirname in directory for directory in directories):
				read_write(dirname)
				db.execute('INSERT INTO CONFIG_MASTER (Directory) VALUES("%s");' % dirname)
	cursor.close()
	db.commit()
	# commit log, number of entries, number of new paths, runtime, 
	db.close()

	# Sanity Check
	# old values
	# new values
	# values that don't exist

	

if __name__ == '__main__':
	main()

