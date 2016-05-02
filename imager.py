from lxml import etree
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


dates = {}
sources = {}

tree = etree.parse('events.xml')
sentences = tree.findall('Sentence')
for sentence in sentences:
    date = sentence.get('date')
    if not dates.get(date):
        dates[date] = {'count': 0, 'refs': 0, 'sources': []} 
    dates[date]['count'] += 1
    for ref in sentence.findall('Ref'):
        dates[date]['refs'] += 1 
        source = ref.get('source')
        if source:
            if not sources.get(source):
                sources[source] = 0
            sources[source] += 1
            if not source in dates[date]['sources']:
                dates[date]['sources'].append(source)

for date in dates:
    dates[date]['sources'] = len(dates[date]['sources'])

#print len(sentences)
#print sources
#print dates 

f = open('events.csv', 'wb')
for k in sorted(dates):
    v = dates[k]
    if k.startswith('2012'):
        f.write('%s %s %s %s\n' % (k, v['count'], v['refs'], v['sources']))

f.close()
