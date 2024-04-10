from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_latest_stories():
    url = "https://time.com"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch Time.com. Status code: {response.status_code}")
        return []

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    latest_stories = []
    story_elements = soup.find_all('main', class_='homepage-wrapper')
    if not story_elements:
        print("No story elements found")
    else:
        for story in story_elements[0].find_all('li')[:6]:  # Adjusted to select list items within the first ul
            title_elem = story.find('a', class_='headline')  # Finding the title element
            if title_elem:
                title = title_elem.text.strip()  # Extracting the title text and removing leading/trailing whitespace
                link = title_elem['href']  # Extracting the href attribute for the link
                latest_stories.append({"title": title, "link": link})

    return latest_stories

@app.route("/getTimeStories")
def get_time_stories():
    latest_stories = fetch_latest_stories()
    return jsonify(latest_stories)

if __name__ == "__main__":
    app.run(debug=True)



