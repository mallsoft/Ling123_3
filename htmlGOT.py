from bs4 import BeautifulSoup as bs
from bs4 import Comment

""" 
    open the got.html file
    and parse the provided file as html 
"""
file = open("got.html",mode="r",encoding="utf-8")
html = bs(file,'html.parser')
file.close()


""" unicorn """
unicorn = f"""<!--{html.find_all(text=lambda text:isinstance(text, Comment))[0]}-->"""


""" title """
title = f"<h1>{html.find('title').string}</h1>"
# this part is needed for valid html5
head_title = f"<title>{html.find('title').string}</title>"


""" keywords """
keywords = f"<p>Keywords: <span>{html.find('meta',{'name':'keywords'})['content']}</span></p>"


""" paragraphs """
article_text = [p.get_text() for p in html.findAll('p')][:-1] #-1 skips the "contact us part"
paragraphs = "<ul>"
for paragraph in article_text:
    # create the list items <li>
    paragraphs += f"<li>{paragraph}</li>"
paragraphs += "</ul>"


""" cascading stylesheet """
style = """<style>
    h1 {
        text-decoration:underline;
    }
    p > span {
        color:red;
        }
    ul {
        list-style-type: square;
        }
</style>"""


"""
    creating the html structure
    by combining the parts

    !! notice that the task did not specify that
    a title should be inserted into the document
    but is required (nonempty) for valid html5
"""
clean_html = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8"> 
        {head_title}
        {style}
    </head>
    <body>
        {title}
        {keywords}
        {paragraphs}
    </body>
</html>
"""


""" 
    create a document using the beautiful soup constructor,
    so we can make it pretty without too much work
"""
clean_and_pretty = bs(clean_html,features='html.parser').prettify()


""" create file and write this to 'got_clean.html' """
with open("got_clean.html",mode="w+",encoding="utf-8") as clean:
    clean.write(clean_and_pretty)
