import mysql.connector
from mysql.connector import Error

try:
    # Verbindungsaufbau zur Datenbank
    connection = mysql.connector.connect(
        host='localhost',        # z.B. 'localhost' oder die IP-Adresse des Servers
        user='root', # Dein Benutzername
        password='', # Dein Passwort
        database='passwordmanager' # Der Name der Datenbank, zu der du dich verbinden möchtest
    )

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Erfolgreich verbunden mit MySQL Server Version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("SELECT * from passwords;")
        record = cursor.fetchone()
        print("Verbunden mit der Datenbank: ", record)

except Error as e:
    print("Fehler beim Verbinden mit MySQL", e)