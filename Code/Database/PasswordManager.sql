Create Database PasswordManager;
Use PasswordManager;

Create Table Users(
    User_ID int Primary Key AUTO_INCREMENT,
    Name varchar(255) not null,
    VorName varchar(255) not null,
    MasterPassword text not null,
    LoginName varchar(10) not null /* LoginName setzt sich aus den ersten drei Bustaben vom Vor und nachnamen und einer zahl zusammen */
);

Create Table Passwords(
    Password_ID int Primary Key  AUTO_INCREMENT,
    Name varchar(255) not null,
    password text not null,
    User_ID int, FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
);

INSERT INTO Users (User_ID, Name, VorName, MasterPassword, LoginName) VALUES
(1, 'Müller', 'Max', 'MasterPass123', 'MulMax1'),
(2, 'Schmidt', 'Anna', 'SecurePass456', 'SchAnn2'),
(3, 'Weber', 'Tom', 'TopSecret789', 'WebTom3');

INSERT INTO Passwords (Password_ID, Name, password, User_ID) VALUES
(1, 'Facebook', 'Pass1234', 1),
(2, 'Instagram', 'Instapass1', 1),
(3, 'Twitter', 'TwitPass99', 1),
(4, 'LinkedIn', 'LinkPass22', 1),
(5, 'Email', 'MailPass11', 1);

INSERT INTO Passwords (Password_ID, Name, password, User_ID) VALUES
(6, 'Facebook', 'AnnaFB123', 2),
(7, 'Instagram', 'AnnaInsta45', 2),
(8, 'Twitter', 'AnnaTwit67', 2),
(9, 'LinkedIn', 'AnnaLink23', 2),
(10, 'Email', 'AnnaMail78', 2);

INSERT INTO Passwords (Password_ID, Name, password, User_ID) VALUES
(11, 'Facebook', 'TomFB890', 3),
(12, 'Instagram', 'TomInsta12', 3),
(13, 'Twitter', 'TomTwit34', 3),
(14, 'LinkedIn', 'TomLink56', 3),
(15, 'Email', 'TomMail67', 3);