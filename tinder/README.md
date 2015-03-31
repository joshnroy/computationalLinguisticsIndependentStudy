# About the Tinder Bot
## Purpose
The purpose of this tinder bot is not to flirt with people or attempt to get dates. Rather, its purpose is to use tinder as a set of learning/testing data to learn how to speak English and respond to common phrases.
## Why Tinder
Tinder happens to be a very fruitful place to find casual conversation. In addition, it is up 24 hours a day and would allow the bot to assign itself feedback based on how long (in messages) it is able to hold a conversation. In addition, it would enable the bot to learn common speech patterns used by humans without direct supervision from the user of the program. In essence, the program could be left running overnight and continue learning.

# How it Works
## General Step Through Process
1. Automatically like all of the profiles (male and female) within a certain area Probably a very large area. 100 miles or more as the system alllows. The following steps are done for each match
2. Obtain a match
3. Randomly pick from a weighted list (probably in a database) a starter message 
4. Recieve a message back
5. Randomly pick from a weighted list based on the message(s) and ending words/sentences in the conversation
6. Repeat steps 4-5 until there is not a response for a specified amount of time.
7. After the conversation is decided to be finished, rank how well the conversation went based on how many messages it went on for.
8. Assign/correct values on each response based on the ranking of the conversation


# Parts
Python
[MongoDB](https://api.mongodb.org/python/current/)
