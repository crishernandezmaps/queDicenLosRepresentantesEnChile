#!/usr/bin/python3
import requests as req
from bs4 import BeautifulSoup as S
import time
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd

# printing with less effort
p = print

# hiding
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# list holding representantes twitter screen_name
representantes = []

# getting Senadorxs
senado = 'http://www.senado.cl/prontus_senado/site/edic/base/port/senadores.html'
soupS = S(((req.get(senado)).content),'lxml')
for i in soupS.find_all('div', class_='s0'):
    preS = senado.split('/prontus_senado')[0]
    sufxS = i.find('a').get('href')
    each_senadxr = "".join([preS,sufxS])
    new_soupS = S(((req.get(each_senadxr)).content),'lxml')
    twitter_senador = new_soupS.find_all('h3')[2].findNext('ul').findNext('li').find('a').get('href')
    if(twitter_senador[7:14] == 'twitter'):
        ts = twitter_senador.split('.com/')[1]
        representantes.append(ts)
        p(ts)

# getting Diputadxs
diputados = 'https://www.camara.cl/camara/diputados.aspx#tab'
soupD = S(((req.get(diputados)).content),'lxml')
for k in soupD.find(id='ctl00_mainPlaceHolder_pnlComposicion').find_all('a'):
    if(k.get('href')[0:9] == 'diputado_'):
        preD = diputados.split('/diputados')[0]
        sufxD = "".join(['/',k.get('href')])
        each_diputadx = "".join([preD,sufxD])

        new_soupD = S(((req.get(each_diputadx)).content),'lxml')
        nombre_diputadx = new_soupD.find(id='ficha').find('h3').get_text()
        cargo_nombre_apellido = word_tokenize(nombre_diputadx)
        cargo_nombre_apellido_t = "%20".join(cargo_nombre_apellido[0:3])
        busqueda = "".join(['https://twitter.com/search?f=users&vertical=default&q=',cargo_nombre_apellido_t,'&src=typd'])

        soupG = S(((req.get(busqueda, headers = headers)).content),'lxml')
        diputadx_t = soupG.find('b', class_='u-linkComplex-target')
        if(diputadx_t is not None):
            td = diputadx_t.get_text()
            representantes.append(td)
            p(td)
    time.sleep(3)


df = pd.DataFrame(representantes)
df.to_csv('users.csv',sep=',')
p(df)


'''
Método
- Se obtiene el nombre de usuario de cada Senadxr de aquellos que hacen pública su cuenta en Senado.cl
- Se obtiene el nombre de cada Diputado en Camara.cl. Luego con ese nombre se realiza una búsquea programática en Twitter para obtener el nombre de usuario en dicha red social, ya que no se publican "enlaces" como es el caso de la web del Senado.
- Finalmente se guarda en un archivo .CSV todos los nombre de usuario de los representantes chilenos en el Congreso.

La ventaja de realizar esta búsqueda de forma programática es que se actualiza de acuerdo a los cambios que se realicen en las fuentes de información, sin información de intervención manual.
'''
