import os

f = open('history.txt')
data = f.read()
f.close()

newdata = data.replace('\n', '')
arr = newdata.split('。')

fout = open('input.txt', 'w')
for line in arr:
    fout.write(line+'。\n')
fout.close()
