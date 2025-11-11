import requests
import pandas as pd
import math
from datetime import datetime
from banco_de_dados import inicializar_banco, inserir_clima, inserir_previsao
from alerts import gerar_alerta, enviar_email

API_KEY = #"coloque aqui sua chave"
FORCAR_TESTE = False


#Consulta de clima atual + máximas/mínimas do dia
def consultar_clima(cidade, estado):
    url_current = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={cidade}&lang=pt"
    url_forecast = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}&lang=pt&days=1"

    try:
        data_current = requests.get(url_current).json()
        data_forecast = requests.get(url_forecast).json()

        dia_hoje = data_forecast["forecast"]["forecastday"][0]["day"]
        current = data_current["current"]

        #Calcula o ponto de orvalho (caso não venha da API)
        T = current["temp_c"]
        RH = current["humidity"]
        a, b = 17.27, 237.7
        gamma = (a * T / (b + T)) + math.log(RH / 100)
        dewpoint_c = round((b * gamma) / (a - gamma), 1)

        return {
            "cidade": data_current["location"]["name"],
            "estado": estado,
            "data": datetime.now().strftime("%Y-%m-%d"),
            "hora": datetime.now().strftime("%H:%M"),
            "temp_c": current["temp_c"],
            "feelslike_c": current["feelslike_c"],
            "temp_max": dia_hoje["maxtemp_c"],
            "temp_min": dia_hoje["mintemp_c"],
            "condition_text": current["condition"]["text"],
            "wind_kph": current["wind_kph"],
            "wind_dir": current["wind_dir"],          
            "precip_mm": current["precip_mm"],
            "humidity": current["humidity"],
            "dewpoint_c": dewpoint_c,                 
            "uv": current["uv"],
            "gust_kph": current["gust_kph"],
            "icon": "https:" + current["condition"]["icon"]
        }

    except Exception as e:
        print(f"⚠️ Erro ao consultar clima de {cidade}: {e}")
        return None


#Consulta da previsão dos próximos 3 dias
def consultar_previsao(cidade, estado):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}&days=7&lang=pt"

    try:
        data = requests.get(url).json()

        previsoes = []
        for dia in data["forecast"]["forecastday"]:
            previsoes.append({
                "cidade": data["location"]["name"],
                "estado": estado,
                "data": dia["date"],
                "temp_max": dia["day"]["maxtemp_c"],
                "temp_min": dia["day"]["mintemp_c"],
                "chance_chuva": dia["day"]["daily_chance_of_rain"],
                "condicao": dia["day"]["condition"]["text"],
                "icon": "https:" + dia["day"]["condition"]["icon"],
                "uv": dia["day"]["uv"]
            })
        return previsoes

    except Exception as e:
        print(f"⚠️ Erro ao consultar previsão de {cidade}: {e}")
        return []


#Execução principal
if __name__ == "__main__":
    inicializar_banco()

    cidades = pd.read_csv(r"C:\Users\UEMG\Desktop\BI\Projeto API\Projeto\cidades_triangulo.csv")
    usuarios = pd.read_csv(r"C:\Users\UEMG\Desktop\BI\Projeto API\Projeto\usuarios.csv")

    for _, row in cidades.iterrows():
        cidade = row["cidade"]
        estado = row["estado"]

        print(f"\n🌎 Coletando dados para {cidade}...")

        try:
            clima = consultar_clima(cidade, estado)
            if not clima:
                continue

            clima["alert"] = gerar_alerta(clima)
            inserir_clima(clima)
            print(f"✅ Clima atual de {cidade} salvo.")

            #Previsão de 3 dias
            previsoes = consultar_previsao(cidade, estado)
            if previsoes:
                inserir_previsao(previsoes)
                print(f"📆 Previsão semanal de {cidade} salva.")

            #Envio de alertas
            if clima["alert"]:
                mensagem = (
                    f"[ALERTA CLIMÁTICO] {clima['cidade']} - {clima['data']} {clima['hora']}\n"
                    f"Temperatura: {clima['temp_c']}°C (Máx: {clima['temp_max']}°C / Mín: {clima['temp_min']}°C)\n"
                    f"Condição: {clima['condition_text']}\n"
                    f"Umidade: {clima['humidity']}%\n"
                    f"Ponto de orvalho: {clima['dewpoint_c']}°C\n"
                    f"Vento: {clima['wind_kph']} km/h ({clima['wind_dir']})\n"
                    f"Alerta: {clima['alert']}\n"
                )
                for _, user in usuarios.iterrows():
                    enviar_email(user["email"], f"Alerta Climático - {clima['cidade']}", mensagem)

        except Exception as e:
            print(f"⚠️ Erro geral ao processar {cidade}: {e}")

    #Envio de e-mail de teste (se ativado)
    if FORCAR_TESTE:
        mensagem_teste = "🚀 Este é um e-mail de teste do SACI - Sistema de Alerta Climático Inteligente."
        for _, user in usuarios.iterrows():
            enviar_email(user["email"], "Teste SACI - Sistema Climático", mensagem_teste)

    print("\n📁 Coleta e gravação concluídas com sucesso.")

