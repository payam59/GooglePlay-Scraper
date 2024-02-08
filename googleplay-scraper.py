import argparse
import re
from google_play_scraper import Sort, reviews_all

def extract_package_name(url):
    """Extracts the package name from the Google Play Store URL."""
    match = re.search(r'id=([a-zA-Z0-9_.]+)', url)
    if match:
        return match.group(1)
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
                if content is None:
                    print("Warning: Found a review without content. Skipping...")
                    continue
                file.write(content + '\n\n')
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
