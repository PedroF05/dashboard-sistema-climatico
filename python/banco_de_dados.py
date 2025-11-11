import sqlite3

DB_PATH = r"C:\Users\UEMG\Desktop\BI\Projeto API\Projeto\saci.db"

def inicializar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Clima atual
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clima_capitais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cidade TEXT,
        estado TEXT,
        data TEXT,
        hora TEXT,
        temp_c REAL,
        feelslike_c REAL,
        temp_max REAL,
        temp_min REAL,
        condition_text TEXT,
        wind_kph REAL,
        wind_dir TEXT,             
        precip_mm REAL,
        humidity REAL,
        dewpoint_c REAL,          
        uv REAL,
        gust_kph REAL,
        alert TEXT,
        icon TEXT
    )
    """)

    #Previsão de 3 dias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS previsao_semana (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cidade TEXT,
        estado TEXT,
        data TEXT,
        temp_max REAL,
        temp_min REAL,
        chance_chuva REAL,
        condicao TEXT,
        icon TEXT,
        uv REAL
    )
    """)

    conn.commit()
    conn.close()


def inserir_clima(clima):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clima_capitais
        (cidade, estado, data, hora, temp_c, feelslike_c, temp_max, temp_min,
         condition_text, wind_kph, wind_dir, precip_mm, humidity, dewpoint_c,
         uv, gust_kph, alert, icon)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        clima["cidade"], clima["estado"], clima["data"], clima["hora"],
        clima["temp_c"], clima["feelslike_c"], clima["temp_max"], clima["temp_min"],
        clima["condition_text"], clima["wind_kph"], clima["wind_dir"],
        clima["precip_mm"], clima["humidity"], clima["dewpoint_c"],
        clima["uv"], clima["gust_kph"], clima["alert"], clima["icon"]
    ))

    conn.commit()
    conn.close()


def inserir_previsao(previsoes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if not previsoes:
        conn.close()
        return

    #Apaga previsões antigas da cidade antes de inserir as novas
    cidade = previsoes[0]["cidade"]
    cursor.execute("DELETE FROM previsao_semana WHERE cidade = ?", (cidade,))

    #Insere as previsões atualizadas
    for prev in previsoes:
        cursor.execute("""
            INSERT INTO previsao_semana
            (cidade, estado, data, temp_max, temp_min, chance_chuva, condicao, icon, uv)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prev["cidade"], prev["estado"], prev["data"], prev["temp_max"], prev["temp_min"],
            prev["chance_chuva"], prev["condicao"], prev["icon"], prev["uv"]
        ))

    conn.commit()
    conn.close()
