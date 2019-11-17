import praw
import time 

# profanities in txt file made global
with open('profanity_list.txt', 'r') as f:
		profanity_list = [line.strip() for line in f]


def authenticate():
	# logs the bot in 
	reddit = praw.Reddit('theCensoringBot', user_agent = "I detect swear words and return a censored version of the comment")
	return reddit


def split_special_chars(word):
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


def find_and_replace(word):
	# check word to see if profanity and replace if so
	if word.lower() in profanity_list:
		word = '*censored*'
	return word


def get_saved_comments():
	# opens list containing comment IDs already replied to so I don't reply again
	with open("comments_replied_to.txt", "r") as f:
		comments_replied_to = f.read()
		comments_replied_to = comments_replied_to.split('\n')
		comments_replied_to = list(filter(None, comments_replied_to))
	return comments_replied_to


def sleep(seconds):
	# sleep for some time (seconds) 
	print('Sleeping for ' + str(seconds) + ' seconds...\n')
	time.sleep(seconds)


def censor_comment(reddit, comments_replied_to):
	# read specific comments in particular subreddit based on some attribute
	# if comment contains keyword, work my magic and reply with the censored comment
	# add comment id of comment I replied to to my list so I don't reply again
	# sleep for some time 
	for submissions in reddit.subreddit('AskReddit').rising(limit = 50): 
		submissions.comments.replace_more(limit = None)
		for comments in submissions.comments.list():
			if comments.id not in comments_replied_to:
				parent_name = comments.parent().author
				child_name = comments.author
				if 'censor-this!' in comments.body and child_name != reddit.user.me() and parent_name != reddit.user.me():
					print('new request found!\n')
					parent_comment = comments.parent().body
					child_comment = comments.body
					try:
						temp = parent_comment.split() # puts each word in UC into a list
						words_in_uc = []
						words_in_cc = []
						
						for words in temp:
							words = split_special_chars(words)
							words_in_uc.append(words)
						
						for words in words_in_uc:
							words = find_and_replace(words)
							words_in_cc.append(words)
						
						count = 0
						for words in words_in_cc:
							if words == '*censored*':
								count += 1
						
						censored_comment = ' '.join(words_in_cc)

						comments.reply('I am a bot, *bleep*, *bloop*. I found ' + str(count) + ' swear word(s) in /u/' 
										+ str(parent_name) + '\'s comment.\n\n' + '**Here is a censored version of their comment:**' 
						                + '\n\n________________________________________________\n\n' 
						                + censored_comment
						                + '\n\n________________________________________________\n\n' 
										+ 'Go [here](https://www.reddit.com/user/theCensoringBot/comments/dwssjj/about_me/) to learn more about me\n\n' 
										)
						
						with open("comments_replied_to.txt", "a") as f:
							f.write(comments.id + '\n')

					except AttributeError:
						print('captured AttributeError')
						comments_replied_to.append(comments.id)
						with open("comments_replied_to.txt", "a") as f:
							f.write(comments.id + '\n')

					except praw.exceptions.APIException:
						print('captured rate restriction error')


					finally:	
						sleep(60)


def main(): 
	# run the bot
	reddit = authenticate()
	print('Authenticated as /u/{}\n'.format(reddit.user.me()))
	comments_replied_to = get_saved_comments()
	while True:
		censor_comment(reddit, comments_replied_to)


if __name__ == '__main__':
	main()
