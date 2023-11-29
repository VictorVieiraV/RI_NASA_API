import requests

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

    def display_info(self):
        print(f"ID do Objeto: {self.id_object}")
        print(f"Nome do Objeto: {self.name}")
        print(f"Diâmetro Mínimo Estimado: {self.diameter_min} metros")
        print(f"Diâmetro Máximo Estimado: {self.diameter_max} metros")
        print(f"Data de Aproximação Mais Próxima: {self.approach_date}")
        print(f"Distância Mínima Estimada de Aproximação: {self.miss_distance} quilômetros")
        print(f"Velocidade Relativa à Terra: {self.relative_velocity} km/s")
        print(f"Potencialmente Perigoso: {self.is_potentially_hazardous}")
        print("---")

# URL da API da NASA
url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=2023-11-21&end_date=2023-11-28&api_key=NW3jIAVXdlEPrD3Rs6YEgJquN0ZELJtAF2erudSO"

# Número máximo de requisições
num_requests = 10

for _ in range(num_requests):
    # Fazendo a solicitação GET
    response = requests.get(url)

    # Verificando se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Convertendo a resposta para JSON
        data = response.json()

        # Iterando sobre objetos próximos à Terra e criando instâncias de NearEarthObject
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

                # Exibindo informações do objeto
                neo_object.display_info()

        # Atualizando o URL para a próxima requisição
        url = data['links']['previous']
    else:
        # Imprimindo uma mensagem de erro se a solicitação falhou
        print(f"Erro na solicitação. Código de status: {response.status_code}")