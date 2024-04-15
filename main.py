from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify
from flask import request
import time


app = Flask(__name__)

def get_artist_play_count(idartist):
    track_code="https://open.spotify.com/intl-it/artist/"
    print(track_code+idartist)
    # Imposta le opzioni del browser Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Esegui Chrome in modalità headless (senza interfaccia grafica)
    chrome_options.add_argument("--log-level=3")
    # Inizializza il WebDriver Chrome specificando il percorso del ChromeDriver e le opzioni
    driver=webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome(executable_path=r'C:\Users\mdipa\Downloads\chromedriver_win32\chromedriver.exe', options=chrome_options)
    
    # Carica l'URL della traccia
    driver.get(track_code+idartist)
    
    
    driver.implicitly_wait(50)
    time.sleep(10)
    # Estrai il sorgente HTML della pagina dopo che è stata completamente caricata
    html = driver.page_source
    #print(html)
    
    # Chiudi il WebDriver dopo aver estratto il numero di riproduzioni
    driver.quit()
    
    # Parsing dell'HTML della pagina con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    
    # Trova l'elemento span con l'attributo data-testid="playcount"
    play_count_element = soup.find('span', class_='Ydwa1P5GkCggtLlSvphs')
    
    # Estrai il testo dall'elemento trovato
    if play_count_element:
        play_count = play_count_element.text.strip()
        return play_count
    else:
        return "Numero di riproduzioni non trovato."


def get_play_count(idtrack):
    track_code="https://open.spotify.com/intl-it/track/"
    print(track_code+idtrack)
    # Imposta le opzioni del browser Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Esegui Chrome in modalità headless (senza interfaccia grafica)
    chrome_options.add_argument("--log-level=3")
    # Inizializza il WebDriver Chrome specificando il percorso del ChromeDriver e le opzioni
    driver=webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome(executable_path=r'C:\Users\mdipa\Downloads\chromedriver_win32\chromedriver.exe', options=chrome_options)
    
    # Carica l'URL della traccia
    driver.get(track_code+idtrack)
    
    
    driver.implicitly_wait(50)
    time.sleep(10)
    # Estrai il sorgente HTML della pagina dopo che è stata completamente caricata
    html = driver.page_source
    #print(html)
    
    # Chiudi il WebDriver dopo aver estratto il numero di riproduzioni
    driver.quit()
    
    # Parsing dell'HTML della pagina con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    
    # Trova l'elemento span con l'attributo data-testid="playcount"
    play_count_element = soup.find('span', {'data-testid': 'playcount'})
    
    # Estrai il testo dall'elemento trovato
    if play_count_element:
        play_count = play_count_element.text.strip()
        return play_count
    else:
        return "Numero di riproduzioni non trovato."

        
        
@app.route('/track')
def start_track_analysis():
	track = request.args.get('track')
	nr_play = get_play_count(track)
	return "La canzone ha "+nr_play+" riproduzioni"
    

@app.route('/artist')
def start_artist_analysis():
    artist = request.args.get('artist')
    print(artist)
    nr_play = get_artist_play_count(artist)
    return "L'artista ha " + nr_play.replace("monthly listeners","") + " visualizzazioni mensili"


if __name__ == '__main__':
    app.run(debug=True)
