import os
import customtkinter
from tkVideoPlayer import TkinterVideo
import speech_recognition as sr
from back import monitora_audio
import threading
from time import sleep


def Bia():
	audio = sr.Recognizer()
	with sr.Microphone() as source:
		while True:
			print("Ouvindo..")
			voz = audio.listen(source)

					
			try:
				mensagem = audio.recognize_google(voz, language='pt-br')
				mensagem = mensagem.lower()
				if 'bia' in mensagem:
					# oi_assistente()
					monitora_audio()
				else:
					pass
				break
			except sr.UnknownValueError:
				pass
			except sr.RequestError:
				pass
			
		print('Bia desligada')
		sleep(2)
		janela.destroy()



def Loop(e):
	videoplayer.play()



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

janela = customtkinter.CTk()
janela.geometry("600x500")
janela.iconbitmap('icone.ico')
janela.title('ASSISTENTE VIRTUAL')



# JANELA ASSISTENTE VIRTUAL *****************
tabview  = customtkinter.CTkTabview(master=janela, segmented_button_fg_color='#ffffff', text_color='#ffffff', segmented_button_selected_color='#000000', segmented_button_selected_hover_color='#000000')
tabview._segmented_button.configure(font=('DejaVu Sans Mono', 30, 'bold'))
tabview.pack(fill='both', expand=1, padx=10, pady=10)

tabview.add("BIA")

# ABA BIA *****************
p = threading.Thread(target=Bia)
p.start()
video2 = (r'video_jarvis.mp4')
videoplayer = TkinterVideo(master=tabview.tab("BIA"), scaled=True)
videoplayer.load(video2)
videoplayer.pack(expand=True, fill="both")
videoplayer.play()

videoplayer.bind("<<Ended>>", Loop)


janela.mainloop()   
