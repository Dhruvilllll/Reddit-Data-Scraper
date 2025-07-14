
import os
import praw
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm


load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


def fetch_user_content(username: str, limit: int = 100):
    """
    Fetches latest posts and comments by a Reddit user.

    Args:
        username (str): Reddit username (no 'u/' prefix)
        limit (int): Number of posts/comments to fetch

    Returns:
        Tuple: (posts, comments)
    """
    user = reddit.redditor(username)
    posts, comments = [], []

    print(f"\n🔍 Scraping content for u/{username} ...\n")

    try:
        for comment in tqdm(user.comments.new(limit=limit), desc="📩 Comments"):
            comments.append({
                "subreddit": str(comment.subreddit),
                "body": comment.body,
                "url": f"https://www.reddit.com{comment.permalink}"
            })
    except Exception as e:
        print(f"⚠️ Error fetching comments: {e}")

    try:
        for post in tqdm(user.submissions.new(limit=limit), desc="📝 Posts"):
            posts.append({
                "subreddit": str(post.subreddit),
                "title": post.title,
                "selftext": post.selftext,
                "url": f"https://www.reddit.com{post.permalink}"
            })
    except Exception as e:
        print(f"⚠️ Error fetching posts: {e}")

    return posts, comments


def save_to_file(username: str, posts: list, comments: list):
    """
    Saves fetched content to a raw text file for LLM processing.

    Args:
        username (str): Reddit username
        posts (list): List of post dictionaries
        comments (list): List of comment dictionaries
    """
    Path("raw_data").mkdir(exist_ok=True)
    filename = f"raw_data/{username}_raw.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"=== POSTS by u/{username} ===\n\n")
        for p in posts:
            f.write(f"[{p['subreddit']}] {p['title']}\n")
            if p['selftext'].strip():
                f.write(f"Body: {p['selftext']}\n")
            f.write(f"URL: {p['url']}\n\n")

        f.write(f"\n=== COMMENTS by u/{username} ===\n\n")
        for c in comments:
            f.write(f"[{c['subreddit']}] {c['body']}\n")
            f.write(f"URL: {c['url']}\n\n")

    print(f"\n✅ Raw data saved to: {filename}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Reddit User Scraper")
    parser.add_argument("username", type=str, help="Reddit username (no 'u/' prefix)")
    parser.add_argument("--limit", type=int, default=100, help="Number of posts/comments to fetch")
    args = parser.parse_args()

    posts, comments = fetch_user_content(args.username, args.limit)
    save_to_file(args.username, posts, comments)
