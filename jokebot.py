import time
import csv
import sys
import requests

# given a prompt and punchline, prints out
# the prompt and punchline with 2 second delay inbetween.
def tellJoke(prompt, punchline):
	print(prompt)
	time.sleep(2)
	print(punchline)

# Asks for user input between jokes
def userInput():
	while True:
		time.sleep(0.5)
		x = input("What do I do next? (next/quit) ")
		if x == "next":
			return True
		elif x == "quit":
			return False
		else:
			print("Sorry, I don't understand.")

# opens specified joke file and returns a list of jokes
def openFile(fileName):
	try:
		with open(fileName, 'r') as jokes:
			reader = csv.reader(jokes)
			jokeList = list(reader)
			return jokeList
	except IOError:
		return False

# main joke bot function
def jokeBot():
	jokeList = None
	if len(sys.argv) == 1:
		jokeList = getReddit()
	else:
		jokeList = openFile(sys.argv[1])
	if jokeList is False:
		print("No joke file given.")
		return
	else:
		jokeNum = 0
		while jokeNum < len(jokeList):
			currentJoke = jokeList[jokeNum]
			tellJoke(currentJoke[0], currentJoke[1])
			jokeNum += 1
			if userInput() is False:
				return
		print("No more jokes left to tell!")

# filters individual jokes from Reddit
def checkJoke(joke):
	if joke['over_18'] is False and\
		joke['title'][0:4] in ["What", "How ", "Why "]:
		return True
	return False

# gets jokes from r/dadjokes, calls checkJoke
# to filter each one and return a list of jokes
def getReddit():
	data = requests.get('https://www.reddit.com/r/dadjokes.json', 
		headers = {'user-agent': 'the joke bot'})
	data = data.json()
	jokeList = []
	for content in data['data']['children']:
		joke = content['data']
		if checkJoke(joke):
			jokeList.append([joke['title'], joke['selftext']])
	return jokeList

jokeBot()










