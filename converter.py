import glob
import json
from lxml import etree

MONTHS = dict(
    January = '01',
    February = '02',
    March = '03',
    April = '04',
    May = '05',
    June = '06',
    July = '07',
    August = '08',
    September = '09',
    October = '10',
    November = '11',
    December = '12'
)

root = etree.Element('Sentences')

for n, path in enumerate(glob.glob('*.json')):
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    for n2, events in enumerate(data.items()):
        date = events[0].split()
        date2 = []
        for part in date: 
            idx = part.find(u'\u2013')
            if idx != -1:
                part = part[:idx]
            date2.append(part)

        date = date2
        try:
            int(date[0])
        except:
            date.reverse()

        if len(date[0]) == '4':
            continue

        year = path[-10:-6]
        for n3, event in enumerate(events[1]):
            day = date[0]
            day = day if len(day) == 2 else '0' + day
            if not event['refs']:
                continue

            ref = event['refs'][0]
            sentence = etree.Element(
                'Sentence',
                date = '%s%s%s' % (year, day, MONTHS[date[1]]),
                id = '%s.%s.%s' % (n, n2, n3),
                source = ref['source'] or ref['href'],
                sentence = 'True'
            )
            text = etree.Element('Text')
            text.text = event['event']
            sentence.append(text)
            root.append(sentence)

f = open('events.xml', 'wb')
f.write(etree.tostring(root, pretty_print=True))
f.close()
