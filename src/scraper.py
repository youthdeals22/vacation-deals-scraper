# src/scraper.py - ROBOT B - SMART SCRAPER

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os
import random
import undetected_chromedriver as uc

class SmartScraper:
    """
    ROBOT B: Scrapet AUTOMATISCH met geleerde selectors van Robot A
    """
    
    def __init__(self, website_name, training_data):
        self.website_name = website_name
        self.training_data = training_data
        self.selectors = training_data.get('selectors', [])
        self.deals = []
        self.driver = None
        
    def start_scraping(self, url):
        """Open website en extract data"""
        print(f"\n🤖 ROBOT B ACTIVATED - Scraping {self.website_name}...")
        print(f"📍 URL: {url}\n")
        
        try:
            options = Options()
            options.add_argument("--start-maximized")
            
            self.driver = uc.Chrome(options=options)
            self.driver.get(url)
            time.sleep(5)
            
            return self.driver
            
        except Exception as e:
            print(f"❌ FOUT: {str(e)}")
            return None
    
    def extract_deals(self):
        """Extract alle deals van de pagina"""
        print("🔍 Extracting deals...\n")
        
        try:
            # Get HTML
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Gebruik geleerde selectors van Robot A
            if self.selectors:
                selector = self.selectors[0]['selectors'][0]
                print(f"📌 Using selector: {selector}")
                
                elements = soup.select(selector)
                print(f"✅ Found {len(elements)} elements\n")
                
                for i, element in enumerate(elements[:10]):  # Eerste 10
                    deal = self._parse_element(element)
                    if deal:
                        self.deals.append(deal)
                        print(f"{i+1}. {deal['name'][:50]} - €{deal.get('price', 'N/A')}")
            
            return self.deals
            
        except Exception as e:
            print(f"❌ Extract error: {str(e)}")
            return []
    
    def _parse_element(self, element):
        """Parse één element"""
        try:
            # Probeer data uit element te halen
            deal = {
                'name': element.get_text(strip=True)[:100],
                'html': str(element)[:500],
                'timestamp': datetime.now().isoformat(),
                'source': self.website_name
            }
            
            # Probeer prijs te vinden
            price_text = element.get_text()
            import re
            price_match = re.search(r'€(\d+(?:[.,]\d{2})?)', price_text)
            if price_match:
                deal['price'] = float(price_match.group(1).replace(',', '.'))
            
            return deal
            
        except:
            return None
    
    def save_results(self):
        """Sla resultaten op"""
        if len(self.deals) == 0:
            print("❌ Geen deals gevonden!")
            return
        
        os.makedirs('data', exist_ok=True)
        
        results = {
            'website': self.website_name,
            'timestamp': datetime.now().isoformat(),
            'deals_found': len(self.deals),
            'deals': self.deals
        }
        
        fname = f"data/{self.website_name}_results.json"
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Results saved: {fname}")
        print(f"📊 Total deals: {len(self.deals)}")
        
        return results
    
    def stop(self):
        """Stop"""
        try:
            self.driver.quit()
        except:
            pass


if __name__ == '__main__':
    
    print("""
    ╔════════════════════════════════════════════╗
    ║  ROBOT B - SMART SCRAPER                  ║
    ║  (Uses training data from Robot A)        ║
    ╚════════════════════════════════════════════╝
    """)
    
    # Load training data from Robot A
    try:
        with open('data/vakantiediscounter_training.json', 'r', encoding='utf-8') as f:
            training_data = json.load(f)
    except:
        print("❌ Training data not found!")
        print("💡 Run Robot A first: python src/recorder.py")
        exit(1)
    
    # Start scraping
    url = "https://www.vakantiediscounter.nl/zoekresultaten?countrycode=BG%7ECY%7EGR%7EIT%7EHR%7EPT%7EES%7ETR%7EAL&departuredatestart=2026-06-22&holidaytype=all&page=1&room=2_0_0&sort=price_asc&transporttype=VL&trip_duration=8&trip_duration_range=6-10&arrivaldateend=2026-08-31&departureairport=AMS%7EEIN%7ERTM&region=adriatische_kust%7Ealgarve%7Eantalya%7Ebalearen%7Ecanarische_eilanden%7Ecorfu%7Ecosta_barcelona%7Ecosta_blanca%7Ecosta_brava%7Ecosta_dorada%7Ecosta_del_sol%7Edubrovnik_neretva%7Efamagusta%7Egran_canaria%7Ehvar%7Eibiza%7Eionische_eilanden%7Eistrie%7Ekos%7Ekreta%7Emallorca%7Emykonos%7Eqarku_i_durresit%7Eqarku_i_elbasanit%7Eqarku_i_tiranes%7Eqarku_i_vlores%7Eregio_valencia%7Erhodos%7Esantorini%7Esplit_dalmatie%7Eturkse_riviera%7Ezakynthos%7Ezuid_egeische_eilanden%7Ezuid_egeische_kust%7Ezadar&rating=7&stars=2%7E3%7E4%7E5"
    
    scraper = SmartScraper('vakantiediscounter', training_data)
    browser = scraper.start_scraping(url)
    
    if browser is None:
        print("❌ Scraper failed!")
        exit(1)
    
    # Extract
    time.sleep(3)
    scraper.extract_deals()
    
    # Save
    scraper.save_results()
    
    # Stop
    scraper.stop()
    
    print("\n✅ ROBOT B DONE!")
