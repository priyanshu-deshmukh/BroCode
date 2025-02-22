import requests
from sklearn.feature_extraction.text import TfidfVectorizer
def fetch_top_posts(subreddit, limit=10):
    url = f'https://www.reddit.com/r/{subreddit}/top.json'
    params = {'limit': limit}
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    posts = response.json()['data']['children']
    a = []
    for post in posts:
        data = post['data']
        a.append([data["title"],data.get('selftext', 'No text content')[:60] + "..."])
        # print(f"Title: {data['title']}")
        # print(f"Author: {data['author']}")
        # print(f"Score: {data['score']}")
        # print(f"URL: {data['url']}")
        # print(f"Content: {data.get('selftext', 'No text content')}\n")
    return a

if __name__ == '__main__':

    posts = fetch_top_posts('india', 10)
    corpus = [post[0] + " " + post[1] for post in posts]  # Combining title and snippet
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    keywords = vectorizer.get_feature_names_out()


    print("Top Keywords:", keywords)
