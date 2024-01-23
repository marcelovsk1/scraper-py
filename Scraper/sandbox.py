import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scroll_to_bottom(driver, max_clicks=3):
    for _ in range(max_clicks):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

def scrape_events(driver, url, selectors):
    driver.get(url)
    driver.implicitly_wait(10)
    scroll_to_bottom(driver)

    page_content = driver.page_source
    webpage = BeautifulSoup(page_content, 'html.parser')

    events = webpage.find_all(selectors['event']['tag'], class_=selectors['event']['class'])

    event_list = []

    for event in events:
        event_info = {}
        for key, selector in selectors['selectors'].items():
            element = event.find(**selector)
            event_info[key] = element.text.strip() if element else None

        event_list.append(event_info)

    return event_list

def main():
    sources = [
        {
            'name': 'Facebook',
            'url': 'https://www.facebook.com/events/explore/montreal-quebec/102184499823699/',
            'selectors': {
                'event': {'tag': 'div', 'class': 'ph5 pb3'},
                'selectors': {
                    'Event': {'tag': 'span', 'class': 'a-l-k ph5'},
                    'Date': {'tag': 'div', 'class': 'a-l-k-1 ph5'},
                    'Location': {'tag': 'span', 'class': 'a-l-k-2 ph5'},
                    'Image URL': {'tag': 'img', 'class': 'a-l-k-3 x1rg5ohu'}
                }
            }
        },
        {
            'name': 'Ticketmaster',
            'url': 'https://www.ticketmaster.ca/discover/concerts/montreal',
            'selectors': {
                'event': {'tag': 'div', 'class': 'flex flex-wrap items-stretch'},
                'selectors': {
                    'Event': {'tag': 'div', 'class': 'sc-cPZqLP kFZJPH'},
                    'Date': {'tag': 'div', 'class': 'sc-fAUrTm cmvptJ'},
                    'Location': {'tag': 'div', 'class': 'sc-cpISQd dtbdEy'},
                    'Image URL': {'tag': 'img', 'class': 'sc-ebFjAB ciZrVm'}
                }
            }
        },
        {
            'name': 'Eventbrite',
            'url': 'https://www.eventbrite.com/d/canada--montreal/events/',
            'selectors': {
                'event': {'tag': 'div', 'class': 'eds-media-card-content eds-media-card-content--event'},
                'selectors': {
                    'Event': {'tag': 'h2', 'class': 'eds-media-card-content__title'},
                    'Date': {'tag': 'p', 'class': 'eds-media-card-content__sub-title'},
                    'Location': {'tag': 'div', 'class': 'location-wrapper'},
                    'Image URL': {'tag': 'a', 'class': 'eds-media-card-content__image'}
                }
            }
        }
    ]

    all_events = []

    for source in sources:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        events = scrape_events(driver, source['url'], source['selectors'])
        driver.quit()

        source_data = {
            'source_name': source['name'],
            'events': events
        }

        all_events.append(source_data)

    # Convert to JSON
    json_data = json.dumps(all_events, indent=2)

    print(json_data)

if __name__ == "__main__":
    main()
