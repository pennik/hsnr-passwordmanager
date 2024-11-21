import math 
import mysql.connector
from mysql.connector import Error

try:
    # Verbindungsaufbau zur Datenbank
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='passwordmanager'
    )

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Erfolgreich verbunden mit MySQL Server Version ", db_Info)

except Error as e:
    print("Fehler beim Verbinden mit MySQL", e)

def Login(username, password):
    try:
        query = "SELECT User_ID FROM `users` WHERE LoginName = %s AND MasterPassword = %s"
        cursor = connection.cursor()  # Neuer Cursor
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()  # Schließe den Cursor nach Gebrauch
        return result
    except Error as e:
        print("Fehler beim Ausführen der Login-Abfrage:", e)
        return False


def Menu():
    print("Was möchtest du machen?")
    print("1. Passwordabfragen \n2. Password Hinzufügen \n3. Password Generieren")
    usecase = int(input())
    match usecase:
        case 1:
            print("Liste der passwörter")
            query = """
            SELECT Passwords.Name, Passwords.password, Users.User_ID 
            FROM Passwords 
            INNER JOIN Users ON Passwords.User_ID = Users.User_ID 
            WHERE Users.User_ID = %s
            """
            cursor = connection.cursor()
            cursor.execute(query, (UserID))
            result = cursor.fetchall()
            cursor.close()
            print(result)
        case 2: 
            print("Password hinzufügen")
            print("Gebe den namen deines Passwords ein")
            name = input()
            print("Gebe das Password ein")
            passwordinput = input()
            query= """Insert into Passwords (name, password, User_ID) Value(%s , %s , %s)"""
            cursor = connection.cursor()
            cursor.execute(query, (name , passwordinput , UserID))
            connection.commit()
            print(name, passwordinput)
        


print("Wilkommen im Passwortmanager")
print("Gebe deinen Nutzernamen an:")
username = input()
print("Gebe dein Password an:")
password = input()
UserID = Login(username, password)
if UserID != 0:
    UserID = UserID[0]
    print("Willkommen " + username)
    Menu()
else:
    print("Benutzername oder Password falsch!")