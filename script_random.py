#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import praw
from praw.models import MoreComments

class CollectRandom:
    def __init__(self):
        self.links = []
        self.path  = os.getcwd()
        self.connect_to_reddit()
        self.collect()

    def connect_to_reddit(self):
        self.reddit = praw.Reddit(
            "indirbeni",
            config_interpolation="basic"
        )

    def collect(self):
        try:
            submission = self.reddit.submission(id="ogk6aj")
            submission.comment_sort = 'new'
            for top_level_comment in submission.comments[0:200]:
                if isinstance(top_level_comment, MoreComments):
                    continue
                for i in top_level_comment.body.split():
                    if "/download/" in i:
                        self.links.append(i)
            with open("links.txt", "a+") as f:
                f.write("\n".join(self.links))

        except:
            with open("links.txt", "a+") as f:
                f.write("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
