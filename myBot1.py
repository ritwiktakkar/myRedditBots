import praw
import configForBot1   # credentials for this bot -- file not visible on GitHub
import time 

config = configForBot1

# making the list of profanities' scope global 
with open('profanity_list.txt', 'r') as f:
	profanity_list = [line.strip() for line in f]

# this method logs the bot in 
def bot_login():
	print("Logging in...")
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "Im a bot that detects swear words and returns a censored version of the comment")
	print("Logged in!")
	return r

# function that retrieves the comment that summoned the bot
def censor_comment(r):
	for comments in r.subreddit('botTesting123456').comments(limit=10):
		if 'censor-this!' in comments.body:
			uncensoredComment = comments.body
			print(uncensoredComment)
			wordsInUC = uncensoredComment.split()


			#print(wordsInUC)
			#wordsInCC = []
			#censoredComment = ' '.join(wordsInCC)
			#print('Here is a censored version of the comment:\n'+censoredComment)
	print('sleeping for 10 secs')
	time.sleep(10)	

while True:
	r = bot_login()
	censor_comment(r)