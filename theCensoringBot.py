import praw
import configForTCB   # credentials for this bot -- file not visible on GitHub
import time 

config = configForTCB

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

def splitSpecialChars(word):
	# checks word
	# if word starts/ends with special char and 
		# 1) is profanity: returns profanity without special chars
		# 2) isn't profanity: returns word without change
	orig_word = word
	for letter in word:
		if (letter.isalpha() == False):
			word = word.strip(letter)
	if word in profanity_list:
		return word
	else:
		return orig_word

def findAndReplace(word):
	if word.lower() in profanity_list:
		word = '(profanity)'
	return word

def get_saved_comments():
	with open("comments_replied_to.txt", "r") as f:
		comments_replied_to = f.read()
		comments_replied_to = comments_replied_to.split('\n')
		comments_replied_to = list(filter(None, comments_replied_to))
	return comments_replied_to

# function that retrieves the comment that summoned the bot
def censor_comment(r, comments_replied_to):
	for comments in r.subreddit('botTesting123456').comments(limit=10):
		if 'censor-this!' in comments.body and comments.id not in comments_replied_to and comments.author != r.user.me():
			uncensoredComment = comments.body # this string is the uncensored comment that called the bot
			print("here is the uncensored comment:\n"+uncensoredComment) 
			wordsInUC_unrev = uncensoredComment.split() # puts each word in UC into a list
			wordsInUC_unrev2 = []
			wordsInCC = []
			for words in wordsInUC_unrev:
				words = splitSpecialChars(words)
				wordsInUC_unrev2.append(words)
			for words in wordsInUC_unrev2:
				words = findAndReplace(words)
				wordsInCC.append(words)
			count = 0
			for words in wordsInCC:
				if words == '(profanity)':
					count += 1
			censoredComment = ' '.join(wordsInCC)
			comments.reply('I found ' + str(count) + ' profanities in the comment.\n\n' + 
				  'Here is a censored version of the comment:\n\n'
				  + censoredComment)
			print('Replied to comment id: '+comments.id)
			comments_replied_to.append(comments.id)
			with open("comments_replied_to.txt", "a") as f:
				f.write(comments.id + '\n')

	print('sleeping for 4 secs')
	time.sleep(4)	


r = bot_login()

comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
	censor_comment(r, comments_replied_to)