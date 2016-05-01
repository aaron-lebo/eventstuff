from bs4 import BeautifulSoup
import json
import wikipedia as wiki

events = {} 
for timeline in wiki.search('Timeline of the Syrian Civil War', results=14)[1:]:
    page = wiki.page(timeline)
    soup = BeautifulSoup(page.html(), 'html.parser')
    lis = soup.select('.toclevel-1')
    refs = lis.pop()
    for li in lis:
        month = li.contents.pop(0).contents[-1].text
        contents = []
        for item in li.contents[1]:
            if item.name:
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
                                a = soup.select('%s .external' % part.a['href'])[0]
                                refs.append({'text': a.text.strip('"'), 'href': a['href']})
                            else:
                                event += part.string 
                            if event.strip() and (not part.next_sibling or refs and part.next_sibling.name != 'sup'):
                                ps.append({'event': event.strip(), 'refs': refs})
                                event = ''
                                refs = []
                contents.append({item.a.contents[-1].text: ps}) 
        events[month] = contents
    break

file = open('events.json', 'wb')
file.write(json.dumps(events))
file.close()
