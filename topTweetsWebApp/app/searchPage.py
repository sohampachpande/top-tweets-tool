from flask import render_template, request
from app import app
from getTopTweets import getTopTweets


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    searchQuery = request.form.get("search")
    startDate = "2020-05-17"
    endDate = "2020-05-25"

    df = getTopTweets(searchQuery, startDate, endDate, noTopTweets=5)

    # Get top tweets in the required format
    tweetsList = []
    for i, row in df.iterrows():
        d = {}
        d['name'] = row['username']
        d['username'] = "@"+row['username']
        d['date'] = row['formatted_date']
        d['replies'] = row['replies']
        d['retweets'] = row['retweets']
        d['favorites'] = row['favorites']
        d['text'] = row['text']
        d['link'] = row['permalink']
        # d['hashtag'] = row['hashtags']
        # d['mentions'] = row['mentions']
        tweetsList.append(d)

    return render_template('indexResult.html', tweets=tweetsList, searchQuery=searchQuery)