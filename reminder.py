#! /usr/bin/env python
from tinydb import TinyDB, Query
import yagmail
import datetime

class Reminder:
    # Constructor
    def __init__(self):
        # Create the database instance
        self.database = TinyDB('db.json')

    # ------------------------------------------
    # DATABASE
    # ------------------------------------------
    # Method to insert a player into the database
    def insert_player(self, first_name, last_name, age, phone, email, address, city, state, zipcode):
        self.database.insert({'first_name': first_name, 'last_name': last_name, 'age': age, 'phone': phone, 'email': email, 'address': address, 'city': city,
            'state': state, 'zipcode': zipcode})

    # Method to insert a tournament into the database
    def insert_tournament(self, tournament, year, month, day, time, prize):
        self.database.insert({'tournament': tournament, 'year': year, 'month': month, 'day': day, 'time': time, 'prize': prize})

    # Method to remove player from database
    def remove_player(self, fname, lname):
        q = Query()
        criteria = q.first_name == fname and q.last_name == lname
        self.database.remove(criteria)

    # ------------------------------------------
    # Email - not working
    # ------------------------------------------
    def send_email(self, tournament, time, recipients):
        # Create yagmail object
        email = yagmail.SMTP('email@teamliquid.net', 'password')
        # Get array of emails to send to
        recipients = recipients
        # Body of the message
        body = ["Don't forget about the " + tournament + " tournament tomorrow at " + time,
                "Please make sure to post a tweet about the tournament 1 - 2 hours prior",
                "Example Tweet:",
                "@YourTeammate @OtherTeammate and I are playing in the @TournamentsTwitterHandle Apex tournament",
                "starting at (insert time). Come watch us!",
                "@Twitch.tv/yourtwitchhandle #LETSGOLIQUID"]
        # For loop to send email to each recipient
        # for recipient in recipients:
        email.send(recipients, 'Reminder!', body)
        print("Sent!")

    # ------------------------------------------
    # Time
    # ------------------------------------------
    def check_date(self):
        # Get current time
        dt = datetime.datetime.now()
        # Create query
        q = Query()
        # Criteria for reminder
        criteria = q.year == str(dt.year) and q.month == str(dt.month) and q.day == str(dt.day + 1)
        # Search database for a date one day from now
        result = self.database.search(criteria)
        if result:
            print("Sending...")
            Email = Query()
            players = self.database.search(Email.email.search('[teamliquid.net]'))
            for i in range(len(players)):
                self.send_email(result[0]['tournament'], result[0]['time'], players[i]['email'])
        else:
            print('No tournament tomorrow')


    # ------------------------------------------
    # Main Menu
    # ------------------------------------------
    def main_menu(self):
        print('Welcome to the Reminder!')
        print('1. Add Tournament')
        print('2. Add Player')
        print('3. Drop Player')
        print('4. Send Reminder')
        print('5. Exit')
    # ------------------------------------------
    # Input Handlers
    # ------------------------------------------
    def handle_input(self):
        argument = input("")
        argument = int(argument)
        if argument == 1:
            self.add_tournament()
        elif argument == 2:
            self.add_player()
        elif argument == 3:
            self.drop_player()
        elif argument == 4:
            self.check_date()

    # Method to collect tournament information and insert into db
    def add_tournament(self):
        name = input("Enter tournament name: ")
        year = input("Enter year: ")
        month = input("Enter month: ")
        day = input("Enter day: ")
        time = input("Enter time: ")
        prize = input("Enter prize: ")
        self.insert_tournament(name, year, month, day, time, prize)
        print("Tournament Added!\n")

    # Method to collect player information and insert into db
    def add_player(self):
        fname = input("First Name: ")
        lname = input("Last Name: ")
        age = input("Age: ")
        phone = input("Phone: ")
        email = input("Email: ")
        address = input("Address: ")
        city = input("City: ")
        state = input("State: ")
        zipcode = input("Zipcode: ")
        self.insert_player(fname, lname, age, phone, email, address, city, state, zipcode)
        print("Player Added!\n")

    # Method to drop player from database
    def drop_player(self):
        fname = input("First Name: ")
        lname = input("Last Name: ")

# ------------------------------------------
# MAIN
# ------------------------------------------
def main():
    reminder = Reminder()
    reminder.main_menu()
    reminder.handle_input()

if __name__ == '__main__':
    main()
main()
