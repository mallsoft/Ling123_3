import xml.etree.ElementTree as ET
import xml.dom.minidom as mdom

"""
    read and strip the poem, making a list of lines for each stanza
"""
with open('shake.txt',mode='r',encoding='utf-8') as poem:    
    poem_arr = [[]]
    for idx,line in enumerate(poem):
        if len(line) > 1:
            poem_arr[len(poem_arr)-1].append(line.split())
        else:
            poem_arr.append([])

"""
    to create all the needed numbers and letters we use a...
    ...beautifull 3x nested loop
    go trough each stanza:
        -> keep count on what stanza and token we are looking at
        -> create a <stanza> that we can append a child to
        go trough each line in the stanza:
            go trough all tokens in a line:
            -> Generate token / wordform / rhyme and combine
            -> append what we made to the stanza we created
        -> add the stanza tag to the poem
"""

poem = ET.Element('poem') #ROOT <poem>

stanza_idx = 0
for stanza in poem_arr:
    stanza_idx += 1
    token_idx = 0 # token_idx is defined here so it is relative to each stanza

    stanza_TAG = ET.Element('stanza',{'s-id':f"{stanza_idx}"})

    for idx,line in enumerate(stanza):
        for token in line:

            rhyme = ['A','A','B','C','C','B'][idx%6] #pattern
            token_idx += 1

            token_TAG = ET.Element('token',{'t-id':f'{stanza_idx}-{token_idx}'})
            
            wform = ET.SubElement(token_TAG,'wordform')
            rhym = ET.SubElement(token_TAG,'rhyme')

            wform.text = token
            rhym.text = rhyme
            
            stanza_TAG.append(token_TAG)
    poem.append(stanza_TAG)

"""
    there is probably a better way do add dtd and prettify
    but below is how i did it.
"""

elementTreeString = ET.tostring(poem,encoding="unicode",method='xml')
dtd_inline = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<!DOCTYPE poem[
    <!ELEMENT poem (stanza)+>
    <!ELEMENT stanza (token)+>
    <!ATTLIST stanza s-id CDATA #REQUIRED>
    <!ELEMENT token (wordform,rhyme)>
    <!ATTLIST token t-id CDATA #REQUIRED>
    <!ELEMENT wordform (#PCDATA)>
    <!ELEMENT rhyme (#PCDATA)>
]>
"""
xmlString = dtd_inline + elementTreeString
xmlPretty = mdom.parseString(xmlString).toprettyxml()


#only data
# print(elementTreeString)
#all of it...
# print(xmlString)
#pretty version
print(xmlPretty)

# write it to a file ?
with open("poem.xml",mode="w+",encoding="utf-8") as xmlfile:
    xmlfile.write(xmlPretty)
