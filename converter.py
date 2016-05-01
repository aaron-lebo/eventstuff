from lxml import etree

root = etree.Element('Sentences')
sentence = etree.Element(
    'Sentence',
    date = '20110101',
    id = '',
    source = '',
    sentence = 'True'
)
root.append(sentence)
print etree.tostring(root, pretty_print=True)
