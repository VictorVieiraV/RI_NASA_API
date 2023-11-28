import scrapy
from scrapy.http import Response

class RiBot(scrapy.Spider):
    name = "RI BOT"
    # start_urls = ["https://www.buser.com.br/onibus/belo-horizonte-mg/uberlandia-mg?ida=2023-11-27",""]
    start_urls = ["https://www.buser.com.br/onibus/belo-horizonte-mg/uberlandia-mg?ida=2023-11-27"]

    def parse(self, response):
        viagens = []
        for categoria in response.css(".grupos-por-dia .ada-card"):
            viagem = {}
            viagem['HorarioSaida'] = categoria.css('.itinerario-resumido .is-origem .ird-hora').extract_first()
            viagem['HorarioChegada'] = categoria.css('.itinerario-resumido .is-origem .ird-destino').extract_first()
            viagem['Preco'] = categoria.css('.p-preco').extract_first()
            
            viagens.append(viagem)
            print(viagens)