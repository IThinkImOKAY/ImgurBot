import os, time, praw, emoji, config, random, pyimgur, requests, traceback, webbrowser

reddit = praw.Reddit(client_id=config.c_id,
                     client_secret=config.c_s,
                     user_agent=config.u_a)

while True:
    try:
        subreddit = reddit.subreddit(random.choice(config.subs))
        print('Random Subreddit Is:',subreddit)
        submissions = list(subreddit.top('all', limit=1000))
        submission = random.choice(submissions)
        if submission.domain in config.domains and '.gifv' not in submission.url:
            no_emoji = str(emoji.demojize(submission.title))
            print('Imgur/Reddit Domain!')
            file_name = submission.url.replace('https://i.imgur.com/','').replace('https://i.redd.it/','')
            response = requests.get(submission.url)
            file = open(file_name, "wb")
            file.write(response.content)
            file.close()
            print('Downloaded Image')
            try:
                with open('tokens.txt') as f:
                    access_token, refresh_token = f.read().strip().split()
                im = pyimgur.Imgur(config.i_id, access_token=access_token, refresh_token=refresh_token)
            except FileNotFoundError:
                im = pyimgur.Imgur(config.i_id)
                webbrowser.open(im.authorization_url('pin'))
                pin = input("What's the pin?: ")
                access_token, refresh_token = im.exchange_pin(pin)
                with open('tokens.txt', 'w') as f:
                    f.write(f'{access_token} {refresh_token}')
            im.upload_image(file_name).submit_to_gallery(title=no_emoji)
            print('Uploaded To Gallery')
            with open("ids.txt", "r") as file:
              f.write(submission.id)
            os.remove(file_name)
            print('Deleted File')
            time.sleep(300)
        else:
            print('Submission Not Actionable :(')
            time.sleep(60)
    except Exception:
        print(traceback.format_exc())
        time.sleep(60)     
    except KeyboardInterrupt:
        print('Shutting Down :(')
        quit()
