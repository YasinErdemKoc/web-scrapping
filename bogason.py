import time
import json
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import pandas as pd

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebScraper:
    def __init__(self):
        self.port_counter = 9223  # Başlangıç portu
        self.driver = self._initialize_driver()
      

    def _initialize_driver(self):
        """WebDriver'ı başlatır ve ayarları yapar."""
        options = Options()
        options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--remote-debugging-port={self.port_counter}")  # Portu dinamik olarak ayarla

        service = ChromeService(executable_path=ChromeDriverManager().install())
        logging.info(f"WebDriver başlatılıyor: Port - {self.port_counter}")
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        return driver

    def add_url(self):
     new_url = simpledialog.askstring("URL Ekle", "Yeni URL'yi girin:")
     if new_url:
        self.urls.append({'url': new_url})
        self.save_urls()
        self.populate_tree()  # TreeView'i güncelle

    def delete_url(self):
       selected_item = self.tree.selection()[0]
       self.urls.pop(int(selected_item))
       self.save_urls()
       self.populate_tree()

    def update_url(self):
       selected_item = self.tree.selection()[0]
       new_url = simpledialog.askstring("URL Güncelle", "Yeni URL'yi girin:")
       if new_url:
        self.urls[int(selected_item)]['url'] = new_url
        self.save_urls()
        self.populate_tree()

       
    def _wait_for_element(self, xpath=None, css_selector=None, timeout=10):
        try:
            if xpath:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            if css_selector:
                return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except Exception as e:
            logging.error(f"Element yüklenemedi. Hata: {e}")
        return None

    def _get_text(self, element):
        return element.text.strip() if element else "Veri bulunamadı"

    def get_text_from_elements(self, xpath=None, css_selector=None):
        element = None
        if xpath:
            element = self._wait_for_element(xpath=xpath)
        if not element and css_selector:
            element = self._wait_for_element(css_selector=css_selector)
        
        if element:
            return self._get_text(element)
        return "Veri bulunamadı"
    
    
    # Status label'in içine scraping sırasında veri güncellemesi ekleyin
    def update_status(self, message):
     self.status_label.config(text=message)
     self.root.update_idletasks()  # Anlık olarak etiketi güncelle

    def scrape_data(self, url):
        logging.info(f"Veri çekme işlemi başlatılıyor: {url}")
        self.port_counter += 1
        self.driver.quit()
        self.driver = self._initialize_driver()

        self.driver.get(url)
        data = {}
        self.update_status(f"{url_data['url']} işleniyor...")

        try:
            # Örnek veri çekme işlemleri

            #GENERAL İNFORMATİON
            data["Name"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[1]/div/div/div/div/div[1]/span")
            data["Name"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div.row.mb-1 > div > div > div > div > div.col.font-large-bold > span")
            data["Ear Tag"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[1]/div/div/div/div/div[2]/span")
            data["Ear Tag"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div.row.mb-1 > div > div > div > div > div.col.d-flex.justify-content-end.font-large > span")
            data["Born"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[2]/div[2]/div/div[1]/div/div/div/detail-grunddaten-component/table/tbody/tr[2]/td[2]")
            data["Born"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(2) > div:nth-child(2) > div > div.row.flex-grow-1 > div > div > div > detail-grunddaten-component > table > tbody > tr:nth-child(2) > td:nth-child(2)")
            data["Breeder"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[2]/div[2]/div/div[1]/div/div/div/detail-grunddaten-component/table/tbody/tr[3]/td[2]")
            data["Breeder"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(2) > div:nth-child(2) > div > div.row.flex-grow-1 > div > div > div > detail-grunddaten-component > table > tbody > tr:nth-child(3) > td:nth-child(2)")
            data["Free of"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[2]/div[2]/div/div[2]/div/div/div/p/span[1]/span")
            data["Free of"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(2) > div:nth-child(2) > div > div.row.hide-when-medium > div > div > div > p > span:nth-child(1) > span")
            data["Genetic character"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[2]/div[2]/div/div[2]/div/div/div/p/span[2]/span/span[1]/span[1]")
            data["Genetic character"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(2) > div:nth-child(2) > div > div.row.hide-when-medium > div > div > div > p > span:nth-child(2) > span > span:nth-child(1) > span:nth-child(1)")
            data["Sire line"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[2]/div[2]/div/div[2]/div/div/div/p/span[3]/span")
            data["Sire line"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(2) > div:nth-child(2) > div > div.row.hide-when-medium > div > div > div > p > span:nth-child(3) > span")
            data["Mother values"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[3]/div[1]/pedigree-small-component/table/tbody/tr[3]/td[1]/div")
            data["Mother values"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div.row.mb-3.print-mb-1.h-100 > div.col-xl-8.col-print-8 > pedigree-small-component > table > tbody > tr:nth-child(3) > td:nth-child(1) > div")
            data["gGZW"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[3]/div[2]/div/div[1]/div/div/div/span[1]/span[2]")
            data["gGZW"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div.row.mb-3.print-mb-1.h-100 > div.col-xl.hide-when-medium.col-print-4 > div > div.col.col-md-12.margin-bottom-xl.col-print-12 > div > div > div > span:nth-child(1) > span:nth-child(2)")
            data["MW"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[3]/div[2]/div/div[2]/div/div/div/span[1]")
            data["MW"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div.row.mb-3.print-mb-1.h-100 > div.col-xl.hide-when-medium.col-print-4 > div > div.col.col-md-4.mt-sm-2.border-blue.col-print-4 > div > div > div > span:nth-child(1)")
            data["FW"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[3]/div[2]/div/div[3]/div/div/div/span[2]")
            data["FW"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div.row.mb-3.print-mb-1.h-100 > div.col-xl.hide-when-medium.col-print-4 > div > div.col.col-md-4.mt-sm-2.border-red.col-print-4 > div > div > div > span:nth-child(2)")
            data["FIT"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[3]/div[2]/div/div[4]/div/div/div/span[1]")
            data["FIT"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div.row.mb-3.print-mb-1.h-100 > div.col-xl.hide-when-medium.col-print-4 > div > div.col.col-md-4.mt-sm-2.border-green.col-print-4 > div > div > div > span:nth-child(1)")
            data["BREEDING VALUES"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[4]/div/div/div[2]/div/div/detail-diff-component")
            data["BREEDING VALUES"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(4) > div > div > div.card-header.header-primary.print-padding-card-header-small > div > div:nth-child(1) > span")
            data["gGZW2"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[4]/div/div/div[1]/div/div[3]/strong")
            data["gGZW2"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(4) > div > div > div.card-header.header-primary.print-padding-card-header-small > div > div.col.text-align-right > strong")
            data["GZW"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[4]/div/div/div[2]/div/div/detail-diff-component/i")
            data["GZW"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(4) > div > div > div.card-body.padding-card-body-small > div > div > detail-diff-component > i")
            data["MILK MV"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[5]/div/div/div[1]/div/div[2]/strong")
            data["MILK MV"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(5) > div > div > div.card-header.print-padding-card-header-small > div > div.col.text-align-right > strong")
            data["MILK MW2"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[5]/div/div/div[2]/div/div/strong")
            data["MILK MW2"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(5) > div > div > div.card-body.padding-card-body-small > div > div > strong")
            data["BEEF FW"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[6]/div/div/div[1]/div/div[2]/strong")
            data["BEEF FW"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(6) > div > div > div.card-header.print-padding-card-header-small > div > div.col.text-align-right > strong")
            data["Net daily gain"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[6]/div/div/div[2]/div/div[1]/detail-zuchtwert-component/span")
            data["Net daily gain"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(6) > div > div > div.card-body.padding-card-body-small > div > div:nth-child(1) > detail-zuchtwert-component > span")
            data["Carcass percentage"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[6]/div/div/div[2]/div/div[2]/detail-zuchtwert-component/span")
            data["Carcass percentage"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(6) > div > div > div.card-body.padding-card-body-small > div > div:nth-child(2) > detail-zuchtwert-component > span")
            data["EUROP trade class"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[6]/div/div/div[2]/div/div[3]/detail-zuchtwert-component/span")
            data["EUROP trade class"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(6) > div > div > div.card-body.padding-card-body-small > div > div:nth-child(3) > detail-zuchtwert-component > span")
            
            #FİTNESS
            
            data["ÖZW"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[1]/div/div[3]/strong")
            data["ÖZW"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-header.print-padding-card-header-small > div > div.col.px-0 > strong")
            data["FIT"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[1]/div/div[4]/strong")
            data["FIT"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-header.print-padding-card-header-small > div > div.col.text-align-right > strong")
            data["Longevity"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[1]/div/div[1]/detail-zuchtwert-component/span")
            data["Longevity"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(1) > div > div:nth-child(1) > detail-zuchtwert-component > span")
            data["Persistency"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[1]/div/div[2]/detail-zuchtwert-component/span")
            data["Persistency"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(1) > div > div:nth-child(2) > detail-zuchtwert-component > span")
            data["Yield improvement"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[1]/div/div[3]/detail-zuchtwert-component/span")
            data["Yield improvement"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(1) > div > div:nth-child(3) > detail-zuchtwert-component > span")
            data["Milking speed"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[1]/div/div[4]/detail-zuchtwert-component/span")
            data["Milking speed"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(1) > div > div:nth-child(4) > detail-zuchtwert-component > span")
            data["Udder health index"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[2]/div/div[1]/detail-zuchtwert-component/span")
            data["Udder health index"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(2) > div > div:nth-child(1) > detail-zuchtwert-component > span")
            data["Fertility index"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[2]/div/div[2]/detail-zuchtwert-component/span")
            data["Fertility index"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(2) > div > div:nth-child(2) > detail-zuchtwert-component > span")
            data["Calving ease direct"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[2]/div/div[3]/detail-zuchtwert-component/span")
            data["Calving ease direct"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(2) > div > div:nth-child(3) > detail-zuchtwert-component > span")
            data["Milking behaviour"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[2]/div/div[4]/detail-zuchtwert-component/span")
            data["Milking behaviour"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(2) > div > div:nth-child(4) > detail-zuchtwert-component > span")
            data["Somatic cell count"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[3]/div/div[1]/detail-zuchtwert-component/span")
            data["Somatic cell count"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(3) > div > div:nth-child(1) > detail-zuchtwert-component > span")
            data["Claw health index"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[3]/div/div[2]/detail-zuchtwert-component/span")
            data["Claw health index"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(3) > div > div:nth-child(2) > detail-zuchtwert-component > span")
            data["Calving ease maternal"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[3]/div/div[3]/detail-zuchtwert-component/span")
            data["Calving ease maternal"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(3) > div > div:nth-child(3) > detail-zuchtwert-component > span")
            data["Calf vitality"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[3]/div/div[4]/detail-zuchtwert-component/span")
            data["Calf vitality"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(3) > div > div:nth-child(4) > detail-zuchtwert-component > span")
            data["Mastitis"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[2]/div[12]/detail-zuchtwert-component/span")
            data["Mastitis"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(4) > div > div:nth-child(1) > detail-zuchtwert-component > span")
            data["Early fert. disorders"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[4]/div/div[2]/detail-zuchtwert-component/span")
            data["Early fert. disorders"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(4) > div > div:nth-child(2) > detail-zuchtwert-component > span")
            data["Cysts"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[4]/div/div[3]/detail-zuchtwert-component/span")
            data["Cysts"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(4) > div > div:nth-child(3) > detail-zuchtwert-component > span")
            data["Milk fever"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[7]/div/div/div[2]/div[1]/div[4]/div/div[4]/detail-zuchtwert-component/span")
            data["Milk fever"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div:nth-child(7) > div > div > div.card-body.padding-card-body-small > div.row.visible-when-xl > div:nth-child(4) > div > div:nth-child(4) > detail-zuchtwert-component > span")
            
            #CONFORMATİON
            
            data["Conformation info"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[1]/div/div[2]")
            data["Conformation info"] = self.get_text_from_elements(css_selector="body > main-component > div.container-fluid > div > fleckvieh-detail > div > div.row.mb-2.print-mb-1.h-100.print-pagebreak > div > div > div.card-header.print-padding-card-header-small > div > div.col.text-align-right.col-print-6")
            data["Frame"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[2]/td[2]/span")
            data["Frame"] = self.get_text_from_elements(css_selector="#ext1 > td:nth-child(2) > span")
            data["Muscling"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[3]/td[2]/span")
            data["Muscling"] = self.get_text_from_elements(css_selector="#ext2 > td:nth-child(2) > span")
            data["Feet & Legs"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[4]/td[2]/span")
            data["Feet & Legs"] = self.get_text_from_elements(css_selector="#ext3 > td:nth-child(2) > span")
            data["Udder"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[5]/td[2]/span")
            data["Udder"] = self.get_text_from_elements(css_selector="#ext4 > td:nth-child(2) > span")
            data["Cross height"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[6]/td[2]/span")
            data["Cross height"] = self.get_text_from_elements(css_selector="#ext5 > td:nth-child(2) > span")
            data["Body length"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[7]/td[2]/span")
            data["Body length"] = self.get_text_from_elements(css_selector="#ext6 > td:nth-child(2) > span")
            data["Hip width"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[8]/td[2]/span")
            data["Hip width"] = self.get_text_from_elements(css_selector="#ext7 > td:nth-child(2) > span")
            data["Body depth"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[9]/td[2]/span")
            data["Body depth"] = self.get_text_from_elements(css_selector="#ext8 > td:nth-child(2) > span")
            data["Rump angle"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[10]/td[2]/span")
            data["Rump angle"] = self.get_text_from_elements(css_selector="#ext9 > td:nth-child(2) > span")
            data["Hock angularity"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[11]/td[2]/span")
            data["Hock angularity"] = self.get_text_from_elements(css_selector="#ext10 > td:nth-child(2) > span")
            data["Hock develop"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[12]/td[2]/span")
            data["Hock develop"] = self.get_text_from_elements(css_selector="#ext11 > td:nth-child(2) > span")
            data["Pasterns"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[13]/td[2]/span")
            data["Pasterns"] = self.get_text_from_elements(css_selector="#ext12 > td:nth-child(2) > span")
            data["Hoof height"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[14]/td[2]/span")
            data["Hoof height"] = self.get_text_from_elements(css_selector="#ext13 > td:nth-child(2) > span")
            data["Fore udder length"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[15]/td[2]/span")
            data["Fore udder length"] = self.get_text_from_elements(css_selector="#ext14 > td:nth-child(2) > span")
            data["Rear udder length"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[16]/td[2]/span")
            data["Rear udder length"] = self.get_text_from_elements(css_selector="#ext15 > td:nth-child(2) > span")
            data["Fore udder attachment"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[17]/td[2]/span")
            data["Fore udder attachment"] = self.get_text_from_elements(css_selector="#ext16 > td:nth-child(2) > span")
            data["Central ligament"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[18]/td[2]/span")
            data["Central ligament"] = self.get_text_from_elements(css_selector="#ext17 > td:nth-child(2) > span")
            data["Udder depth"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[19]/td[2]/span")
            data["Udder depth"] = self.get_text_from_elements(css_selector="#ext18 > td:nth-child(2) > span")
            data["Teat length"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[20]/td[2]/span")
            data["Teat length"] = self.get_text_from_elements(css_selector="#ext19 > td:nth-child(2) > span")
            data["Teat thickness"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[21]/td[2]/span")
            data["Teat thickness"] = self.get_text_from_elements(css_selector="#ext20 > td:nth-child(2) > span")
            data["Front teat placement"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[22]/td[2]/span")
            data["Front teat placement"] = self.get_text_from_elements(css_selector="#ext21 > td:nth-child(2) > span")
            data["Rear teat placement"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[23]/td[2]/span")
            data["Rear teat placement"] = self.get_text_from_elements(css_selector="#ext22 > td:nth-child(2) > span")
            data["Rear teat direction"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[24]/td[2]/span")
            data["Rear teat direction"] = self.get_text_from_elements(css_selector="#ext23 > td:nth-child(2) > span")
            data["Additional teats"] = self.get_text_from_elements(xpath="/html/body/main-component/div[2]/div/fleckvieh-detail/div/div[8]/div/div/div[2]/exterieur-graph-component/table/tbody/tr[25]/td[2]/span")
            data["Additional teats"] = self.get_text_from_elements(css_selector="#ext24 > td:nth-child(2) > span")
            # Diğer veriler buraya eklenebilir
        except Exception as e:
            logging.error(f"Veri çekme hatası: {e}")

        self.driver.quit()
        return data

def update_progress_bar(progress, max_value):
    progress['maximum'] = max_value
    progress['value'] = 0
    for i in range(1, max_value + 1):
        time.sleep(0.1)
        progress['value'] = i
        progress.update()



def save_data_to_file(data, file_format='csv'):
    # DataFrame oluşturulmadan önce tüm verilerin eksiksiz olduğundan emin ol
    df = pd.DataFrame(data)

    # Kaydetme işlemi
    if file_format == 'csv':
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:  # Kullanıcı bir dosya seçtiyse
            df.to_csv(file, index=False)
    elif file_format == 'excel':
        file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file:  # Kullanıcı bir dosya seçtiyse
            df.to_excel(file, index=False)

class ScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper")

        # self.urls boş bir liste olarak tanımlanıyor
        self.urls = []  # Burada boş bir liste oluşturun
        self.setup_ui()

    def setup_ui(self):
        # Frame oluşturun (self.frame)
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)
        style = ttk.Style()
        style.configure("TLabel", font=('Arial', 12))
        style.configure("TButton", font=('Arial', 10))
        self.status_label = ttk.Label(self.frame, text="Hazır", style="TLabel")
        # Status label'den sonra progress bar ekleyelim
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=400, mode="determinate", variable=self.progress_var)
        self.progress.grid(row=4, column=0, pady=10)
        # Treeview için sütunları tanımlayın
        columns = (
            "Name", "Ear Tag", "Born", "Breeder", "Free of", "Genetic character",
            "Sire line", "Mother values", "gGZW", "MW", "FW", "FIT", "Longevity", 
            "Persistency", "Yield improvement", "Milking speed", "Udder health index",
            "Fertility index", "Calving ease direct", "Milking behaviour", 
            "Somatic cell count", "Claw health index", "Calving ease maternal", 
            "Mastitis", "Early fert. disorders", "Cysts", "Milk fever", "Conformation info", 
            "Frame", "Muscling", "Feet & Legs", "Udder", "Cross height", "Body length", 
            "Hip width", "Body depth", "Rump angle", "Hock angularity", "Hock develop", 
            "Pasterns", "Hoof height", "Fore udder length", "Rear udder length",
            "Fore udder attachment", "Central ligament", "Udder depth", "Teat length", 
            "Teat thickness", "Front teat placement", "Rear teat placement", 
            "Rear teat direction", "Additional teats"
        )

        # Treeview widget'ini oluşturun
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        # Sütun başlıklarını ayarlayın ve genişlikleri içeriğe göre dinamik ayarlayın
        for col in columns:
            self.tree.heading(col, text=col)
            max_width = len(col)  # Başlık genişliği
            self.tree.column(col, width=max_width * 10, anchor="center")  # Sütun genişliğini başlık uzunluğuna göre ayarla

        # Treeview'i ekleyin ve kaydırma çubuğunu ayarlayın
        self.tree.grid(row=0, column=0, sticky="nsew")


        scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        scrollbar.grid(row=1, column=0, sticky="ew")
        self.tree.config(xscrollcommand=scrollbar.set)
        

       
        def populate_tree(self):
        # URL'leri ve verileri Treeview'e ekleyin
         for url_data in self.urls:
            values = (
                url_data.get('name', "N/A"),
                url_data.get('ear_tag', "N/A"),
                url_data.get('born', "N/A"),
                url_data.get('breeder', "N/A"),
                url_data.get('free_of', "N/A"),
                url_data.get('genetic_character', "N/A"),
                url_data.get('sire_line', "N/A"),
                url_data.get('mother_values', "N/A"),
                # Diğer veri alanlarını burada ekleyin
            )
            self.tree.insert("", "end", values=values)

        # Treeview'e veri ekleme işlemi
         self.populate_tree()
          # Progress bar
        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=20)      
        button_frame = Frame(self.root)
        button_frame.pack(pady=10)
        Button(button_frame, text="Verileri Çek", command=self.start_scraping).pack(side=LEFT, padx=5)
        Button(button_frame, text="CSV Olarak Kaydet", command=lambda: save_data_to_file(self.urls, 'csv')).pack(side=LEFT, padx=5)
        Button(button_frame, text="Excel Olarak Kaydet", command=lambda: save_data_to_file(self.urls, 'excel')).pack(side=LEFT, padx=5)
    def start_scraping(self):
        thread = threading.Thread(target=self.scrape_all_data)
        thread.start()
      

    def scrape_all_data(self):
        scraper = WebScraper()
        for i, url_info in enumerate(self.urls):
            data = scraper.scrape_data(url_info["url"])
            self.tree.set(self.tree.get_children()[i], column="Name", value=data.get("Name", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Ear Tag", value=data.get("Ear Tag", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Born", value=data.get("Born", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Breeder", value=data.get("Breeder", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Free of", value=data.get("Free of", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Genetic character", value=data.get("Genetic character", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Sire line", value=data.get("Sire line", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Mother values", value=data.get("Mother values", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="gGZW", value=data.get("gGZW", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="MW", value=data.get("MW", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="FW", value=data.get("FW", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="FIT", value=data.get("FIT", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Longevity", value=data.get("Longevity", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Persistency", value=data.get("Persistency", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Yield improvement", value=data.get("Yield improvement", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Milking speed", value=data.get("Milking speed", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Udder health index", value=data.get("Udder health index", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Fertility index", value=data.get("Fertility index", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Calving ease direct", value=data.get("Calving ease direct", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Milking behaviour", value=data.get("Milking behaviour", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Somatic cell count", value=data.get("Somatic cell count", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Claw health index", value=data.get("Claw health index", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Calving ease maternal", value=data.get("Calving ease maternal", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Mastitis", value=data.get("Mastitis", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Early fert. disorders", value=data.get("Early fert. disorders", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Cysts", value=data.get("Cysts", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Milk fever", value=data.get("Milk fever", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Conformation info", value=data.get("Conformation info", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Frame", value=data.get("Frame", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Muscling", value=data.get("Muscling", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Feet & Legs", value=data.get("Feet & Legs", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Udder", value=data.get("Udder", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Cross height", value=data.get("Cross height", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Body length", value=data.get("Body length", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Hip width", value=data.get("Hip width", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Body depth", value=data.get("Body depth", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Rump angle", value=data.get("Rump angle", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Hock angularity", value=data.get("Hock angularity", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Hock develop", value=data.get("Hock develop", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Pasterns", value=data.get("Pasterns", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Hoof height", value=data.get("Hoof height", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Fore udder length", value=data.get("Fore udder length", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Rear udder length", value=data.get("Rear udder length", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Fore udder attachment", value=data.get("Fore udder attachment", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Central ligament", value=data.get("Central ligament", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Udder depth", value=data.get("Udder depth", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Teat length", value=data.get("Teat length", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Teat thickness", value=data.get("Teat thickness", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Front teat placement", value=data.get("Front teat placement", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Rear teat placement", value=data.get("Rear teat placement", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Rear teat direction", value=data.get("Rear teat direction", "N/A"))
            self.tree.set(self.tree.get_children()[i], column="Additional teats", value=data.get("Additional teats", "N/A"))

            update_progress_bar(self.progress, len(self.urls))
            
if __name__ == "__main__":
    root = Tk()
    app = ScraperGUI(root)
    root.mainloop()
