from pathlib import Path
from pathlib import Path
import datetime as dt
from jinja2 import Environment, FileSystemLoader

from getTopTweets import getTopTweets

from emailFunc import send_email


# Function to get top tweets for a particular search query (username)
# Calls getTopTweets to get tweets and packs them into usable format
def getResult(searchQuery, noTopTweets=3):

    start = dt.datetime.now() - dt.timedelta(days=3)
    startDate = start.strftime('%Y-%m-%d')
    endDate = dt.datetime.utcnow().strftime('%Y-%m-%d')

    df, profileInformation = getTopTweets(searchQuery, startDate, endDate,
                                          noTopTweets)

    # Get top tweets in the required formsat
    tweetsList = []
    for i, row in df.iterrows():
        d = {}
        # d['name'] = row['username']
        # d['username'] = "@"+row['username']
        d['date'] = row['formatted_date'][3:-14]
        d['replies'] = row['replies']
        d['retweets'] = row['retweets']
        d['favorites'] = row['favorites']
        d['text'] = row['text']
        d['link'] = row['permalink']
        # d['hashtag'] = row['hashtags']
        # d['mentions'] = row['mentions']
        d['permalink'] = row['permalink']
        tweetsList.append(d)

    profileUserName = profileInformation["username"]
    profileName = profileInformation["name"]
    profilePhotoLink = profileInformation["profile_photo"]

    return tweetsList, profileUserName, profileName, profilePhotoLink

searchUser = input("Hello! This application will help you stay upto date with tweets of your Twitter celebrities in a short newsletter\n Enter Username of Twitter Account you wish to generate newsletter for:")
tweets, profileUserName, profileName, profilePhotoLink = getResult(
    searchUser, noTopTweets=5)

# Set up jinja templates

template_file = "newsletterContentTemplate.html"
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(template_file)
template_vars = {
    'tweets': tweets,
    'profileUserName': "@"+profileUserName,
    'profileName': profileName,
    'profilePhotoLink': profilePhotoLink
}

raw_html = template.render(template_vars)

out_file = Path.cwd() / 'finalEmail.html'
out_file.write_text(raw_html)

# Send Email
today = dt.datetime.now()
send_email("Top Tweets for Week of {}".format(profileName), raw_html, "soham.pachpande@gmail.com")
