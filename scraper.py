import pandas as pd
import requests
import os.path
from time import sleep

py = 'https://www.reddit.com/r/python.json'
r = 'https://www.reddit.com/r/Rlanguage.json'
posts_csv = 'posts.csv'


def scrape(url, csv):

    posts = []
    after = None
    csv = f'python_{csv}' if 'python' in url else f'r_{csv}'

    for i in range(4):
        if after and i == 1:
            url = f"{url}?after={after}"
        elif i > 1:
            url = f"{url[:url.index('?')]}?after={after}"

        res = requests.get(url, headers={'User-agent': 'Chrome'})
        print(url)

        if res.status_code != 200:
            print(f'Status Error: {res.status_code}')
            break

        res_dict = res.json()['data']['children']

        if os.path.isfile(csv):
            df = pd.read_csv(csv)
            for post in res_dict:
                if (
                    post['data']['id'] not in df['id']
                    and post['data']['selftext']
                    and not post['data']['stickied']
                ):
                    posts.append(post['data'])
            new_df = pd.DataFrame(posts)
            pd.concat([df, new_df], axis=0, sort=0).to_csv(csv, index=False)

        else:
            for post in res_dict:
                if post['data']['selftext'] and not post['data']['stickied']:
                    posts.append(post['data'])
            pd.DataFrame(posts).to_csv(csv, index=False)

        after = res.json()['data']['after']
        sleep(2)


scrape(py, posts_csv)
scrape(r, posts_csv)
