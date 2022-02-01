import time
import json
import os
import secrets

import praw
import requests
from praw.models import Comment, Message


class indirbeni_cli:
    def __init__(self):
        self.ind = 2749
        self.path = os.getcwd()
        self.NSFW = {True: "### NSFW", False: ""}
        self.subs = ['KGBTR', 'ArsivUnutmaz', 'INDIRBENI', 'u_indirbeni',
                     'u_oldventura', 'Turkey', 'TurkeyJerky', 'BLKGM', 'AtaturkKutuphanesi']
        self.help = open("%s/help.md" % (self.path), "r").read()

        self.load_replies()
        self.connect_to_reddit()

        self.run()

    def connect_to_reddit(self):
        self.reddit = praw.Reddit(
            "indirbeni",
            config_interpolation="basic"
        )

    def load_replies(self):
        with open('%s/replies.json' % (self.path),) as f:
            self.replies = json.load(f)['text']

    def format_url(self, url, title, nsfw):
        url = "## " + url + "\n\n%s\n\n%s" % (title, nsfw)
        return url

    def format_text(self, author, shortlink):
        text = "Buyur u/%s, işte içerik yukarıda \^\^\n\nBu da gönderinin kendisi: [LINK](%s)\n\n### -> [DONATE](https://oldventura.github.io/donate/)" % (
            author, shortlink)
        return text

    def format_comment(self, url):
        cmt = "# [INDIR](%s)\n\n-\n\n##### -> [BAĞIŞ](https://oldventura.github.io/donate/)" % (url)
        return cmt

    def random_porn(self):
        try:
            page = requests.get("https://www.pornhub.com/video/random").url
        except:
            page = "https://www.pornhub.com/view_video.php?viewkey=ph60f74690300a0"
        return "## [SURPRISE PORN](%s)" % (page)

    def random_xkcd(self):
        try:
            page = requests.get("https://c.xkcd.com/random/comic/").url
        except:
            page = "https://xkcd.com/162/"
        return "## [SURPRISE XKCD](%s)" % (page)

    def random_wiki(self):
        try:
            page = requests.get(
                "https://tr.wikipedia.org/wiki/%C3%96zel:Rastgele").url
        except:
            page = "https://tr.wikipedia.org/wiki/Mast%C3%BCrbasyon"
        return "## [SURPRISE WIKI](%s)" % (page)

    def random_link(self):
        try:
            with open("%s/links.txt" % (self.path), "r") as s:
                s = s.read().splitlines()
                if len(s) >= 1:
                    text = s[secrets.randbelow(len(s))]
        except FileNotFoundError:
            text = "https://www.youtube.com/watch?v=bSpqLqC7U6g"
        return "## [SURPRISE FILE](%s)" % (text)

    def handleit(self, item):
        if "u/indirbeni random" in item.body:
            item.reply(self.random_link())
        elif "u/indirbeni wiki" in item.body:
            item.reply(self.random_wiki())
        elif "u/indirbeni porn" in item.body:
            item.reply(self.random_porn())
        elif "u/indirbeni xkcd" in item.body:
            item.reply(self.random_xkcd())
        elif "u/indirbeni help" in item.body:
            item.reply(self.help)
        else:
            url = "https://indirbeni.herokuapp.com/download/%s" % (
                item.submission.id)
            comment = self.reddit.submission(id='ogk6aj').reply(
                self.format_url(
                    url, item.submission.title, self.NSFW[item.submission.over_18]
                )
            )
            comment.reply(
                self.format_text(
                    item.author.name, item.submission.shortlink
                )
            )
            item.reply(self.format_comment(url))

        Comment.mark_read(item)
        item.mark_read()

    def run(self):
        item = None
        while True:
            try:
                for item in self.reddit.inbox.unread(limit=None):
                    Message.mark_read(item)
                    item.mark_read()
                    print("\nfrom:", item.author)
                    print("in:", item.context)
                    print("type:", item.type)
                    print("message:", item.body)

                    if item.type == "username_mention":
                        if item.submission.subreddit.display_name in self.subs and item.author not in ["AutoModerator", "getdown2me"]:
                            try:
                                self.handleit(item)
                            except Exception as e:
                                if "No media found" in str(e):
                                    item.reply(
                                        "Ya ben yamuluyorum ya da bu post'ta dikkate alınacak bir şey yok amk")
                                else:
                                    print("Error_message:", e)
                        Message.mark_read(item)
                        item.mark_read()

                    elif item.type == "post_reply":
                        if item.submission.subreddit.display_name in ['u_indirbeni', 'KGBTR', 'INDIRBENI']:
                            if item.author not in ["AutoModerator", "getdown2me"]:
                                try:
                                    if item.body == "u/indirbeni random":
                                        item.reply(self.random_link())
                                    else:
                                        item.reply(
                                            self.replies[secrets.randbelow(len(self.replies))])
                                except:
                                    pass
                        else:
                            if item.author != "AutoModerator":
                                item.reply(
                                    "Anam yabancılarla konuşma dedi, ne diyon lan sen öyle?")

                    elif item.type == "comment_reply":
                        if item.submission.subreddit.display_name in ['u_indirbeni', 'KGBTR', 'INDIRBENI']:
                            if item.author not in ["AutoModerator", "getdown2me"]:
                                try:
                                    if item.body == "u/indirbeni random":
                                        item.reply(self.random_link())
                                    else:
                                        item.reply(
                                            self.replies[secrets.randbelow(len(self.replies))])
                                except:
                                    pass

                    else:
                        print(item.type)

                self.ind += 1

                if self.ind == 2750:
                    self.reddit.submission("ofbxx4").reply(
                        "Update: %s  Fully functional." % (time.strftime("%D %H:%M")))
                    print("Fully functional.")
                    self.ind = 0

            except Exception as e:
                if item:
                    Message.mark_read(item)
                    item.mark_read()

                print("Got Error:\nType:%s\n###" % (e.__class__.__name__))
                print(str(e))
                print("###")
