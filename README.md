# Google Play Store Comments Scraper

This Python script allows you to download and save comments from a Google Play Store app page to a text file. It's designed to extract comments based on the app's URL provided as an argument.

## Installation

Before running the script, you need to ensure Python is installed on your system. This script has been tested with Python 3.8 and above.

1. **Clone the repository**:

```bash
git clone https://github.com/payam59/GooglePlay-Scraper.git
cd GooglePlay-Scraper
```

2. **Set up a virtual environment** (optional but recommended):

```bash
python -m venv venv
```

- On Windows, activate the virtual environment:

```bash
venv\Scripts\activate
```

- On macOS and Linux:

```bash
source venv/bin/activate
```

3. **Install required packages**:

```bash
pip install google-play-scraper
```

## Usage

Run the script by providing the Google Play Store URL of the app as an argument. The script extracts the app's package name from the URL and downloads all available comments, saving them to a text file named `<package_name>_comments.txt`.

```bash
python googleplay-scraper.py "https://play.google.com/store/apps/details?id=com.example"
```

### Arguments

- `url`: The Google Play Store URL of the app you want to scrape comments from.

### Output

The script saves the comments to a text file in the current directory, named using the app's package name followed by `_comments.txt`. If no comments are found or an error occurs, the script will print a relevant message to the console.

## Troubleshooting

If you encounter any issues related to rate limiting or no comments being saved, ensure that the URL is correctly formatted and points to a valid Google Play Store app page. Adjusting the `sleep_milliseconds` parameter in the script can help avoid rate limiting by Google.

## Contributing

Contributions to improve the script or fix issues are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more details.
