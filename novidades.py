from bs4 import BeautifulSoup
import requests
import csv
import os.path

def spotify():
  url = 'https://engineering.atspotify.com/'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  file_exists = os.path.exists('spotify_ids.csv')
  posts = soup.find_all('article')[1:]
  articles = []

  if not file_exists:
    with open('spotify_ids.csv', 'w', encoding='UTF8') as f:
      writer = csv.writer(f)
      for i in range(len(posts)):
        writer.writerow([posts[i]['id']])
        articles.append({ 'id': posts[i]['id'], 'title': posts[i].find('a')['title'], 'link': posts[i].find('a')['href'] })
  else:
    ids = set()
    with open('spotify_ids.csv', encoding="utf8") as f:
      csv_reader = csv.reader(f)
      for line in csv_reader:
        ids.add(line[0])

    with open('spotify_ids.csv', 'a', encoding='UTF8') as f:
      writer = csv.writer(f)
      for i in range(len(posts)):
        if posts[i]['id'] not in ids:
          writer.writerow([posts[i]['id']])
          articles.append({ 'id': posts[i]['id'], 'title': posts[i].find('a')['title'], 'link': posts[i].find('a')['href'] })

  return articles

def netflix():
  url = 'https://netflixtechblog.com/'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  file_exists = os.path.exists('netflix_ids.csv')
  posts = soup.find_all(attrs={'data-post-id': True})
  articles = []

  if not file_exists:
    with open('netflix_ids.csv', 'w', encoding='UTF8') as f:
      writer = csv.writer(f)
      for i in range(len(posts)):
        if posts[i].span is not None:
          writer.writerow([posts[i]['data-post-id']])
          title = posts[i].span.get_text()
          articles.append({ 'id': posts[i]['data-post-id'], 'title': title, 'link': posts[i].a['href'] })
  else:
    ids = set()
    with open('netflix_ids.csv', encoding="utf8") as f:
      csv_reader = csv.reader(f)
      for line in csv_reader:
        ids.add(line[0])

    with open('netflix_ids.csv', 'a', encoding='UTF8') as f:
      writer = csv.writer(f)
      for i in range(len(posts)):
        if posts[i]['data-post-id'] not in ids:
          if posts[i].span is not None:
            writer.writerow([posts[i]['data-post-id']])
            title = posts[i].span.get_text()
            articles.append({ 'id': posts[i]['data-post-id'], 'title': title, 'link': posts[i].a['href'] })

  return articles

# def github():

def twitter():
  url = 'https://blog.twitter.com/engineering/en_us/topics/insights'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  file_exists = os.path.exists('twitter_ids.csv')
  posts = soup.find_all('div', {'class': ['result__copy']})
  articles = []

  if not file_exists:
    with open('twitter_ids.csv', 'w', encoding='UTF8') as f:
      writer = csv.writer(f)
      for i in range(len(posts)):
        writer.writerow([posts[i].a.get_text()])
        articles.append({ 'title': posts[i].a.get_text(), 'link': 'https://blog.twitter.com/' + posts[i].a['href'] })
  else:
    titles = set()
    with open('twitter_ids.csv', encoding="utf8") as f:
      csv_reader = csv.reader(f)
      for line in csv_reader:
        titles.add(line[0])

    with open('twitter_ids.csv', 'a', encoding='UTF8') as f:
      writer = csv.writer(f)
      for i in range(len(posts)):
        if posts[i].a.get_text() not in titles:
          writer.writerow([posts[i].a.get_text()])
          articles.append({ 'title': posts[i].a.get_text(), 'link': 'https://blog.twitter.com/' + posts[i].a['href'] })

  return articles

def main():
  # new_spotify_articles = spotify()
  # new_netflix_articles = netflix()
  # new_github_articles = github()
  new_twitter_articles = twitter()
  # print(new_twitter_articles)

  # cheguei aqui já com o dictionary articles contendo os valores a serem enviados

main()