#!/usr/bin/env python
# coding: utf-8

# In[198]:


# import libraries necessary for drawing random English words, accessing system date/time data, and reading local files
import os
import ast
import sys
from wordfreq import top_n_list
import random
from datetime import datetime 


# In[192]:


class game:
    def __init__(self, user, target, maxmiss):
        self.user = user
        self.target = target
        self.maxmiss = maxmiss
        self.n = 1
        self.miss = 0
        self.misses = ""
        self.hits = ""
        self.working = []
        for i in target:
            self.working.append("_")

    def guess(self, letter):
        # add 1 to guess count
        self.n += 1

        # determine if letter has already been guessed
        if ((letter in self.misses) or (letter in self.hits)):
            print(letter+" has already been guessed.\n")
            
        # determine if guess is correct
        elif not(letter in self.target):

            # if not, increase miss count and announce to the user that the guess is wrong
            self.miss += 1

            # update list of incorrect guesses
            self.misses = self.misses + letter
            print(letter," is not in the word. Miss count: ",self.miss,"\n")

        # if it is correct, then...
        else:

            # update list of correct guesses
            self.hits = self.hits + letter
            
            # count the number of occurrences of the guess in the target word
            m = 0
            for i in range(0,len(self.target)):
                if self.target[i] == letter:
                    m += 1

                    # update the board to reflect correct guess
                    self.working[i] = letter

            # announce state of game to the user
            print("There are ",m," instances of ",letter,". Miss count: ",self.miss,"\n")



# In[193]:


# display the board
def display(list):
    output = ""
    for i in list:
        output = output+i+" "
    print(output+"\n\n")


# In[194]:


# change the high scores file to reflect new high scores (if applicable)
def recordscore(rec, filename):

    # open the hangman_scores.txt file
    with open(filename, "r") as file:

        # strip whitespace and read file as literal python code
        # high score file simply contains list of tuples which store score information
        highscores = ast.literal_eval(file.read().strip())
        newscores = []

        # set default indication that high scores havent been changed
        changed = False

        # search through existing high scores and compare if current score should be on the list
        for i in range(0,len(highscores)):

            # if current score beats an current high scores and the list hasn't yet been updated, then do so
            if ((rec[2]>highscores[i][2]) and (changed == False)):
                newscores.append(rec)
                newscores.append(highscores[i])

                # indicate that the list has been updated
                changed = True
            else:

                # add rest of high scores in their correct places
                newscores.append(highscores[i])

        # add score to the end of the list if it ties existing high score #10
        if ((rec[2]==highscores[-1][2]) and (not(rec in newscores))):
            newscores.append(rec)

        # remove high scores from the list which are not in the top 10 (including ties for #10)
        torem = []
        if len(newscores)>10:
            for i in range(10,len(newscores)):
                if newscores[i][2]<newscores[9][2]:
                    torem.append(newscores[i])
            for i in torem:
                newscores.remove(i)

        # save the new high scores as list of tuples in hangman_scores.txt file
        with open(filename, "w") as file:
            file.write(str(newscores))


# In[195]:


# print the high score board
def printhighscores(filename):

    # read hangman_scores.txt file
    with open(filename, "r") as file:

        # save high scores data as list of tuples since it is stored that way
        highscores = ast.literal_eval(file.read().strip())

        # print scoreboard labels
        print("High Scores: \n date/time | username | score | # of guesses | # of misses | difficulty | target word \n")

        # print each high score
        for i in highscores:
            print("(",highscores.index(i)+1,") ",i,"\n")
        print("score is calculated as the length of the word minus the number of guesses used minus the difficulty. only successful games are counted.\n")


# In[199]:


# run the game
def initialize():

    # prepare game by checking if high score file exists
    filename = "hangman_scores.txt"
    if not(os.path.exists(filename)):
        
        # if not, create file and write empty list to file
        with open(filename, "w") as file:
            file.write("[]")

    # save the top 10000 most common English words from the library wordfreq as the variable wordlist and draw a random word to be the target word.
    wordlist = top_n_list('en', 10000)
    target = random.choice(wordlist)
    
    # run the game and collect score information as output
    rec = game(input("Enter a username to begin.\n"), target, int(input("Enter a difficulty/maximum number of misses, which will be deducted from final score\n")))

    # begin playing the game. end the game after all letters are guessed or maxmiss wrong guesses (misses)
    while rec.miss<rec.maxmiss and ("_" in rec.working):

        # display the board
        display(rec.working)

        # prompt the user for a guess
        print("hits: ",rec.hits," misses: ",rec.misses)
        rec.guess(input("Guess #"+str(rec.n)+":"))

    # after the game ends, determine if the game ended due to the user missing m guesses or guessing all letters
    if rec.miss >= rec.maxmiss:

        # if game ended due to too many wrong guesses, announce loss to user and show answer
        print("You lose :(\n The word was "+rec.target+"\n")
        
    else:

        # if game ended due to guessing the word correctly, announce win to user and prompt the user to play again
        display(rec.working)
        score = len(rec.target)-rec.n-rec.maxmiss
        print("You win :)\n")
        print("The length of the word was ",len(rec.target),", you took ",rec.n," guesses, and had ",rec.miss," misses.\n")
        print("Your score was: ",score)
        # run recordscore to determine if the collected score is a high score. if so, add it to the high score list
        recordscore((datetime.now().isoformat(), rec.user, score, rec.n, rec.miss, rec.maxmiss, rec.target), filename)

    # print all high scores
    printhighscores(filename)

    # prompt user to play again
    inp = input("Play again? If so, type Yes or yes. Otherwise type anything.")
    
    # if the user selects to play again, then begin another game
    if ((inp == "Yes") or (inp == "yes")):
        initialize()

