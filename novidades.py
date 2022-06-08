# Necessário instalar: pip install python-telegram-bot

from bs4 import BeautifulSoup
import requests
import csv
import os.path
import telegram
from datetime import datetime

windows_path = 'G:\\Projetos\\Python\\Novidades tech\\'

def spotify():
  url = 'https://engineering.atspotify.com/'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  file_path = windows_path + 'spotify_ids.csv'
  file_exists = os.path.exists(file_path)
  posts = soup.find_all('article')[1:]
  articles = []

  if len(posts) > 0:
    if not file_exists:
      with open(file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in range(len(posts)):
          writer.writerow([posts[i]['id']])
          articles.append({ 'id': posts[i]['id'], 'title': posts[i].find('a')['title'], 'link': posts[i].find('a')['href'], 'source': 'spotify' })
    else:
      ids = set()
      with open(file_path, encoding="utf8") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
          ids.add(line[0])

      with open(file_path, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(posts)):
          if posts[i]['id'] not in ids:
            writer.writerow([posts[i]['id']])
            articles.append({ 'id': posts[i]['id'], 'title': posts[i].find('a')['title'], 'link': posts[i].find('a')['href'], 'source': 'spotify' })
      if len(articles) == 0:
        articles.append({ 'no_new_articles': 'Sem artigo novo no blog do Spotify' })
  else:
    articles.append({ 'no_results': 'Não foi possível encontrar artigos no blog do Spotify'})

  return articles

def netflix():
  url = 'https://netflixtechblog.com/'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  file_path = windows_path + 'netflix_ids.csv'
  file_exists = os.path.exists(file_path)
  posts = soup.find_all(attrs={'data-post-id': True})
  articles = []

  if len(posts) > 0:
    if not file_exists:
      with open(file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in range(len(posts)):
          if posts[i].span is not None:
            writer.writerow([posts[i]['data-post-id']])
            title = posts[i].span.get_text()
            link = posts[i].a['href'].split('?source')[0]
            articles.append({ 'id': posts[i]['data-post-id'], 'title': title, 'link': link, 'source': 'netflix' })
    else:
      ids = set()
      with open(file_path, encoding="utf8") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
          ids.add(line[0])

      with open(file_path, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(posts)):
          if posts[i]['data-post-id'] not in ids:
            if posts[i].span is not None:
              writer.writerow([posts[i]['data-post-id']])
              title = posts[i].span.get_text()
              link = posts[i].a['href'].split('?source')[0]
              articles.append({ 'id': posts[i]['data-post-id'], 'title': title, 'link': link, 'source': 'netflix' })
      if len(articles) == 0:
        articles.append({ 'no_new_articles': 'Sem artigo novo no blog da Netflix' })
  else:
    articles.append({ 'no_results': 'Não foi possível encontrar artigos no blog da Netflix'})

  return articles

def github():
  url = 'https://github.blog/category/engineering/'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  file_path = windows_path + 'github_ids.csv'
  file_exists = os.path.exists(file_path)
  posts = soup.find_all('article', {'class': ['post', 'type-post', 'status-publish']})
  articles = []

  if len(posts) > 0:
    if not file_exists:
      with open(file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in range(len(posts)):
          writer.writerow([posts[i]['id']])
          link = posts[i].find('a', class_="Link--primary")
          articles.append({ 'id': posts[i]['id'], 'title': link.get_text(), 'link': link['href'], 'source': 'github' })
    else:
      ids = set()
      with open(file_path, encoding="utf8") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
          ids.add(line[0])

      with open(file_path, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(posts)):
          if posts[i]['id'] not in ids:
            writer.writerow([posts[i]['id']])
            link = posts[i].find('a', class_="Link--primary")
            articles.append({ 'id': posts[i]['id'], 'title': link.get_text(), 'link': link['href'], 'source': 'github' })
      if len(articles) == 0:
        articles.append({ 'no_new_articles': 'Sem artigo novo no blog do Github' })
  else:
    articles.append({ 'no_results': 'Não foi possível encontrar artigos no blog do Github' })
  return articles

def twitter():
  url = 'https://blog.twitter.com/engineering/en_us/topics/insights'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  file_path = windows_path + 'twitter_ids.csv'
  file_exists = os.path.exists(file_path)
  posts = soup.find_all('div', {'class': ['result__copy']})
  articles = []

  if len(posts) > 0:
    if not file_exists:
      with open(file_path, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for i in range(len(posts)):
          writer.writerow([posts[i].a.get_text()])
          articles.append({ 'title': posts[i].a.get_text(), 'link': 'https://blog.twitter.com/' + posts[i].a['href'], 'source': 'twitter' })
    else:
      titles = set()
      with open(file_path, encoding="utf8") as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
          titles.add(line[0])

      with open(file_path, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(posts)):
          if posts[i].a.get_text() not in titles:
            writer.writerow([posts[i].a.get_text()])
            articles.append({ 'title': posts[i].a.get_text(), 'link': 'https://blog.twitter.com/' + posts[i].a['href'], 'source': 'twitter' })
      if len(articles) == 0:
        articles.append({ 'no_new_articles': 'Sem artigo novo no blog do Twitter' })
  else:
    articles.append({ 'no_results': 'Não foi possível encontrar artigos no blog do Twitter'})

  return articles

def send_message(articles):
  token_path = windows_path + 'TELEGRAM_TOKEN.txt'
  user_id_path = windows_path + 'USER_ID.txt'

  token_file = open(token_path, 'r')
  user_id_file = open(user_id_path, 'r')
  telegram_token = token_file.read()
  user_id = user_id_file.read()
  bot = telegram.Bot(token=telegram_token)

  if len(articles) == 1:
    text = articles[0]['no_results']
  else:
    for article in articles:
      text = '<b>Novo texto no blog: ' + article['source'].upper() + '</b>\n\n'
      text += article['title'] + '\n' + article['link']

  bot.send_message(chat_id=user_id, text=text, parse_mode='HTML')

  token_file.close()
  user_id_file.close()

def main():
  spotify_articles = spotify()
  netflix_articles = netflix()
  github_articles = github()
  twitter_articles = twitter()
  log_path = windows_path + 'novidades_tech_log.txt'
  log_message = ''

  for article in [spotify_articles, netflix_articles, github_articles, twitter_articles]:
    if len(article) == 1 and 'no_new_articles' in article[0]:
      log_message += article[0]['no_new_articles'] + ' em ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + '\n'
    else:
      send_message(article)
      source = article[0]['source'].title()
      log_message += 'Artigo do blog ' + source + ' enviado no telegram em ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + '\n'

    with open(log_path, 'w', encoding='UTF8') as log_file:
      log_file.write(log_message)

main()