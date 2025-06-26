from bs4 import BeautifulSoup
import requests


# url = 'https://webscraper.io/test-sites/tables'
# response = requests.get(url)
# soup = BeautifulSoup(response.content)

# img = soup.find_all('img')
# print(img)
# print(img[0]['src'])
# print(img[0]['alt'])

# table = soup.find_all('table')[1]
# rows = table.find_all('tr')[1:]
# print('**********************')

# last_names = []
# for row in rows:
#     last_names.append(row.find_all('td')[2].get_text())
# print(last_names)

# print('**********************')


########################################

# url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
# response = requests.get(url)
# soup = BeautifulSoup(response.content)
# table = soup.find(class_="wikitable")
# rows = table.find_all('tr')[1:]

# mutable_list = []
# immutable_list = []
# for row in rows:
#     mutability = row.find_all('td')[1].get_text().strip()
#     type = row.find_all('td')[0].get_text().strip()
#     if mutability == 'immutable':
#         immutable_list.append(type)
#     else:
#         mutable_list.append(type)

# print(mutable_list)
# print(immutable_list)