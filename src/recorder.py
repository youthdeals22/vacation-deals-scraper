# src/recorder.py - UNDETECTABLE VERSION

from selenium.webdriver.chrome.options import Options
import json
import time
from datetime import datetime
import os
import random
import undetected_chromedriver as uc

class ClickRecorder:
    """Undetectable - Chrome denkt je bent ECHT"""
    
    def __init__(self, website_url):
        self.url = website_url
        self.driver = None
        self.clicks = []
        
    def start_recording(self):
        """Open website - UNDETECTABLE"""
        print(f"\n🔴 RECORDING STARTED!")
        print(f"📍 Website: {self.url}")
        print(f"⏹️  Sluit browser als je klaar bent\n")
        
        try:
            options = Options()
            options.add_argument("--start-maximized")
            
            # Undetected Chrome (ECHTE browser voor Chrome!)
            self.driver = uc.Chrome(options=options)
            
            self.driver.get(self.url)
            time.sleep(5)
            
            # Wacht tot pagina geladen
            try:
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.common.by import By
                
                wait = WebDriverWait(self.driver, 10)
                # Wacht tot er IETS geladen is
                wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
            except:
                pass
            
            time.sleep(2)
            
            self._attach_click_listener()
            
            return self.driver
            
        except Exception as e:
            print(f"❌ FOUT: {str(e)}")
            print("💡 Zorg dat je dit installeert:")
            print("   pip install undetected-chromedriver")
            return None
    
    def _attach_click_listener(self):
        """Register clicks"""
        script = """
        window.recordedClicks = [];
        document.addEventListener('click', function(e) {
            let text = e.target.innerText || e.target.value || '';
            if (text.trim().length === 0) return;
            
            window.recordedClicks.push({
                text: text.substring(0, 100),
                tag: e.target.tagName,
                class: e.target.className,
                id: e.target.id
            });
            
            console.log('✅ Klik #' + window.recordedClicks.length);
        }, true);
        """
        
        try:
            self.driver.execute_script(script)
            print("✅ Klik listener ACTIEF!")
        except:
            pass
    
    def stop_recording(self):
        """Stop"""
        print("\n⏹️  Opslaan...")
        
        try:
            self.clicks = self.driver.execute_script(
                "return window.recordedClicks || []"
            )
        except:
            self.clicks = []
        
        print(f"✅ {len(self.clicks)} klikken geregistreerd!")
        
        try:
            self.driver.quit()
        except:
            pass
        
        return self.clicks
    
    def analyze_clicks(self):
        """Learn selectors"""
        if len(self.clicks) == 0:
            print("⚠️  Geen klikken!")
            return
        
        print("\n🧠 Selectoren leren...\n")
        
        selectors = []
        for i, click in enumerate(self.clicks):
            text = click['text'][:40] if click['text'] else 'Click'
            print(f"{i+1}. '{text}'")
            
            sel = []
            if click['class']:
                sel.append(f".{click['class'].split()[0]}")
            if click['id']:
                sel.append(f"#{click['id']}")
            sel.append(click['tag'].lower())
            
            sel = list(dict.fromkeys(sel))
            if sel:
                print(f"   → {sel[0]}")
            
            selectors.append({
                'text': click['text'],
                'selectors': sel[:2],
                'priority': i + 1
            })
        
        self.selectors = selectors
    
    def save_training_data(self, website_name):
        """Save"""
        if len(self.selectors) == 0:
            print("❌ Geen selectors!")
            return None
        
        os.makedirs('data', exist_ok=True)
        
        data = {
            'website': website_name,
            'timestamp': datetime.now().isoformat(),
            'clicks_count': len(self.clicks),
            'selectors_learned': len(self.selectors),
            'selectors': self.selectors,
        }
        
        fname = f"data/{website_name}_training.json"
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Opgeslagen: {fname}")
        return data


if __name__ == '__main__':
    
    print("""
    ╔════════════════════════════════════════════╗
    ║  ROBOT A - UNDETECTABLE RECORDER          ║
    ║  (Chrome denkt je bent ECHT!)             ║
    ╚════════════════════════════════════════════╝
    """)
    
    website = "https://www.vakantiediscounter.nl/zoekresultaten?countrycode=BG%7ECY%7EGR%7EIT%7EHR%7EPT%7EES%7ETR%7EAL&departuredatestart=2026-06-22&holidaytype=all&page=1&room=2_0_0&sort=price_asc&transporttype=VL&trip_duration=8&trip_duration_range=6-10&arrivaldateend=2026-08-31&departureairport=AMS%7EEIN%7ERTM&region=adriatische_kust%7Ealgarve%7Eantalya%7Ebalearen%7Ecanarische_eilanden%7Ecorfu%7Ecosta_barcelona%7Ecosta_blanca%7Ecosta_brava%7Ecosta_dorada%7Ecosta_del_sol%7Edubrovnik_neretva%7Efamagusta%7Egran_canaria%7Ehvar%7Eibiza%7Eionische_eilanden%7Eistrie%7Ekos%7Ekreta%7Emallorca%7Emykonos%7Eqarku_i_durresit%7Eqarku_i_elbasanit%7Eqarku_i_tiranes%7Eqarku_i_vlores%7Eregio_valencia%7Erhodos%7Esantorini%7Esplit_dalmatie%7Eturkse_riviera%7Ezakynthos%7Ezuid_egeische_eilanden%7Ezuid_egeische_kust%7Ezadar&rating=7&stars=2%7E3%7E4%7E5"
    
    recorder = ClickRecorder(website)
    browser = recorder.start_recording()
    
    if browser is None:
        print("❌ Browser start failed!")
        exit(1)
    
    input("\n🖱️  Klik op deals! Druk ENTER als klaar...")
    
    try:
        recorder.stop_recording()
    except:
        print("Browser gesloten")
    
    recorder.analyze_clicks()
    recorder.save_training_data("vakantiediscounter")
    
    print("\n✅ KLAAR!")

    
