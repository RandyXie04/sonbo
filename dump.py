import sys
path = r'c:\users\sonbo\appdata\local\programs\python\python312\lib\site-packages\surya\recognition\__init__.py'
with open(path, 'r', encoding='utf-8') as fin:
    content = fin.read()
with open('test_surya_rec.txt', 'w', encoding='utf-8') as fout:
    fout.write(content)
