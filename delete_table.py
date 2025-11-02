import psycopg2


try:
    connection = psycopg2.connect(
        dbname= "autobuddy_elderly_database",
        user= "elderly_admin",
        password= "elderlyAB#1234",
        host= "autobuddy-elderly.cxs26o04s5t8.ap-south-1.rds.amazonaws.com",
        port= 5432,
    )

    cursor = connection.cursor()
    cursor.execute("alter table elder_patientrelative add column modelnumber varchar(255)")
    connection.commit()
    print("Done")
    cursor = connection.cursor()
    cursor.execute("select * from elder_userprofile")
    a = cursor.fetchall()
    b = cursor.description
    print("Done", a)
    print("Done", b)

except psycopg2.OperationalError as e:
    print("Error", e)