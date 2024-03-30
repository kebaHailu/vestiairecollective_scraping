values = {
    'men': ['men','#gender=Men%232',10],
    'women': ['women','#gender=Women%231',16],
    'kids': ['kids','#gender=Kids%233',21],
    'we-love': ['we-love','',21],
    'new-items': ['new-items','',21]
}

def get_url(value,cur):
    return f'https://www.vestiairecollective.com/{value[0]}/p-{cur}/{value[1]}'

urls = []
urls.append('https://www.vestiairecollective.com/vintage/')
urls.append('https://www.vestiairecollective.com/we-love/')
urls.append('https://www.vestiairecollective.com/kids/')
urls.append('https://www.vestiairecollective.com/men/')
urls.append('https://www.vestiairecollective.com/women/')
urls.append('https://www.vestiairecollective.com/new-items/')
for val in values.values():
    for i in range(2,val[2]+1):
        urls.append(get_url(val,i))


for url in urls:
    print(url.split('/')[3])
