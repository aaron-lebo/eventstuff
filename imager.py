from lxml import etree

dates = {}
sources = {}

tree = etree.parse('events.xml')
sentences = tree.findall('Sentence')
for sentence in sentences:
    date = sentence.get('date')
    if not dates.get(date):
        dates[date] = {'count': 0, 'refs': 0, 'sources': []} 
    date = dates[date]
    date['count'] += 1
    for ref in sentence.findall('Ref'):
        date['refs'] += 1 
        source = ref.get('source')
        if source:
            if not sources.get(source):
                sources[source] = 0
            sources[source] += 1
            if not source in date['sources']:
                date['sources'].append(source)

for date in dates:
    dates[date]['sources'] = len(dates[date]['sources'])

print len(sentences)
#print sources
#print dates 
