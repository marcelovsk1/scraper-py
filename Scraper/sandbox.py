import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scroll_to_bottom(driver, max_clicks=3):
    for _ in range(max_clicks):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

def scrape_events(driver, url, event_selector, name_selector, date_selector, location_selector, image_selector):
    driver.get(url)
    driver.implicitly_wait(10)
    scroll_to_bottom(driver)

    page_content = driver.page_source
    webpage = BeautifulSoup(page_content, 'html.parser')

    events = webpage.find_all(event_selector)

    event_list = []

    for event in events:
        event_name = event.find(name_selector).text if event.find(name_selector) else None
        event_date = event.find(date_selector).text.strip() if event.find(date_selector) else None
        event_location_element = event.find(location_selector)
        event_location = event_location_element.text.strip() if event_location_element else None
        event_image = event.find(image_selector)
        image_url = event_image['src'] if event_image and 'src' in event_image.attrs else None

        event_data = {
            'Event': event_name,
            'Date': event_date,
            'Location': event_location,
            'image_url': image_url
        }

        event_list.append(event_data)

    return event_list

def main():
    sources = [
        {
            'name': 'Facebook',
            'url': 'https://www.facebook.com/events/explore/montreal-quebec/102184499823699/',
            'event_selector': 'div.x78zum5.x1n2onr6.xh8yej3',
            'name_selector': 'span.x4k7w5x.x1h91t0o.x1h9r5lt.x1jfb8zj.xv2umb2.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1qrby5j',
            'date_selector': 'div.xu06os2.x1ok221b',
            'location_selector': 'span.x4k7w5x.x1h91t0o.x1h9r5lt.x1jfb8zj.xv2umb2.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1qrby5j',
            'image_selector': 'img.x1rg5ohu.x5yr21d.xl1xv1r.xh8yej3'
        },
        {
            'name': 'Ticketmaster',
            'url': 'https://www.ticketmaster.ca/discover/concerts/montreal',
            'event_selector': 'div.Flex-sc-145abwg-0.bWTqsV.accordion__item.event-listing__item',
            'name_selector': 'div.sc-fFeiMQ.bCvzDL.text.text--dark.text--primary.sc-6jnhqk-0.kGOLzf.event-tile__title',
            'date_selector': 'div.sc-fFeiMQ.dBYlim.text.text--accent.text--accent01.text-tm.sc-17ev1tv-0.cnj20n-0.firocR.iZsGLV.event-tile__date-title',
            'location_selector': 'div.sc-fFeiMQ.iIgzpz.text.text--dark.text--secondary.sc-1s3i3gy-0.hbRPym.event-tile__sub-title',
            'image_selector': 'img.event-listing__thumbnail'
        },
        {
            'name': 'Eventbrite',
            'url': 'https://www.eventbrite.com/d/canada--montreal/events/',
            'event_selector': 'div.Stack_root__1ksk7',
            'name_selector': 'h2',
            'date_selector': 'p',
            'location_selector': 'p.Typography_root__487rx.#585163.Typography_body-md__487rx.event-card__clamp-line--one.Typography_align-match-parent__487rx',
            'image_selector': 'a.event-card-link'
        }
    ]

    all_events = []

    for source in sources:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        events = scrape_events(
            driver,
            source['url'],
            source['event_selector'],
            source['name_selector'],
            source['date_selector'],
            source['location_selector'],
            source['image_selector']
        )
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
