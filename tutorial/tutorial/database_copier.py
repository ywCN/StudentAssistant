import sqlite3

from_file = 'courses.db'

to_file = 'course_descriptions.db'

from_table = 'courses'

to_table = 'quickstart_course'
call_number = "call_number"
credits = "credits"
days_times = "days_times"
instructor = "instructor"
section_title = "section_title"
session_dates = "session_dates"
status_seats = "status_seats"
course_id = "course_id"

# Connecting to the database file
conn_from = sqlite3.connect(from_file)
cursor_from = conn_from.cursor()

# Every row from entire table
cursor_from.execute('SELECT * FROM {table_name}'.\
	format(table_name=from_table))
all_rows = cursor_from.fetchall()
conn_from.close()

conn_to = sqlite3.connect(to_file)
cursor_to = conn_to.cursor()

for row in all_rows:
	sql = 'INSERT INTO {table_name} ({st}, {cn}, {ss}, {dt}, {ins}, {sd}, {cr}, {ci}) VALUES '.format(table_name=to_table, cn=call_number, cr=credits, dt=days_times, ins=instructor, st=section_title, sd=session_dates, ss=status_seats, ci=course_id)
	sql = sql+"("
	section_splits = row[0].split('-')
	course_id_concat = section_splits[0].strip()+section_splits[1].strip()
	#print course_id
	for item in row:
		sql = sql+"\""+(item.encode('ascii','ignore').strip()+"\",")
	#sql = sql[:-1]
	sql = sql +"\""+course_id_concat+"\""
	sql = sql+")"
	print sql
	cursor_to.execute(sql)

conn_to.commit()
conn_to.close()
	

