#scrape reddit v1

import praw
import pprint
import sys
import random
import time

common_spammy_words = ['udemy','course','save','coupon','free','discount']

reddit = praw.Reddit(client_id  = 'input here',
                     client_secret  =  'input here',
                     username  =  'input here',
                     password  =  'input here',
                     user_agent  =  'input here')

##subreddit = reddit.subreddit('python')

#bot to detect spam

common_spammy_words = ['udemy','course','save','coupon','free','discount']

def find_spam_by_name(search_query):
    authors = []
    for submission in reddit.subreddit("all").search(search_query, sort="new", limit=11):
        print(submission.title, submission.author, submission.url)
        if submission.author not in authors:
            authors.append(submission.author)
    return authors

 
if __name__ == "__main__":
    while True:
        current_search_query = random.choice(["udemy"])
        spam_content = []
        trashy_users = {}
        smelly_authors = find_spam_by_name(current_search_query)
        for author in smelly_authors:
            user_trashy_urls = []
            sub_count = 0
            dirty_count = 0
            try:
                for sub in reddit.redditor(str(author)).submissions.new():
                    submit_links_to = sub.url
                    submit_id = sub.id 
                    submit_subreddit = sub.subreddit
                    submit_title = sub.title
                    dirty = False
                    for w in common_spammy_words:
                        if w in submit_title.lower():
                            dirty = True
                            junk = [submit_id,submit_title]
                            if junk not in user_trashy_urls:
                                user_trashy_urls.append([submit_id,submit_title,str(author)])

                    if dirty:
                        dirty_count+=1
                    sub_count+=1

                try:
                    trashy_score = dirty_count/sub_count
                except: trashy_score = 0.0
                print("User {} trashy score is: {}".format(str(author), round(trashy_score,3)))

                if trashy_score >= 0.5:
                    trashy_users[str(author)] = [trashy_score,sub_count]

                    for trash in user_trashy_urls:
                        spam_content.append(trash)  

            except Exception as e:
                print(str(e))

        for spam in spam_content:
            spam_id = spam[0]
            spam_user = spam[2]
            submission = reddit.submission(id=spam[0])
            created_time = submission.created_utc
            if time.time()-created_time <= 86400:
                link = "https://reddit.com"+submission.permalink

                message = """*Beep boop*

I am a bot that sniffs out spammers, and this smells like spam.

At least {}% out of the {} submissions from /u/{} appear to be for Udemy affiliate links. 

Don't let spam take over Reddit! Throw it out!

*Bee bop*""".format(round(trashy_users[spam_user][0]*100,2), trashy_users[spam_user][1], spam_user)

                try:
                    with open("posted_urls.txt","r") as f:
                        already_posted = f.read().split('\n')
                    if link not in already_posted:
                        print(message)
                        submission.reply(message)
                        print("We've posted to {} and now we need to sleep for 12 minutes".format(link))
                        with open("posted_urls.txt","a") as f:
                            f.write(link+'\n')
                        time.sleep(12*60)
                        break
                except Exception as e:
                    print(str(e))
                    time.sleep(12*60)

    


##for comment in subreddit.stream.comments():
##    try:
##        parent_id = str(comment.parent())
##        
##        original = reddit.comment(parent_id)
##        print('Parent: ')
##        print(original.body)
##        print('Reply: ')
##        print(comment.body)
##        
##    except praw.exceptions.PRAWException as e:
##        pass
##        


            
##top_subreddit = subreddit.top(limit = 10) #request limit is 1000

##submission_dict = { 'Title': [] , 'Score': [] , 'Id':[], 'Url':[],
##               'Comms_num':[], 'Created': [], 'Body':[] } 

    
#parsing and downloading the data

##for submission in subreddit.top(limit = 1):
####    print(submission.title, submission.id)
##    submission_dict['Title'].append(submission.title)
##    submission_dict['Score'].append(submission.score)
##    submission_dict['Id'].append(submission.id)
##    submission_dict['Url'].append(submission.url)
##    submission_dict['Comms_num'].append(submission.num_comments)
##    submission_dict['Created'].append(submission.created)
##    submission_dict['Body'].append(submission.selftext)
##
##    print('Title:','Score','Id','Url','Comms_num','Created','Body')
##    print(submission_dict)
##    
    
