import requests
import csv
import re
from datetime import datetime, timedelta

class NearEarthObject:
    def __init__(self, id_object, name, diameter_min, diameter_max, approach_date, miss_distance, relative_velocity, is_potentially_hazardous):
        self.id_object = id_object
        self.name = name
        self.diameter_min = diameter_min
        self.diameter_max = diameter_max
        self.approach_date = approach_date
        self.miss_distance = miss_distance
        self.relative_velocity = relative_velocity
        self.is_potentially_hazardous = is_potentially_hazardous

    def to_list(self):
        # Retorna uma lista com os atributos do objeto
        return [
            self.id_object,
            self.name,
            self.diameter_min,
            self.diameter_max,
            self.approach_date,
            self.miss_distance,
            self.relative_velocity,
            self.is_potentially_hazardous
        ]

# URL da API da NASA
url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=2023-11-21&end_date=2023-11-28&api_key=NW3jIAVXdlEPrD3Rs6YEgJquN0ZELJtAF2erudSO"

# Obtendo a data atual no formato YYYY-MM-DD
current_date = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

# Nome do arquivo CSV
csv_filename = f"C:/Users/PC/Desktop/Dados_near_earth_objects/near_earth_objects_{current_date}.csv"

# Número máximo de requisições
num_requests = 500

cont = 0

# Abrindo o arquivo CSV para escrita fora do loop
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    # Criando um escritor CSV
    csv_writer = csv.writer(csv_file)

    # Escrevendo o cabeçalho no arquivo CSV
    csv_writer.writerow([
        "ID do Objeto",
        "Nome do Objeto",
        "Diâmetro Mínimo Estimado em Km",
        "Diâmetro Máximo Estimado em Km",
        "Data de Aproximação Mais Próxima",
        "Distância Mínima Estimada de Aproximação em Km",
        "Velocidade Relativa à Terra em Km/h",
        "Potencialmente Perigoso"
    ])

    # Loop para fazer o número específico de requisições
    for _ in range(num_requests):
        # Fazendo a solicitação GET
        response = requests.get(url)

        # Verificando se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Convertendo a resposta para JSON
            data = response.json()

            # Iterando sobre objetos próximos à Terra e gravando no CSV
            for date, neo_list in data['near_earth_objects'].items():
                for neo_data in neo_list:
                    neo_object = NearEarthObject(
                        id_object=neo_data['neo_reference_id'],
                        name=neo_data['name'],
                        diameter_min=neo_data['estimated_diameter']['kilometers']['estimated_diameter_min'],
                        diameter_max=neo_data['estimated_diameter']['kilometers']['estimated_diameter_max'],
                        approach_date=neo_data['close_approach_data'][0]['close_approach_date_full'],
                        miss_distance=neo_data['close_approach_data'][0]['miss_distance']['kilometers'],
                        relative_velocity=neo_data['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                        is_potentially_hazardous=neo_data['is_potentially_hazardous_asteroid']
                    )

                    # Escrevendo os dados do objeto no arquivo CSV
                    csv_writer.writerow(neo_object.to_list())

            cont += 1
            print(f"Dados salvos em {csv_filename} - {cont}")
            
            url = data['links']['previous']
            
            
            # Extracting start_date and end_date from the URL string using regular expressions
            start_date_match = re.search(r'start_date=(\d{4}-\d{2}-\d{2})', url)
            end_date_match = re.search(r'end_date=(\d{4}-\d{2}-\d{2})', url)

            if start_date_match and end_date_match:
                # Parsing the matched dates
                start_date_str = start_date_match.group(1)
                end_date_str = end_date_match.group(1)

                # Converting the dates to datetime objects
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

                # Adjusting the dates by subtracting one day
                start_date -= timedelta(days=1)
                end_date -= timedelta(days=1)

                # Formatting the adjusted dates back to strings
                adjusted_start_date_str = start_date.strftime("%Y-%m-%d")
                adjusted_end_date_str = end_date.strftime("%Y-%m-%d")

                # Reconstructing the URL with adjusted dates
                adjusted_url = re.sub(
                    r'start_date=\d{4}-\d{2}-\d{2}',
                    f'start_date={adjusted_start_date_str}',
                    re.sub(r'end_date=\d{4}-\d{2}-\d{2}', f'end_date={adjusted_end_date_str}', url)
                )
            url = adjusted_url
        else:
            # Imprimindo uma mensagem de erro se a solicitação falhou
            print(f"Erro na solicitação. Código de status: {response.status_code}")
