import json
import os
from datetime import datetime
import pyautogui
import pyperclip

import speech_recognition as sr
from bs4 import BeautifulSoup
from gtts import gTTS
from playsound import playsound
from requests import get
from time import sleep

from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService



def cria_audio(audio,mensagem):
	tts = gTTS(mensagem, lang="pt-br")
	tts.save(audio)
	playsound(audio)
	os.remove(audio)


def monitora_audio():
	oi_assistente()
	recon = sr.Recognizer()
	with sr.Microphone() as source:
		continuar = 'sim'
		while True:
			if continuar == 'sim':
				print("Diga algo")
				audio = recon.listen(source)
			try:
				mensagem = recon.recognize_google(audio, language='pt-br')
				mensagem = mensagem.lower()
				print("Você disse", mensagem)
				executa_comandos(mensagem)
				sleep(1)
				resposta = 'sim'
				while True:
					if resposta == 'sim':
						cria_audio('audios/welcome.mp3', 'Posso ajudar em algo a mais?')
						audio = recon.listen(source)
						mensagem = recon.recognize_google(audio, language='pt-br')
						mensagem = mensagem.lower()
						print("Você disse", mensagem)
						if 'não' in mensagem:
							resposta = 'não'
						elif 'sim' in mensagem:
							cria_audio('audios/welcome.mp3', 'Em que posso ajudar?')
							audio = recon.listen(source)
							mensagem = recon.recognize_google(audio, language='pt-br')
							mensagem = mensagem.lower()
							print("Você disse", mensagem)
							executa_comandos(mensagem)
					elif resposta == 'não':
						cria_audio('audios/welcome.mp3', 'Ok,Bia Desligando! Até mais')
						continuar = 'não'
						break						
			except sr.UnknownValueError:
				pass
			except sr.RequestError:
				pass
			else:
				break
		return resposta
	

def executa_comandos(mensagem):
	if 'horas' in mensagem:
		hora = datetime.now().strftime('%H:%M')
		frase = (f'Agora são {hora}')
		cria_audio('audios/mensagem.mp3', frase)

	elif 'desligar computador' in mensagem and 'uma hora' in mensagem:
		os.system('shutdown -s -t 3600')

	elif 'desligar computador' in mensagem and 'meia hora' in mensagem:
		os.system('shutdown -s -t 1800')

	elif 'cancelar desligamento do computador' in mensagem:
		os.system('shutdown -a')

	elif 'notícias' in mensagem:
		ultimas_noticias()

	elif 'cotação' in mensagem and 'dólar' in mensagem:
		cotacao_moeda('Dólar')

	elif 'cotação' in mensagem and 'euro' in mensagem:
		cotacao_moeda('Euro')

	elif 'cotação' in mensagem and 'bitcoin' in mensagem:
		cotacao_moeda('Bitcoin')

	elif 'mandar' in mensagem and 'whats' in mensagem:
		Mandar_Whats()



def oi_assistente():
	cria_audio('audios/welcome.mp3', 'Olá, em que posso ajudá-lo?')	


def ultimas_noticias():
	site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
	noticias = BeautifulSoup(site.text, 'html.parser')
	for item in noticias.findAll('item')[:7]:
		mensagem = item.title.text
		cria_audio('audios/mensagem.mp3', mensagem)


def cotacao_moeda(moeda):
	if moeda == 'Dólar':
		requisicao = get('https://economia.awesomeapi.com.br/all/USD-BRL')
		cotacao = requisicao.json()
		nome = cotacao['USD']['name']
		data = cotacao['USD']['create_date']
		valor = cotacao['USD']['bid']
		mensagem = f'Cotação do {nome} em {data} é {valor} reais'
		cria_audio('audios/mensagem.mp3', mensagem)
	elif moeda == 'Euro':
		requisicao = get('https://economia.awesomeapi.com.br/all/EUR-BRL')
		cotacao = requisicao.json()
		nome = cotacao['EUR']['name']
		data = cotacao['EUR']['create_date']
		valor = cotacao['EUR']['bid']
		mensagem = f'Cotação do {nome} em {data} é {valor} reais'
		cria_audio('audios/mensagem.mp3', mensagem)
	elif moeda == 'Bitcoin':
		requisicao = get('https://economia.awesomeapi.com.br/all/BTC-BRL')
		cotacao = requisicao.json()
		nome = cotacao['BTC']['name']
		data = cotacao['BTC']['create_date']
		valor = cotacao['BTC']['bid']
		mensagem = f'Cotação do {nome} em {data} é {valor} reais'
		cria_audio('audios/mensagem.mp3', mensagem)


def iniciar_driver():	
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1300,1000']
    for argument in arguments:
        chrome_options.add_argument(argument)
    chrome_options.add_experimental_option('prefs', {
        # Notificar o google chrome sobre essa alteração
        'download.directory_upgrade': True,
        # Desabilitar confirmação de download
        'download.prompt_for_download': False,
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permitir multiplos download
        'profile.default_content_setting_values.automatic_downloads': 1,
        # Remover todos os erros e avisos, 
        "excludeSwitches": ['disable-logging'],
    })
    chrome_service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver


def digitar_naturalmente(texto, elemento):
    for letra in texto:
        elemento.send_keys(letra)
        sleep(randint(1, 5)/20)


def Mandar_Whats():
	recon = sr.Recognizer()
	with sr.Microphone() as source:
		cria_audio('audios/welcome.mp3', 'Para quem deseja enviar um whatsapp?')
		audio = recon.listen(source)
		mensagem = recon.recognize_google(audio, language='pt-br')
		mensagem = mensagem.lower()
		para = str(mensagem)
		print("Você disse", para)
		pyautogui.press('win')
		sleep(1)
		pyautogui.write('whatsapp', interval=0.50)
		sleep(1)
		pyautogui.press('enter')
		sleep(3)
		for x in para:
			pyperclip.copy(x)
			pyautogui.hotkey('ctrl', 'v', interval=0.05)
		pyautogui.press('tab')
		sleep(1)
		pyautogui.press('enter')
		cria_audio('audios/welcome.mp3', 'Qual seria a mensagem?')
		audio = recon.listen(source)
		mensagem = recon.recognize_google(audio, language='pt-br')
		mensagem = mensagem.lower()
		msg = str(mensagem)
		print("Você disse", msg)
		for x in msg:
			pyperclip.copy(x)
			pyautogui.hotkey('ctrl', 'v', interval=0.05)
		pyautogui.press('enter')
		sleep(2)
		pyautogui.hotkey('alt', 'F4')


