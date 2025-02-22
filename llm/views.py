from django.shortcuts import render,redirect,reverse
from .reddit_scraper import fetch_top_posts
from tavily import TavilyClient
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from .twitter import twitter_scrape
from asgiref.sync import async_to_sync
from sklearn.feature_extraction.text import TfidfVectorizer
from .csv_review import analyze_reviews
from dotenv import find_dotenv,load_dotenv
import os


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Load Auth0 application settings into memory
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

def llm_home(request):
    session = request.session.get("user")
    if session:
        return render(request,"llm/llm_home.html",
            context={"session": session})
    else:
        return render(request, "llm/llm_home.html",
                      context={})

def chatbot(request):
    session = request.session.get("user")
    if session:
        return render(request,"llm/chatbot.html",
            context={"session": session})
    else:
        return redirect(reverse("auth_0:login"))


def dashboard(request):
    session = request.session.get("user")
    if session:
        if request.method == "POST":
            query = request.POST.get("query")
            subreddit = request.POST.get("subreddit")
            nltk.download('vader_lexicon')

            reddit_posts = fetch_top_posts(subreddit)

            corpus = [post[0] + " " + post[1] for post in reddit_posts]
            vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
            tfidf_matrix = vectorizer.fit_transform(corpus)
            keywords = vectorizer.get_feature_names_out()

            twitter_posts = async_to_sync(twitter_scrape)(query)

            analyzer = SentimentIntensityAnalyzer()
            twitter_compound_scores = []
            # Analyze and print sentiment scores for each post
            for post in twitter_posts:
                scores = analyzer.polarity_scores(post)
                twitter_compound_scores.append(scores["compound"])
                print(f"Sentiment Scores: {scores}\n")

            return render(request, "llm/dashboard.html",
                          context={"session": session,"cs":twitter_compound_scores,
                                   "tp":zip(twitter_posts,twitter_compound_scores),
                                   "rp":reddit_posts,
                                   "tkey":keywords,
                                   }
                          )
        else:

            return render(request, "llm/dashboard.html",
                          context={"session": session})
    else:
        return redirect(reverse("auth_0:login"))

def search(request):
    session = request.session.get("user")
    if session:
        if request.method == "POST":
            query = request.POST.get("query")
            client = TavilyClient(api_key=TAVILY_API_KEY)
            response = client.search(
            query=query,
            search_depth = "advanced",
            time_range = "w",
            include_answer = "advanced",
            include_images = True,
            max_results=8,
            )

            combined_data = zip(response['results'],response['images'])
            answer = response["answer"]

            return render(request, "llm/search.html",
                      context={"session": session,"response":combined_data,"answer":answer})
        else:
            return render(request, "llm/search.html",
                          context={"session": session})
    else:
        return redirect(reverse("auth_0:login"))

def reputation(request):
    session = request.session.get("user")
    if session:
        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]
            results = analyze_reviews(csv_file)
            cs = list(results["sentiment_trend"]["sentiment_score"])



            return render(request, "llm/reputation.html",
                        context={"session": session, "results":results ,"cs":cs,
                                 "tkey":results["top_keywords"]})
        else:
            return render(request, "llm/reputation.html",
                          context={"session": session,})
    else:
        return redirect(reverse("auth_0:login"))

def contact(request):
    session = request.session.get("user")
    if session:
        return render(request, "llm/contact.html",
                      context={"session": session})
    else:
        return redirect(reverse("auth_0:login"))

def about(request):
    session = request.session.get("user")
    if session:
        return render(request, "llm/about.html",
                      context={"session": session})
    else:
        return redirect(reverse("auth_0:login"))

def profile(request):
    session = request.session.get("user")
    if session:
        return render(request, "llm/profile.html",
                      context={"session": session})
    else:
        return redirect(reverse("auth_0:login"))




