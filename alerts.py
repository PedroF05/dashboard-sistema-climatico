import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ORIGEM = "alertas.climaticos00@gmail.com"
SENHA_APP = "tnixzryztjnzfeeq"

def gerar_alerta(registro):
    alertas = []
    if registro["precip_mm"] > 20:
        alertas.append("Chuva forte, atenção a possíveis alagamentos e deslizamentos. Evite áreas de risco e desloque-se apenas se necessário.")
    if "storm" in registro["condition_text"].lower() or registro["gust_kph"] > 60:
        alertas.append("Tempestade, evite permanecer ao ar livre, desligue equipamentos eletrônicos e siga as orientações de segurança locais.")
    if registro["temp_c"] > 35:
        alertas.append("Calor extremo, mantenha-se hidratado, evite atividades físicas intensas no período mais quente e procure locais frescos ou sombreados.")
    if registro["temp_c"] < 10:
        alertas.append("Frio intenso, use roupas quentes, proteja mãos e pés, e evite exposição prolongada ao ar livre, especialmente crianças e idosos.")
    if registro["uv"] >= 8:
        alertas.append("Radiação ultravioleta alta, evite exposição direta ao sol entre 10h e 16h, use protetor solar, chapéu e óculos de sol.")

    return "; ".join(alertas) if alertas else ""

def enviar_email(destinatario, assunto, mensagem):
    msg = MIMEText(mensagem, "plain", "utf-8")
    msg["From"] = EMAIL_ORIGEM
    msg["To"] = destinatario
    msg["Subject"] = assunto

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_APP)
            server.sendmail(EMAIL_ORIGEM, destinatario, msg.as_string())
        print(f"📧 E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"⚠️ Erro ao enviar e-mail: {e}")
