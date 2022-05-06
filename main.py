from email import header
import re
from flask import Flask ,jsonify,request
from storage import all_articles,liked_articles,not_liked_articles
from demographic_filtering import output
from content_filtering import get_recommendations

app=Flask(__name__)


@app.route("/get-article")
def get_article():
    return jsonify({
        "article": all_articles[0],
        "message":"success"
    },200)

@app.route("/liked-article",methods=["POST"])
def liked_article():
    article=all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "message":"success"
    },200)

app.route("/not-liked-article",methods=["POST"])
def not_liked_article():
    article=all_articles[0]
    not_liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "message":"success"
    },200)

@app.route("/popular-articles")
def popular_articles():
    article_data=[]
    for article in output:
        data={
            "title":article[1],
            "url":article[0],
            "text":article[2],
            "lang":article[3],
            "total_events":article[4]
        }
    article_data.append(data)
    return jsonify({
        "data":article_data,
        "message":"success"
    },200)

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended=[]
    for article in liked_articles:
        output=get_recommendations(article[13])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data=[]
    for recommended in all_recommended:
        data={
            "title":recommended[1],
            "url":recommended[0],
            "text":recommended[2],
            "lang":recommended[3],
            "total_events":recommended[4]
        }
    article_data.append(data)
    return jsonify({
        "data":article_data,
        "message":"success"
    },200)

if __name__ == "__main__":
    app.run()