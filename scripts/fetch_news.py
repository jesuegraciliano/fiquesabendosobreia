import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Função para obter as notícias
def fetch_news(api_key, query="Artificial Intelligence"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    return response.json()

# Função para enviar e-mail
def send_email(subject, body):
    from_email = os.getenv("EMAIL_FROM")
    to_email = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASSWORD")
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

# Função principal
def main():
    # Carregar as chaves de API do GitHub Secrets
    newsapi_key = os.getenv("NEWSAPI_KEY")
    gnewsapi_key = os.getenv("GNEWS_API_KEY")
    currentsapi_key = os.getenv("CURRENTSAPI_KEY")
    
    # Obter notícias de todas as APIs
    newsapi_response = fetch_news(newsapi_key)
    gnewsapi_response = fetch_news(gnewsapi_key)  # Assumindo que a lógica para GNews seja semelhante
    currentsapi_response = fetch_news(currentsapi_key)  # Assumindo que a lógica para CurrentsAPI seja semelhante
    
    # Processar as notícias e montar o corpo do e-mail
    articles = []
    articles.extend(newsapi_response['articles'][:5])
    articles.extend(gnewsapi_response['articles'][:5])
    articles.extend(currentsapi_response['news'][:5])
    
    body = "<h1>Notícias sobre Inteligência Artificial</h1><ul>"
    for article in articles[:5]:
        body += f'<li><a href="{article["url"]}">{article["title"]}</a><p>{article["description"]}</p></li>'
    body += "</ul>"
    
    # Enviar o e-mail
    send_email("Top 5 Notícias sobre Inteligência Artificial", body)

if __name__ == "__main__":
    main()
