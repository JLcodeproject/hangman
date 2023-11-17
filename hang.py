# Hangman game
import random
import os
import time
import csv
import sys
from prettytable import PrettyTable

class Game():
    """
    Starts a hangman game, and initializes the answer.
    Keeps track of the guesses and words remaining.
    """
    #base words in case winner.csv is empty
    wordBank = ["chester","vivian","gunash","rouzbeh","jacqueline","dylan","heidi"]

    def __init__(self):
        # Initializes the first game
        self.moreWords()
        self._answer = random.choice(Game.wordBank)
        self._status = "_" * len(self.getAnswer())
        self._remainingGuesses = len(self.getAnswer())
        self._guessed = set()
        self._score = 0
        self._end = False

    def moreGame(self):
        # Initialize more games
        self._answer = random.choice(Game.wordBank)
        self._status = "_" * len(self.getAnswer())
        self._remainingGuesses = len(self.getAnswer())
        self._guessed = set()

    def moreWords(self):
        # Adds more words to wordBank from the winner.csv
        file = "winner.csv"
        try:
            with open(file,'r') as data:
                reader = csv.DictReader(data, delimiter=",")
                winners = list(reader)
                for winner in winners:
                    if winner["name"] not in Game.wordBank:
                        Game.wordBank.append(winner["name"])
        except FileNotFoundError:
            sys.exit(f"Error: The file '{file}' was not found.")
        except csv.Error as e:
            print(f"Error while reading CSV file '{file}': {e}")

    def endNow(self):
        self._game = True

    def getEnd(self):
        return self._game

    def validLetter(self,letter):
        # Checks if valid letter
        return letter.isalpha() and len(letter) == 1 and letter not in self._guessed

    def getStatus(self):
        # Shows str of current solved letters and strings
        return self._status

    def getWrongGuesses(self):
        # Returns a str of previous guesses
        return ', '.join(self._guessed)

    def getRemainingGuesses(self):
        # A int showing remaining Guesses
        return self._remainingGuesses

    def getBank(self):
        return Game.wordBank

    def getScore(self):
        return self._score

    def getAnswer(self):
        return self._answer

    def play(self):
        # Ends the game in win or loss
        while True:
            if self.getRemainingGuesses() == 0:
                # for losing the game
                print(f"Sorry you've lost, the answer is {self.getAnswer()}")
                self.endNow()
                self.countdownTimer(3)
                break
            elif self.getStatus() == self.getAnswer():
                print(f"Congratulations! You've correctly guessed {self.getAnswer()}")
                self._score += 1
                print(f"Current Score: {self.getScore()}")
                self.countdownTimer(3)
                break
            else:
                self.playRound()

    def playRound(self):
        """ Checks whether the guess has already been 1) guessed 2) correct 3) wrong.
            1) Takes in a valid letter
            2) Updates the status list with Correct letter
            3) Updates the guessed list by with Wrong guesses
        """
        self.getLegend()
        letter = 'dummy'
        while not self.validLetter(letter):
            letter = input("Please enter only one valid new letter: ").lower().strip()

        # cannot substitude in a str, must change to list to change 1 char, then rejoin into str
        statusList = list(self.getStatus())
        if letter in self.getAnswer():
            # fill in _ with letter in the status
            for c in range(len(self.getAnswer())):
                if letter == self._answer[c].lower():
                    statusList[c] = letter
            self._status = ''.join(statusList)

        else:
            # add failed guess to _guessed and updates counter
            self._remainingGuesses -= 1
            self._guessed.add(letter)
        os.system('clear')

    def countdownTimer(self,seconds):
        for n in range(seconds, 0, -1):
            print(f"Time remaining before new game: {n} seconds")
            time.sleep(1)
        clearscreen()
        print(f"Starting a new game.")

    def getLegend(self):
        print(f"Problem: {self.getStatus()} [{len(self._answer)}]")
        print(f"Already guessed: {self.getWrongGuesses()}")
        print(f"Guesses remaining: {self.getRemainingGuesses()}")

class History:
    """
    1) Historical top 5 players in hang from history.txt,
    2) dictionary with highest solved names
    3) updates Game.wordBank
    """
    filename = "winner.csv"
    def __init__(self):
        # initializes a dictionary to hold "names","high_scores"
        self._scores = []
        self.readTable()

    def readTable(self):
        # Opens historical CSV and populates the _scores
        try:
            data = open(History.filename,'r')
        except IOError or FileNotFoundError:
            sys.exit("Could not read file.")
        except:
            sys.exit("Unexcepted error: ", sys.exc_info()[0])
        with data:
            reader = csv.DictReader(data, delimiter=",")
            self._scores = list(reader)

    def updateCsvAtEnd(self,name,score=0):
        # updates winner.csv with new winner's score
        pastwinners = self.getScores()

        winner = next((w for w in pastwinners if w["name"] == name), None)
        if winner:
            winner["high_score"] = max(score, winner["high_score"])
        else:
            newWinner = {"name":name, "high_score":score}
            self.getScores().append(newWinner)

        fieldnames = list(self._scores[0].keys())
        try:
            with open('winner.csv','w',newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
                writer.writeheader()
                writer.writerows(self._scores)
        except PermissionError:
            sys.exit(f"Error: Permission denied to write to '{History.filename}'.")
        except csv.Error as e:
            sys.exit(f"Error while writing  to CSV file '{History.filename}'.")

    def getScores(self):
        # prints all scores from _scores
        return self._scores

    def showTop5(self):
        # returns top 5 dics highest scores from _scores
        key = 'high_score'
        sorted_scores = sorted(self._scores, key = lambda x: int(x[key]), reverse = True)
        return sorted_scores[:5]

    def clearTable(self,name=all):
        # removes 1 player's score, or cleans entire table
        if name == "all":
            self._scores = {}
        else:
            del self._scores[name]

def clearscreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    game = Game()
    while True:
        user = input("Do you want to play a hangman game? (Y / N): ").upper().strip()
        clearscreen()
        if user == 'Y':
            hist = History()
            hist.readTable()
            game.moreGame()
            game.play()
        elif user == 'N' or game.getEnd():
            # At least one game played will record
            if game.getScore() > 0:
                name = input("Please enter your name: ").lower().strip()
                hist.updateCsvAtEnd(name, game.getScore())
                clearscreen()

                #top 5 returned in pretty format
                s = PrettyTable()
                s.field_names = ['Name','High Score']
                for row in hist.showTop5():
                    s.add_row(row.values())
                s.title = 'HALL OF FAME'
                s.align = 'c'
                print(s)
            sys.exit("Let's play next time then! Have a great day!")

if __name__ == "__main__":
    main()
