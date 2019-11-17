# myRedditBot

## What theCensoringBot bot does / will do
This Reddit bot will ultimately:
1. [ ] endlessly wait to be called by users based on given condition (eg sort through comments in the 10 newest posts on r/AskReddit)
2. [x] when called, it will read the comment of the user to whom the caller replied
3. [x] while reading the user's comment, it will search for all the profanities in it and calculate the amount
4. [x] it will then replace each of the profanities with "(profanity)" :arrow_right: this will be the censored comment
5. [x] after doing so, it will reply to the caller's comment with the censored comment
6. [x] when waiting to be called, it will make sure not to reply to comments that contain the keyword that calls it if it has already done so
