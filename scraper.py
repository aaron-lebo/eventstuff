from bs4 import BeautifulSoup
import json
import os
import wikipedia as wiki

def run(page):
    events = {}
    soup = BeautifulSoup(page.html(), 'html.parser')
    lis = soup.select('.toclevel-1')
    if lis[0].a['href'] == '#Timeline':
        lis = soup.select('.toclevel-2')

    refs = lis.pop()
    for li in lis:
        if li.a['href'] in ('#References', '#See_also'):
            continue

        try:
            items = li.contents[1]
        except:
            items = soup.select('.toclevel-2')

        contents = []
        for item in items:
            if hasattr(item, 'name') and item.name:
                ps = []
                for sib in soup.select(item.a['href'])[0].parent.next_siblings:
                    if sib.name in ('h2', 'h3'):
                        break
                    if sib.name:
                        if sib.name == 'ul':
                            sib = sib.contents[0]
                        event, refs = '', [] 
                        for part in sib.contents:
                            if not part.string:
                                continue
                            if part.name == 'sup':
                                a = soup.select('%s .external' % part.a['href'])
                                if a:
                                    a = a[0]
                                    refs.append({'text': a.text.strip('"'), 'href': a['href']})
                            else:
                                event += part.string 
                            if event.strip() and (not part.next_sibling or refs and part.next_sibling.name != 'sup'):
                                ps.append({'event': event.strip(), 'refs': refs})
                                event = ''
                                refs = []

                contents.append({item.a.contents[-1].text: ps}) 
        events = contents

    return events

for timeline in wiki.search('Timeline of the Syrian Civil War', results=14)[1:]:
    page = wiki.page(timeline)
    path = '%s.json' % page.url.split('/')[-1]
    if os.path.exists(path):
        continue

    title = page.title
    if '2015' in title or '2016' in title:
        continue

    print title + ' START'

    events = run(page)
    file = open(path, 'wb')
    file.write(json.dumps(events, sort_keys=True, indent=4))
    file.close()

    print title + ' END'
