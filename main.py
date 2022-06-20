import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.sec.gov/forms'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
data = []
table = soup.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
hrefs = []
for row in rows:
    cols = row.find_all('td')
    hrefs.append('https://www.sec.gov' + str(cols[1].find('a').get('href')))
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

df = pd.DataFrame(data, columns=['Number', 'Description', 'Last Updated', 'SEC Number', 'Topic(s)'])
df = df.apply(lambda x: [ele.split(sep=':')[1] for ele in x])

df = pd.concat([df, pd.Series(hrefs, name='PDF')], axis=1)

print(df)
df.to_excel('forms.xlsx', index=False)

