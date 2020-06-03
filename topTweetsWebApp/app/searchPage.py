from flask import render_template, request
from app import app

from getTopTweets import getTopTweets
import datetime as dt

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    searchQuery = request.form.get("search")

    print(searchQuery)

    start = dt.datetime.now() - dt.timedelta(days=1)
    startDate = start.strftime('%Y-%m-%d')
    endDate = dt.datetime.utcnow().strftime('%Y-%m-%d')

    df, profileInformation = getTopTweets(searchQuery, startDate, endDate, noTopTweets=5)

    # Get top tweets in the required formsat
    tweetsList = []
    for i, row in df.iterrows():
        d = {}
        # d['name'] = row['username']
        # d['username'] = "@"+row['username']
        d['date'] = row['formatted_date']
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

    return render_template('indexResult.html', tweets=tweetsList,
        profileUserName = profileUserName, profileName = profileName,
        profilePhotoLink= profilePhotoLink, searchQuery=searchQuery)