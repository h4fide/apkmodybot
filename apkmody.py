import requests
import bs4 as bs

m_url = 'https://apkmody.io'

class Mody():
    def __init__(self):
        self.search = self.search
        self.items = self.items
        self.dlurl = self.dlurl
    def search(search):
        req = requests.get(f'{m_url}/?s={search}')
        soup = bs.BeautifulSoup(req.text, 'html.parser')
        data = []
        resultes = soup.find_all('div', class_='flex-item')
        for result in resultes:
            title = result.find('h2', class_='truncate').text
            ver_m = result.find('p' , class_='card-excerpt has-small-font-size truncate').text
            version = ver_m.replace('\n', '').split('•')[0]
            mod = ver_m.replace('\n', '').split('•')[1][1:]
            link =  result.find('a')['href']
            image = result.find('img')['src']
            data.append({'title': title, 'version': version, 'mod': mod, 'link': link, 'image': image})
        return data

    def items(url):
        f_url ='https://download.apkmody.fun'
        req = requests.get(f'{url}/download', timeout=10)
        soup = bs.BeautifulSoup(req.text, 'html.parser')
        results = soup.find_all('a', class_='clickable')
        data = []
        for result in results[:-2][1:]:
            link = result['href']
            name = result.find('div', class_='has-vivid-cyan-blue-color').text
            data.append({'name': name, 'link': f_url+link})
        return data

    def dlurl(url):
        req = requests.get(url, timeout=10)
        soup = bs.BeautifulSoup(req.text, 'html.parser')
        results = soup.find_all('a', id='download-button')
        data = []
        for result in results:
            data.append(result['href'])
        return data[0]


