import argparse
import re
from google_play_scraper import Sort, reviews_all, app, reviews
from urllib.parse import urlparse, parse_qs
import time
from google_play_scraper import Sort, reviews
import logging
import json
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            # Format datetime object as a string in the desired format
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
        
        
def fetch_reviews_in_batches(app_package , lang='en', country='us', sort=Sort.NEWEST, batch_size=100, max_reviews=None):
    all_reviews = []
    token = None  # Initialize the continuation token
    total_fetched = 0

    while True:
        logging.info(f"Fetching batch: token={token}")
        batch_reviews, new_token = reviews(
            app_package,
            continuation_token=token,  # Use the current token
            count=batch_size,
            sort=sort,
            country='ca',
            lang='en'
        )
        
        logging.info(f"Fetched {len(batch_reviews)} reviews. New token: {new_token}")

        if not batch_reviews:
            logging.info("No more reviews to fetch.")
            break

        all_reviews.extend(batch_reviews)
        total_fetched += len(batch_reviews)
        logging.info(f"Total fetched: {total_fetched}.")

        if new_token == token or not new_token:
            logging.info("No new continuation token. Ending fetch.")
            break
        else:
            token = new_token

        if max_reviews and total_fetched >= max_reviews:
            logging.info(f"Reached the maximum review limit of {max_reviews}.")
            break

    return all_reviews
    
    
def get_total_reviews_count(app_package):
    try:
        app_info = app(
            app_package
        )
        total_reviews = app_info['reviews']
        return total_reviews
    except Exception as e:
        print(f"An error occurred while fetching app details: {e}")
        return None
        
        
def is_valid_url(url):
    """Check if the given string is a valid URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def extract_package_name(argument):
    """Extracts the package name from either a Google Play Store URL or a direct package name."""
    if is_valid_url(argument):
        parsed_url = urlparse(argument)
        query_params = parse_qs(parsed_url.query)
        package_name = query_params.get("id", [None])[0]
        if package_name:
            return package_name
        else:
            raise ValueError("Invalid URL. Could not extract package name.")
    else:
        # Assume the argument is a package name if it's not a valid URL
        return argument

def save_comments_to_file(app_package):
    if app_package is None:
        raise ValueError("App package name is None. Cannot proceed with fetching comments.")

    file_name = f"{app_package}_comments.txt"
    if not isinstance(file_name, str):
        raise TypeError(f"File name resolved to a non-string type: {type(file_name)}")

    try:
        reviews = reviews_all(
            app_package,
            sleep_milliseconds=100,  # Adjust as necessary
            sort=Sort.NEWEST,  # Sort by newest
            lang='en',  # Language
            country='us'  # Country
        )

        if not reviews:
            print(f"No reviews found for {app_package}.")
            return

        with open(file_name, 'w', encoding='utf-8') as file:
            for review in reviews:
                content = review.get('content')
                review_date = review.get('at')  # Extracting the review date/timestamp
                score = review.get('score')  # Extracting the star rating
                reply_content = review.get('replyContent', "No reply")
                replied_at = review.get('repliedAt')  # Extracting the reply date/timestamp

                # Format the datetime objects as strings
                review_date_str = review_date.strftime('%Y-%m-%d %H:%M:%S') if review_date else "No date provided"
                replied_at_str = replied_at.strftime('%Y-%m-%d %H:%M:%S') if replied_at else "No reply date"

                if content is None or review_date is None:
                    print("Warning: Found a review without content or date. Skipping...")
                    continue

                # Write review date, star rating, content, and optionally reply content and date to the file
                file.write(f"Date: {review_date_str}\nRating: {score} stars\n{content}\n")
                if reply_content and replied_at:
                    file.write(f"Reply Date: {replied_at_str}\nReply: {reply_content}\n")
                file.write("\n\n")
                
        print(f"Successfully saved {len(reviews)} comments to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving comments: {e}")


def save_comments_to_file1(app_package,reviews):
    if app_package is None:
        raise ValueError("App package name is None. Cannot proceed with fetching comments.")

    file_name = f"{app_package}_comments.txt"
    if not isinstance(file_name, str):
        raise TypeError(f"File name resolved to a non-string type: {type(file_name)}")

    try:

        with open(file_name, 'w', encoding='utf-8') as file:
            for review in reviews:
                content = review.get('content')
                review_date = review.get('at')  # Extracting the review date/timestamp
                score = review.get('score')  # Extracting the star rating
                reply_content = review.get('replyContent', "No reply")
                replied_at = review.get('repliedAt')  # Extracting the reply date/timestamp

                # Format the datetime objects as strings
                review_date_str = review_date.strftime('%Y-%m-%d %H:%M:%S') if review_date else "No date provided"
                replied_at_str = replied_at.strftime('%Y-%m-%d %H:%M:%S') if replied_at else "No reply date"

                if content is None or review_date is None:
                    print("Warning: Found a review without content or date. Skipping...")
                    continue

                # Write review date, star rating, content, and optionally reply content and date to the file
                file.write(f"Date: {review_date_str}\nRating: {score} stars\n{content}\n")
                if reply_content and replied_at:
                    file.write(f"Reply Date: {replied_at_str}\nReply: {reply_content}\n")
                file.write("\n\n")
                
        print(f"Successfully saved {len(reviews)} comments to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving comments: {e}")
        

def get_all_reviews_and_save(package_name, num):
    if not package_name:
        raise ValueError("App package name is None. Cannot proceed with fetching comments.")

    file_name = f"{package_name}_comments.txt"
    
    # Fetch reviews
    result, continuation_token = reviews(
        package_name,
        lang='en',  # Language
        country='us',  # Country
        sort=Sort.RATING,  # Sort by rating
        count=num  # Number of reviews to fetch
    )

    # Save to file
    with open(file_name, 'w', encoding='utf-8') as f:
        for review in result:
            # Use the custom JSON encoder for datetime objects
            f.write(json.dumps(review, ensure_ascii=False, cls=DateTimeEncoder) + '\n')

    print(f"Successfully saved comments to {file_name}")
        
        
def main():
    parser = argparse.ArgumentParser(description="Download comments from a Google Play Store app URL or by package name.")
    parser.add_argument("input", nargs='?', help="The Google Play Store URL or the app package name.")
    args = parser.parse_args()
    
    
    # Setup basic logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    if args.input:
        try:
            app_package = extract_package_name(args.input)
            total_reviews = get_total_reviews_count(app_package)
            if total_reviews is not None:
                print(f"Total reviews for {app_package}: {total_reviews}")
            else:
                print("Failed to fetch total reviews count.")
            #reviews = fetch_reviews_in_batches(app_package, batch_size=1000, max_reviews=50000)
            #save_comments_to_file1(app_package, reviews)
            #save_comments_to_file(app_package)
            get_all_reviews_and_save(app_package,total_reviews)
            
        except Exception as e:
            print(f"Error: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()