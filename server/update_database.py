import sqlite3

# Course description database information
cd_db = 'course_descriptions.db'
cd_table = 'descriptions'
cd_id_column = 'CourseID'

# Course database which was scraped from Stevens.edu
update_db = 'courses2.db'
update_table = 'courses'
update_call_number = 'CallNumber'
update_semester = '2018 Spring'

# Django database which needs to be updated
out_db = 'db.sqlite3'
out_table = 'SAServer_course'
out_id_column = 'course_id'
out_call_number = 'call_number'
out_semester = 'semester'
out_description_column = 'course_description'

# Connect the databases
update_conn = sqlite3.connect(update_db)
update_cursor = update_conn.cursor()

out_conn = sqlite3.connect(out_db)
out_cursor = out_conn.cursor()

# Pull all of the Stevens.edu from its database
update_cursor.execute('SELECT * FROM {tn}'.format(tn=update_table))
all_rows = update_cursor.fetchall()

# Itereate through all of the new courses, if it is not already in the database add it, else update the record
for row in all_rows:
    course_call_number = row[3]
    course_semester = '2018 Spring'
    #print(course_call_number)
    out_cursor.execute('SELECT * FROM SAServer_course WHERE call_number = ? AND semester = ?',(course_call_number,course_semester))
    call_number_row = out_cursor.fetchall()
    if len(call_number_row) > 0:
        out_cursor.execute('UPDATE SAServer_course SET course_id = ?, course_name = ?, course_section = ?, status = ?, seats = ?, day = ?, time = ?, campus = ?, location = ?, instructor = ?, start_date = ?, end_date = ?, min_credit = ?, max_credit = ? WHERE call_number = ? AND semester = ?', (row[0],row[1],row[2],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[3],update_semester))
        out_conn.commit()
    else:
        out_cursor.execute('INSERT into SAServer_course (course_id,course_name,course_section,course_description,call_number,status,seats,day,time,campus,location,instructor,semester,start_date,end_date,min_credit,max_credit) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (row[0],row[1],row[2],'','2018S'+row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],update_semester,row[11],row[12],row[13],row[14]))
        out_conn.commit()

update_cursor.close()

# Now update all of the course descriptions
cd_conn = sqlite3.connect(cd_db)
cd_cursor = cd_conn.cursor()

# Grab all of the course descriptions
cd_cursor.execute('SELECT * FROM '+cd_table)
all_rows = cd_cursor.fetchall()

# Update all courses with their course description
for row in all_rows:
    course_id = ''.join(row[0].split())
    course_description = row[1]
    out_cursor.execute('UPDATE SAServer_course SET course_description = ? WHERE course_id = ?',(course_description,course_id))
    out_conn.commit()

out_cursor.close()
cd_cursor.close()

