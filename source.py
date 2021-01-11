import mysql.connector
import pymysql
from mysql.connector import Error


def alldata():
    mydb = mysql.connector.connect(
        host="45.80.181.198",
        user="root",
        password="kmzway87saa",
        database="erika"
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT id_tumbuhan, CONCAT("
                     " penggunaan,' ',pemerian) AS data "
                     "FROM tanaman")

    myresult = mycursor.fetchall()

    return myresult


def all():
    mydb = mysql.connector.connect(
        host="45.80.181.198",
        user="root",
        password="kmzway87saa",
        database="erika"
    )
    mycursor = mydb.cursor(dictionary=True)

    mycursor.execute("SELECT * FROM tanaman ORDER BY nama ASC")

    myresult = mycursor.fetchall()

    return myresult


def persamaan(var):
    mydb = mysql.connector.connect(
        host="45.80.181.198",
        user="root",
        password="kmzway87saa",
        database="erika"
    )
    mycursor = mydb.cursor()
    format_strings = ','.join(['%s'] * len(var))
    mycursor.execute(
        "SELECT persamaan FROM persamaan WHERE nama_penyakit IN (%s) " % format_strings , tuple(var))

    myresult = mycursor.fetchall()

    return myresult


def alldataZat():
    mydb = mysql.connector.connect(
        host="45.80.181.198",
        user="root",
        password="kmzway87saa",
        database="erika"
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT id_tumbuhan, CONCAT(zat_berkhasit) AS data FROM tanaman")

    myresult = mycursor.fetchall()

    return myresult


def byid(id):
    try:
        mydb = mysql.connector.connect(
            host="45.80.181.198",
            user="root",
            password="kmzway87saa",
            database="erika"
        )
        format_strings = ','.join(['%s'] * len(id))
        mycursor = mydb.cursor(dictionary=True)
        if len(id) == 1:
            mycursor.execute(
                "SELECT tanaman.*  FROM tanaman WHERE id_tumbuhan = %s", tuple(id))
        else:
            data = str(tuple(id)).replace("(", "").replace(")", "")
            mycursor.execute(
                "SELECT tanaman.*  FROM tanaman WHERE id_tumbuhan IN (%s) ORDER BY field(id_tumbuhan,{})".format(
                    data) % format_strings,
                (tuple(id)))
        myresult = mycursor.fetchall()
        return myresult
    except Error as e:
        return False
