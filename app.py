import os
import requests
import time
from datetime import datetime, timedelta
from pytube import YouTube

class YouTubeDownloader:
    def __init__(self, url_consulta_youtube):
        self.url_consulta_youtube = url_consulta_youtube
        self.videos = []
        video_title_informativo = "Informativo Mundial das Missões | "+self.get_data()
        video_title_provai_e_vede = "PROVAI E VEDE "+self.get_data()
        print(video_title_provai_e_vede)
        
        
        self.search_video(video_title_informativo,'Informativo')
        self.search_video(video_title_provai_e_vede,'Provai e Vede')  
        
    def get_data(self):
        meses = {
            "January": "Janeiro",
            "February": "Fevereiro",
            "March": "Março",
            "April": "Abril",
            "May": "Maio",
            "June": "Junho",
            "July": "Julho",
            "August": "Agosto",
            "September": "Setembro",
            "October": "Outubro",
            "November": "Novembro",
            "December": "Dezembro"
        }

        hoje = datetime.now()
        sabado_proximo = hoje + timedelta((5 - hoje.weekday() + 7) % 7)
        nome_mes = meses[sabado_proximo.strftime("%B")]
        data_formatada = sabado_proximo.strftime(f"%d {nome_mes} %Y").upper()
        self.data1 = sabado_proximo.strftime(f"%d de {nome_mes} %Y").upper()
        self.data2 = sabado_proximo.strftime(f"%d/%m/%Y")       
        self.data3 = sabado_proximo.strftime(f"%d de {nome_mes}").upper()
        self.data4 = sabado_proximo.strftime(f"%d de {nome_mes}").lstrip('0').upper()
        self.data5 = sabado_proximo.strftime(f"%d {nome_mes} %Y").upper()
        self.data6 = sabado_proximo.strftime(f"%d/%m")   
        self.data7 = sabado_proximo.strftime(f"%d/%m").lstrip('0').upper()
        return data_formatada

    def search_video(self,video_title,tipo): 
        print(f"Consultando {tipo}")      
        data = {"context": 
                    { 
                     "client":{
                     "clientName":"WEB",
                     "clientVersion":"2.20240327.00.00"   
                    }
                    }, 
                "query": video_title} 
        response = requests.post(self.url_consulta_youtube, json=data)
        lista_videos = response.json()["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        self.add_video(lista_videos,tipo)
        
    def add_video(self,lista_videos,tipo):
        for video in lista_videos:
            if "videoRenderer" in video:
                title = video["videoRenderer"]["title"]["runs"][0]["text"]                
                if self.data1.lower() in title.lower() or self.data2.lower() in title.lower() or self.data3.lower() in title.lower() or self.data4.lower() in title.lower() or self.data5.lower() in title.lower() or self.data6.lower() in title.lower()or self.data7.lower() in title.lower():              
                    print(f"Encontrado: {title}")
                    videoId = video["videoRenderer"]["videoId"]
                    self.videos.append({"title": tipo, "url": f"https://www.youtube.com/watch?v={videoId}"})
                    break
   
    def download_videos(self):
        if not os.path.exists("arquivos"):
            os.makedirs("arquivos")

        for video in self.videos:
            attempt = 0
            while attempt < 3:
                try:
                    yt = YouTube(video["url"])
                    stream = yt.streams.get_highest_resolution()
                    file_name = video["title"] + ".mp4"
                    file_path = os.path.join("arquivos", file_name)
                    
                    # Verifica se o arquivo já existe
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Arquivo existente removido: {file_name}")

                    print(f"Tentativa {attempt + 1} de baixar: {video['title']}")
                    stream.download(output_path="arquivos", filename=file_name)
                    print(f"{video['title']} baixado com sucesso!")
                    break
                except Exception as e:
                    print(f"Erro ao baixar {video['title']}: {e}")
                    attempt += 1
                    if attempt < 3:
                        print(f"Tentativa {attempt + 1} de baixar em 5 segundos...")
                        time.sleep(5)
                    else:
                        print(f"Excedido o n�mero m�ximo de tentativas para baixar {video['title']}.")


url_consulta_youtube = "https://www.youtube.com/youtubei/v1/search"
downloader = YouTubeDownloader(url_consulta_youtube)
downloader.download_videos()