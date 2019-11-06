import praw
import configForBot1   # credentials for this bot -- file not visible on GitHub
import time

config = configForBot1

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

# this method tells the bot what to do as it runs
def run_bot(r):
	for comments in r.subreddit('botTesting123456').comments(limit=5):
		if "stupid" in comments.body:
			print("String found in comment id: "+comments.id)
			comments.reply("hey i found a string saying \"stupid\" in the comments of this post")
			comments.reply("im stupid because i will keep replying to this comment over and over again\nbecause that's how im programmed :(")
			comments.reply("phew... i need to sleep for 10 seconds...")
	print("im stupid because i will keep replying to this comment over and over again\nbecause that's how im programmed :(")
	print("phew... i need to sleep for 10 seconds...")
	time.sleep(10)

# run this bot forever
while True:
	r = bot_login()
	run_bot(r)