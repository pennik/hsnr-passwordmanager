import math
import random
import os
import string
import bcrypt
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet

def load_key():
    with open("secret.key", "rb") as key_file: # Öffnet die datei secret.key in der unser generierter Key zum ver und Endschlüsseln gespeicher ist
        return key_file.read()
    
def encrypt_password(password: str) -> bytes:
    key = load_key()    # Läd den Key
    fernet = Fernet(key) # erstellt ein objekt und läd den key
    encrypted_password = fernet.encrypt(password.encode()) # verschlüsselt das password was mitgegeben wurde
    return encrypted_password

def decrypt_password(encrypted_password: bytes) -> str:
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode() # entschlüsselt das verschlüsselte password mithilfe des keys
    return decrypted_password

try:
    # Verbindungsaufbau zur Datenbank
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='passwordmanager'
    )

except Error as e:
    print("Fehler beim Verbinden mit MySQL", e)

def is_valid_password(password: str) -> bool: 
    # checkt ob das Password die Anforderungen erfüllt und gibt entweder false (0) zurück wenn ein password den Anforderungen nicht 
    # entspricht oder True (1) wenn das Password ok ist

    has_letter = any(char.isalpha() for char in password)  # Mindestens ein Buchstabe 
    has_digit = any(char.isdigit() for char in password)   # Mindestens eine Zahl
    has_special = any(char in string.punctuation for char in password)  # Sonderzeichen

    if len(password) < 12: print("Das Password ist zu kurz bitte beachte das das Password mindestens 12 Zeichen lang sein muss!"); return 0
    if has_letter != True: print("Das Password enthält keine Bustaben bitte beachte das dein Passowrd aus mindestens 12 Zeichen bestehen muss die sich aus Bustaben, Zahlen und Sonderzeichen zusammen setzen!"); return 0
    if has_digit != True: print("Das Password enthält keine Zahl bitte beachte das dein Passowrd aus mindestens 12 Zeichen bestehen muss die sich aus Bustaben, Zahlen und Sonderzeichen zusammen setzen!"); return 0
    if has_special != True: print("Das Password enthält kein Sonderzeichen bitte beachte das dein Passowrd aus mindestens 12 Zeichen bestehen muss die sich aus Bustaben, Zahlen und Sonderzeichen zusammen setzen!"); return 0

    return 1

def clear_console():
        os.system("cls")

def Login(username, password):
    try:
        # Einfache Sql abfrage die schaut ob es einen User mir dem gegebenen usernamen und password gibt und dann eine ID zurück gibt
        query = "SELECT User_ID FROM `users` WHERE LoginName = %s AND MasterPassword = %s" 
        cursor = connection.cursor()  # Neuer Cursor
        cursor.execute(query, (username, password)) # query wird mit dem username und password gefüllt
        result = cursor.fetchone() #fetchone gibt nur ein ergebnis wieder
        cursor.close()  # Schließe den Cursor nach Gebrauch
        return result #returnt die ID des users
    except Error as e:
        print("Fehler beim Ausführen der Login-Abfrage:", e)
        return False

def GetAllPasswords():
    print("Liste der passwörter")
    # Gibt Namen des Passworts und passwort aus
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
    for row in result:
        tempPassowrd = decrypt_password(row[1]) # entschlüsselt die passwörter aus der datenbank
        print(f"Name: {row[0]}, Passwort: {tempPassowrd}")
    input("Drücke Enter, um zum Hauptmenü zurückzukehren.")

def AddPassword():
    print(UserID)
    ID = UserID[0]
    print(ID)
    print("Password hinzufügen")
    name = input("Gebe den namen deines Passwords ein\n")
    passwordinput = input("Gebe das Password ein\n")
    if is_valid_password(passwordinput) != True:
        input("Drücke Enter, zum Password erstellen zurückzukehren.")
        name = ""
        passwordinput = ""
        AddPassword()
    if name == "": #Wenn name leer ist dann
        print("Du hast kein Password angegeben!")
        input("Drücke Enter, um zum Password erstellen zurückzukehren.")
        clear_console()
        name = ""
        passwordinput = ""
        AddPassword()
    if passwordinput == "":
        print("Du hast kein Password angegeben!")
        input("Drücke Enter, um zum Password erstellen zurückzukehren.")
        clear_console()
        name = ""
        passwordinput = ""
        AddPassword()
    else:
        encryptedPassword = encrypt_password(passwordinput) # Ruft die funktion zum verschlüsseln auf
        query= """Insert into Passwords (name, password, User_ID) Value(%s , %s , %s)"""
        cursor = connection.cursor()
        cursor.execute(query, (name , encryptedPassword , ID))
        connection.commit()
    input("Drücke Enter, um zum Hauptmenü zurückzukehren.")

def GeneratePassword():
    length = int(input("Wie lang soll dein Password sein?: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print(f"Generated password: {password}")
    input("Drücke Enter, um zum Hauptmenü zurückzukehren.")

def Menu():
    clear_console()
    print("Was möchtest du machen?")
    print("1. Passwordabfragen \n2. Password Hinzufügen \n3. Password Generieren")
    usecase = int(input())
    match usecase:
        case 1:
            clear_console()
            GetAllPasswords()
            clear_console()
            Menu()
        case 2:
            clear_console()
            AddPassword()
            clear_console()
            Menu()
        case 3:
            clear_console()
            GeneratePassword()
            clear_console()
            Menu()
        case _:
            print("Du haste eine Zahl eingegeben die zu keinem Menü Punkt führt!")
            input("Drücke Enter, um zurück zum Hauptmenü zu kommen.")
            Menu()

    
clear_console()
print("Wilkommen im Passwortmanager")
print("Gebe deinen Nutzernamen an:")
username = input()
print("Gebe dein Password an:")
password = input()
UserID = Login(username, password)
if UserID != "":
    print(UserID)
    print("Willkommen " + username)
    Menu()
else:
    print("Benutzername oder Password falsch!")
