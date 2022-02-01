#!/usr/bin/python
#-*- encoding:utf-8 -*-

import os
import traceback
from shutil import make_archive

import praw
import requests
import yt_dlp


class Downloader:
    def __init__(self):
        self.path       = os.getcwd()
        self.NSFW       = {True:"### NSFW", False:""}
        self.ydl_opts   = {'outtmpl': self.path + '/downloaded/file_id' + '.%(ext)s', 'throttledratelimit': 100}
        self.f_index    = int(open('index',).read())
        self.subs       = ['KGBTR','ArsivUnutmaz','INDIRBENI','u_indirbeni','u_oldventura','Turkey','TurkeyJerky','BLKGM','AtaturkKutuphanesi']

        self.connect_to_reddit()


    def update_index(self):
        self.f_index += 1
        os.popen("echo %s > %s/index" %(self.f_index, self.path))


    def up_ydl(self, id):
        self.ydl_opts = {'outtmpl': self.path + '/downloaded/video_' + id + '.%(ext)s', 'throttledratelimit': 100}
        return '%s/downloaded/video_%s.mp4' %(self.path, id)


    def connect_to_reddit(self):
        self.reddit = praw.Reddit(
            "indirbeni",
            config_interpolation = "basic"
        )


    def remove_files(self):
        os.system("rm -f %/gallery/*" %(self.path))
        os.system("rm -f %s/downloaded/*" %(self.path))


    def handle(self, id):
        try:
            if id.startswith("https"):
                submission = self.reddit.submission(url=id)
            else:
                submission = self.reddit.submission(id=id)

            print("Submission id:", submission.id)

            if submission.subreddit.display_name in self.subs:
                pass
            else:
                return ("Unsupported", None)

            if submission.is_self:
                return self.do_text(submission)

            else:
                url = submission.url.split("?")[0].replace("preview", "i")

                if url.startswith("https://v.redd.it") or url.startswith("https://gfycat.com"):
                    return self.do_video(submission)
                elif url.startswith("https://i.redd.it") or url.startswith("https://i.imgur.com"):
                    return self.do_image(submission,url)
                elif url.startswith("https://www.reddit.com/gallery"):
                    return self.do_gallery(submission,url)
                else:
                    print("Not supported url:", url)
                    return (None, None)

        except Exception as exception:
            print("\n##Got Error:")
            traceback.print_exc()
            print("##\n")
            return (None, None)


    def do_text(self, submission):

        print("Submission type: text")
        content = submission.selftext

        print ("Sent text!")
        return "Text", content


    def do_video(self, submission):

        print("Submission type: video")
        file_path  = self.up_ydl(submission.id)

        if not os.path.isfile(file_path):
            url        = submission.url

            # DOWNLOAD VIDEO
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
        
        print ("Sent video!")
        return "File", file_path


    def do_image(self, submission, url):

        print("Submission type: image")
        file_type  = url.rsplit(".")[-1]
        file_path  = '%s/downloaded/image_%s.%s' %(self.path, submission.id, file_type)

        if not os.path.isfile(file_path):
            # CREATE IMAGE
            with open(file_path, "wb") as f:
                r = requests.get(url)
                f.write(r.content)

        print ("Sent image!")
        return "File", file_path


    def do_gallery(self, submission, url):

        print("Submission type: gallery")
        file_path  = '%s/downloaded/images_%s.zip' %(self.path, submission.id)

        if not os.path.isfile(file_path):
            # CREATE ARCHIVE
            ind = 0
            for i in submission.media_metadata.items():
                url       = i[1]['p'][0]['u'].split("?")[0].replace("preview", "i")
                file_type = url.rsplit(".")[-1]
                r         = requests.get(url)
                with open("%s/gallery/image_%s.%s" %(self.path, ind, file_type), "wb") as f:
                    f.write(r.content)
                ind += 1
            f = make_archive('%s/downloaded/images_%s'%(self.path, submission.id), 'zip', root_dir='%s/gallery' %(self.path))

        print ("Sent zip archive!")
        return "File", file_path
