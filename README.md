# 🌦️ Sistema de Alerta Climático Inteligente (SACI)

Este projeto foi desenvolvido com o objetivo de automatizar a **coleta, armazenamento e análise de dados climáticos** em tempo real, integrando **Python, SQLite e Power BI** para criação de um painel interativo com alertas automáticos por e-mail.

-------------------------------------------------------------

## 📊 Funcionalidades

O sistema coleta e organiza informações climáticas de diversas cidades e as exibe em um **dashboard interativo** no Power BI.

O painel foi dividido em seções principais:

* **Clima Atual** – exibe temperatura atual, sensação térmica, ponto de orvalho, direção e velocidade do vento, índice UV e condição do tempo.  
* **Previsão Semanal** – apresenta a previsão dos próximos 3 dias, com máxima, mínima e chance de chuva.  
* **Histórico de Temperaturas** – monitora as variações de temperatura e condições ao longo do tempo.  
* **Alertas Automáticos** – identifica condições extremas (calor, chuvas fortes, UV alto) e envia notificações por e-mail aos usuários cadastrados.

-------------------------------------------------------------

## 🧰 Tecnologias Utilizadas

* 🐍 **Python** – coleta de dados e automação  
* 🌐 **WeatherAPI** – fonte dos dados meteorológicos  
* 🗄️ **SQLite** – armazenamento local dos dados  
* 📧 **SMTP (smtplib)** – envio de alertas por e-mail  
* 📊 **Power BI** – construção do painel visual e medidas DAX  

-------------------------------------------------------------

## 🧠 Estrutura do Projeto

* O script Python realiza **consultas automáticas à API** para obter os dados climáticos atuais e as previsões dos próximos 3 dias.  
* As informações são armazenadas no **banco de dados SQLite**, organizadas em duas tabelas:
  - `clima_capitais` → dados de temperatura e clima atuais  
  - `previsao_semana` → previsão dos próximos dias  
* Cidades e usuários são definidos através de dois arquivos CSV:
  - `cidades_triangulo.csv`  
  - `usuarios.csv`  
* O Power BI consome esses dados e apresenta o dashboard dinâmico com **visualizações e alertas coloridos**.

-------------------------------------------------------------

## ⚙️ Estrutura do Repositório

* `main.py` → Script principal de coleta e alerta  
* `banco_de_dados.py` → Criação das tabelas e inserção no banco  
* `alerts.py` → Geração de alertas automáticos e envio por e-mail  
* `cidades_triangulo.csv` → Lista de cidades monitoradas  
* `usuarios.csv` → Lista de usuários que recebem alertas  
* `saci.db` → Banco de dados SQLite  
* `dashboard_saci.pbix` → Painel do Power BI com todas as análises
*  `prints/` → Capturas de tela das páginas do painel  

-------------------------------------------------------------

## 📎 Prints do Dashboard

### 🔹 Dashboard
!\[Dashboard] (prints/Dashboard.png)

### 🔹 Alertas
!\[Alertas] (prints/Alertas.png)

-------------------------------------------------------------

Sinta-se à vontade para clonar, adaptar ou contribuir!

📬 Para dúvidas, sugestões ou colaborações: https://www.linkedin.com/in/pedro-henrique-freitas-santos-b93200283/

-------------------------------------------------------------

#PowerBI #SQLite #DataAnalytics #Clima #Dashboard #BusinessIntelligence #Projetos
