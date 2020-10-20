import mysql.connector
import pymysql
from mysql.connector import Error

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="erika"
)


def alldata():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT id_tumbuhan, CONCAT("
                     " penggunaan,' ',pemerian) AS data "
                     "FROM tanaman LIMIT 200")

    myresult = mycursor.fetchall()

    return myresult


def alldataNama():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT id_tumbuhan, CONCAT("
                     "nama,' ',nama_latin,' ',nama_daerah,' ',keluarga) AS data "
                     "FROM tanaman")

    myresult = mycursor.fetchall()

    return myresult


def alldataZat():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT id_tumbuhan, CONCAT(zat_berkhasit) AS data FROM tanaman")

    myresult = mycursor.fetchall()

    return myresult


def byid(id):
    try:
        format_strings = ','.join(['%s'] * len(id))
        mycursor = mydb.cursor(dictionary=True)
        data = str(tuple(id)).replace("(", "").replace(")", "")
        mycursor.execute(
            "SELECT tanaman.*  FROM tanaman WHERE id_tumbuhan IN (%s) ORDER BY field(id_tumbuhan,{})".format(
                data) % format_strings,
            (tuple(id)))
        myresult = mycursor.fetchall()
        return myresult
    except Error as e:
        return False
