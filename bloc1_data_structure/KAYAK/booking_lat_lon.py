import os
import sys
import json
import subprocess
from collections import defaultdict
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime, timedelta
from scrapy_playwright.page import PageMethod
from time import sleep
 

class BookingSpider(scrapy.Spider):
    name = "booking"
    
    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {"headless": True},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': 5000,  # 5 secondes
        'DOWNLOAD_DELAY': 2.0,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 3,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 10,
    }

    def __init__(self, villes=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.villes = villes or []
        self.max_per_city = 20
        self.saved_count_by_city = defaultdict(int)
        self.items_by_city = defaultdict(list)

    def start_requests(self):
        today = datetime.now()
        start_date = (today + timedelta(days=3)).strftime('%Y-%m-%d')
        end_date = (today + timedelta(days=10)).strftime('%Y-%m-%d')
        for v in self.villes:
            city = v["nom"]
            lat = v["latitude"]
            lon = v["longitude"]
            ville_id = v.get("ville_id")

            url = f'https://www.booking.com/searchresults.fr.html??ssne=&ssne_untouched=&ss=&latitude={lat}&longitude={lon}&order=review_score_and_price&&nflt=price%3DEUR-100-200-1%3Bht_id%3D204&checkin={start_date}&checkout={end_date}'
            self.logger.info(f"🌍 Recherche lancée pour {city} (latitude:{lat}, longitude:{lon}) → {url}")

            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={
                    'city': city,
                    'latitude': lat,
                    'longitude': lon,
                    'ville_id': ville_id,
                    'playwright': True,
                    'playwright_page_methods': [
                        PageMethod('wait_for_selector', 'div[data-testid="property-card"]'),
                        PageMethod('mouse.move', x=100, y=100),
                        PageMethod('evaluate', """
                            async () => {
                                let previousHeight = 0;
                                for (let i = 0; i < 2; i++) {
                                    window.scrollTo(0, document.body.scrollHeight);
                                    await new Promise(r => setTimeout(r, 1500));
                                    let newHeight = document.body.scrollHeight;
                                    if (newHeight === previousHeight) break;
                                    previousHeight = newHeight;
                                }
                            }
                        """),
                        PageMethod('wait_for_timeout', 1500)
                    ]
                }
            )

    def parse(self, response):
        city = response.meta['city']
        ville_id = response.meta.get('ville_id')
        hotels = response.xpath('//div[contains(@data-testid, "property-card")]')
        self.logger.info(f"🏨 {city}: {len(hotels)} hôtels trouvés")
        for i,list_hotel in enumerate(hotels):
            name = list_hotel.xpath('.//div[@data-testid="title"]/text()').get()
            name = name.strip() if name else None
            url = list_hotel.xpath('.//a[@data-testid="title-link"]/@href').get()
            rating = list_hotel.xpath('.//div[@data-testid="review-score"]/div/text()').get()
            price = list_hotel.xpath('.//span[@data-testid="price-and-discounted-price"]/text()').get()
            if url:
                url = response.urljoin(url)
                yield response.follow(
                    url, self.parse_hotel,
                    meta={'name': name, 'rating': rating, 'city': city, 'playwright': True, 'prix': price,'ville_id': ville_id,
                        'playwright_page_methods': [PageMethod('wait_for_timeout', 1500)]}
                )

    def parse_hotel(self, response):
        name = response.meta['name']
        rating = response.meta['rating']
        city = response.meta['city']
        prix = response.meta['prix']
        ville_id = response.meta.get('ville_id')

        if self.saved_count_by_city[city] >= self.max_per_city:
            return
        
        gps = response.xpath('//a[@id="map_trigger_header"]/@data-atlas-latlng').get()
        latitude, longitude = gps.split(',') if gps else (None, None)
        description = response.xpath('//p[@data-testid="property-description"]/text()').get()

        self.logger.info(f"✅ Hôtel sauvegardé: {name} ({city})")
        
        self.items_by_city[city].append({
            'ville': city,
            'name': name,
            'description': description,
            'url': response.url,
            'rating': rating,
            'latitude': latitude,
            'longitude': longitude,
            'prix':prix,
            'ville_id': ville_id, 
        })
        self.saved_count_by_city[city] += 1    

    def closed(self, reason):
        """Sauvegarde des résultats en JSON par ville"""
        output_dir = "booking_results"
        os.makedirs(output_dir, exist_ok=True)

        for city, items in self.items_by_city.items():
            items = items[:20]
            filename = os.path.join(output_dir, f"results_{city.lower().replace(' ', '_')}.json")
            with open(filename, "w", encoding="utf-8") as f:
                serializable_items = []
                for item in items:
                    serializable_item = {}
                    for key, value in item.items():
                        if hasattr(value, 'get'):  # Si c'est un objet Selector
                            serializable_item[key] = value.get()  # Extraire la valeur
                        else:
                            serializable_item[key] = value
                    serializable_items.append(serializable_item)

                json.dump(serializable_items, f, ensure_ascii=False, indent=4)
            self.logger.info(f"Résultats sauvegardés dans {filename}")

if __name__ == "__main__":
    # Vérifie qu'un fichier JSON est passé
    if len(sys.argv) < 2:
        print("Erreur Utilisation : python booking_lat_lon.py villes.json")
        sys.exit(1)

    # Charger la liste des villes depuis le fichier JSON
    json_path = sys.argv[1]
    with open(json_path, "r", encoding="utf-8") as f:
        villes = json.load(f)

    BATCH_SIZE = 1
    PAUSE_BATCH = 2  # secondes

    # Exécuter les lots un par un
    for i in range(0, len(villes), BATCH_SIZE):
        batch = villes[i:i+BATCH_SIZE]
        print(f"\n🚀 Lancement batch {i//BATCH_SIZE + 1}: {[v['nom'] for v in batch]}\n")

        process = CrawlerProcess()
        process.crawl(BookingSpider, villes=batch)
        process.start()

        # Pause avant la prochaine série
        if i + BATCH_SIZE < len(villes):
            print(f"Pause {PAUSE_BATCH}s avant le prochain batch...")
            sleep(PAUSE_BATCH)