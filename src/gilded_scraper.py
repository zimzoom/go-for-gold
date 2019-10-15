import praw
import pandas as pd
import datetime as dt
import os

client_id = 'UO79QSYxu2ujuw'
client_secret = 'XRfPWRnRN0O2Wfpwmf-frAgGAmA'
user_agent = 'Private school project reading public info only (by u/wiltnotwither)'

gild_dict = { "id":[],
    "parent_id":[],
    "link_id":[],
    "gilded":[],
    "author":[],
    "created":[],
    "is_submitter":[],
    "permalink":[],
    "score":[],
    "body":[],
    "topic":[] }

for submission in askreddit.hot(limit=5):
    topic = submission.title
    submission.comments.replace_more(limit=None)
    for comment in list(submission.comments):
        gild_dict["id"].append(comment.id) if comment.id else gild_dict["id"].append("None")
        gild_dict["parent_id"].append(comment.parent_id) if comment.parent_id else gild_dict["parent_id"].append("None")
        gild_dict["link_id"].append(comment.link_id) if comment.link_id else gild_dict["link_id"].append("None")
        gild_dict["gilded"].append(comment.gilded) if comment.gilded else gild_dict["gilded"].append("None")
        gild_dict["author"].append(comment.author) if comment.author else gild_dict["author"].append("None")
        gild_dict["created"].append(comment.created_utc) if comment.created_utc else gild_dict["created_utc"].append("None")
        gild_dict["is_submitter"].append(comment.is_submitter) if comment.is_submitter else gild_dict["is_submitter"].append("None")
        gild_dict["permalink"].append(comment.permalink) if comment.permalink else gild_dict["permalink"].append("None")
        gild_dict["score"].append(comment.score) if comment.score else gild_dict["score"].append("None")
        gild_dict["body"].append(comment.body) if comment.body else gild_dict["body"].append("None")
        gild_dict["topic"].append(topic)
