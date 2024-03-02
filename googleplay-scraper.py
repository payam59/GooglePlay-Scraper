import argparse
import re
from google_play_scraper import Sort, reviews_all
from urllib.parse import urlparse, parse_qs

def extract_package_name(url):
    """Extracts the package name from the Google Play Store URL, removing unnecessary parameters."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    package_name = query_params.get("id", [None])[0]
    if package_name:
        return package_name
    else:
        raise ValueError("Invalid URL. Could not extract package name.")

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
                # Fetch the review date. The actual field name depends on the library's return structure. It might be 'at', 'date', 'timestamp', etc.
                review_date = review.get('at')  # Assuming 'at' is the field for the review date/timestamp
                
                if content is None or review_date is None:
                    print("Warning: Found a review without content or date. Skipping...")
                    continue
                
                # Format the review date if necessary. For example, if 'review_date' is a datetime object, you can format it as a string.
                # review_date_str = review_date.strftime('%Y-%m-%d %H:%M:%S')  # Uncomment and adjust format as needed
                
                # Write both review content and date to the file. Adjust the formatting to your preference.
                file.write(f"Date: {review_date}\n{content}\n\n")  # Use review_date_str if you formatted the date
                
        print(f"Successfully saved {len(reviews)} comments to {file_name}")
    except Exception as e:
        print(f"An error occurred while saving comments: {e}")


def main():
    parser = argparse.ArgumentParser(description="Download comments from a Google Play Store app URL.")
    parser.add_argument("url", nargs='?', help="The Google Play Store URL of the app.")

    args = parser.parse_args()
    
    if args.url:
        try:
            app_package = extract_package_name(args.url)
            save_comments_to_file(app_package)
        except Exception as e:  # Catching a broader range of exceptions to capture and display any error.
            print(f"Error: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
