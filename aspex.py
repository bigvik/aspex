import os
import sys, time
import csv
import json
import urllib.request



input = 'aspex.csv'
output  = 'output.csv'
prefix = 'https://site.com/'

if not os.path.exists('files'):
    os.makedirs('files')


def prepare(file):
    with open(file, 'r') as f:
        fd = f.read()
        fd = fd.replace('},{', '};{')
    with open(file, 'w') as f:
        f.write(fd)

def save_img(url, name):
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0"
    req = urllib.request.Request(url, headers={'User-Agent': useragent} )
    with open(name, "wb") as f:
        with urllib.request.urlopen(req) as r:
            print(f"Сохранение файла: {name}", end='\r', file=sys.stdout, flush=True)
            f.write(r.read())

def main():
    prepare(input)
    with open(input, 'r') as readfile, open(output, 'w', newline='') as writefile:
        reader = csv.DictReader(readfile, delimiter=';', quotechar='"')
        fieldnames = ["URL","vendor","model","sku","upc","!sort","category","category 2","gender","gender 2","age","status","frame color","frame color 2","color code","price","size","bridge","B","ED","temple","t","shape","rim type","lens material","temple material","img1","img2","img3"]
        writer = csv.DictWriter(writefile, fieldnames = fieldnames, delimiter=';')
        writer.writeheader()
        rows = []
        for row in reader:
            counter = 1
            for line in row['img1'].split(';'):
                d = json.loads(line)
                url = d['url']
                filename = f"files/{row['vendor']}_{row['model']}_{row['upc']}_{counter}.jpg"
                save_img(url, filename)
                row[f'img{counter}'] = f'{prefix}{filename}'
                counter +=1
            rows.append(row)
        writer.writerows(rows)
           
        
if __name__=="__main__":
    main()