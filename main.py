import requests
import csv

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

# Nome do arquivo CSV
csv_filename = "C:/Users/PC/Desktop/Dados_near_earth_objects/near_earth_objects.csv"

# Número máximo de requisições
num_requests = 10

# Abrindo o arquivo CSV para escrita fora do loop
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    # Criando um escritor CSV
    csv_writer = csv.writer(csv_file)

    # Escrevendo o cabeçalho no arquivo CSV
    csv_writer.writerow([
        "ID do Objeto",
        "Nome do Objeto",
        "Diâmetro Mínimo Estimado",
        "Diâmetro Máximo Estimado",
        "Data de Aproximação Mais Próxima",
        "Distância Mínima Estimada de Aproximação",
        "Velocidade Relativa à Terra",
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
                        approach_date=neo_data['close_approach_data'][0]['close_approach_date'],
                        miss_distance=neo_data['close_approach_data'][0]['miss_distance']['kilometers'],
                        relative_velocity=neo_data['close_approach_data'][0]['relative_velocity']['kilometers_per_second'],
                        is_potentially_hazardous=neo_data['is_potentially_hazardous_asteroid']
                    )

                    # Escrevendo os dados do objeto no arquivo CSV
                    csv_writer.writerow(neo_object.to_list())

            print(f"Dados salvos em {csv_filename}")

        else:
            # Imprimindo uma mensagem de erro se a solicitação falhou
            print(f"Erro na solicitação. Código de status: {response.status_code}")
