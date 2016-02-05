from flask import Flask, url_for, request, render_template, redirect
from glob import iglob
from lxml import etree
app = Flask(__name__)

xml = etree.parse('results.xml')
root = xml.getroot()
print('xml loaded!')

def get_sound_dict(sound):
    """
    Function to extract relevant data from a sound element. Returns a dictionary
    with author tags, crowd tags, description, ID, and file URL.
    """
    crowd_tags = [tag.attrib['label']
                  for tag in sound.xpath('./crowd-tags/tag/raw')]
    author_tags = [tag.attrib['label']
                   for tag in sound.xpath('./author-tags/tag')]
    return {'author_tags': '; '.join(author_tags),
            'crowd_tags': '; '.join(crowd_tags),
            'description': sound.find('description').text,
            'id': sound.attrib['id'],
            'file': sound.find('file').text}

################################################################################
# Possible queries
# ----------------
crowd = './sound[crowd-tags/tag/raw[@label="{}"]]'
author = './sound[author-tags/tag[@label="{}"]]'
description = './sound[description[contains(.,"{}")]]'

@app.route('/',methods=['GET'])
def main_page():
    """
    Function to display the main page. This is the first thing you see when you
    load the website.
    """
    get_or_post = request.method
    return render_template('index.html',
                                query = '',
                                kind = 'crowd',
                                sound = False)

@app.route('/search/', methods=['POST'])
def search():
    """
    Search function. Is called when the search form is submitted. Checks what kind
    of query the user makes, and selects the relevant results using XPATH.
    """
    global query
    global kind
    global results
    query = request.form['query']
    kind = request.form['kind']
    if query == 'all':
        return redirect('all/')
    elif kind == 'crowd':
        xpath_string = crowd.format(query)
    elif kind == 'author':
        xpath_string = author.format(query)
    elif kind == 'description':
        xpath_string = description.format(query)
    elif kind == 'ID':
        return redirect('id/' + query)
    else:
        xpath_string = None
    
    results = root.xpath(xpath_string) if not xpath_string is None else []
    
    return render_template('index.html',
                            query = query,
                            kind = kind,
                            sound = get_sound_dict(results[0]) if results else False,
                            num_results = len(results),
                            current = 1,
                            previous_item = None,
                            next_item = 1)

@app.route('/all/')
def all():
    """
    Function that is called when the user asks to display all entries in the corpus.
    """
    global results
    query = 'all'
    results = root.xpath('./sound')
    return render_template('index.html',
                            query = query,
                            kind = kind,
                            current = 1,
                            sound = get_sound_dict(results[0]),
                            num_results = len(results),
                            previous_item = None,
                            next_item = 1)

@app.route('/id/<id_number>')
def sound_page(id_number):
    """
    Function that is called when the user asks to display a page with a given ID.
    If the ID is not known, the website will display 'No sound with that ID.'
    """
    results = root.xpath('./sound[@id="{}"]'.format(id_number))
    if results:
        return render_template('index.html',
                                query = id_number,
                                kind = 'ID',
                                sound = get_sound_dict(results[0]),
                                previous_item = None,
                                next_item = None)
    else:
        return render_template('index.html',
                                query = id_number,
                                kind = 'ID',
                                sound = False)

def previous_and_next(number, num_results):
    """
    Function that takes the current sound index, and the number of results, and
    returns values for previous_item and next_item. If there is no previous or
    next, the return value is None.
    """
    max_number = num_results - 1
    if number < max_number:
        next_item = number + 1
    else:
        next_item = None
    if number > 0:
        previous_item = number - 1
    else:
        previous_item = None
    return previous_item, next_item

@app.route('/browse/<number>')
def browse(number):
    """
    Function that is called when the user browses through the results and presses
    either 'previous' or 'next'. If, for some reason, the user ends up on this page
    without having pressed 'previous' or 'next' the website will display a page with
    the relevant sound for the previous search. If the number exceeds the amount
    of results, the user gets redirected to the all-page.
    """
    number = int(number)
    num_results = len(results)
    if number in range(num_results):
        previous_item, next_item = previous_and_next(number, num_results)
        return render_template('index.html',
                                query = query,
                                kind = kind,
                                current = number + 1,
                                num_results = num_results,
                                sound = get_sound_dict(results[number]),
                                previous_item = previous_item,
                                next_item = next_item)
    else:
        return redirect('all/')

if __name__ == '__main__':
    app.debug = True
    app.run()
