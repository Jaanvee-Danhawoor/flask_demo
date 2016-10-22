from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/test')
def test():
    return 'Hello World!'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return "I am still working on this"


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template("hello.html", name=name)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")


@app.route('/results')
def results():
    search_term = session['search_term']
    page = get_page(search_term)
    return render_template("results.html", page=page)


def get_page(search_term):
    try:
        page = wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        # no such page, return a random one
        page = wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError:
        # this is a disambiguation page, get the first real page (close enough)
        page_titles = wikipedia.search(search_term)
        # sometimes the next page has the same name (different caps), so don't try the same again
        if page_titles[1].lower() == page_titles[0].lower():
            title = page_titles[2]
        else:
            title = page_titles[1]
        page = get_page(wikipedia.page(title))
    return page


if __name__ == '__main__':
    app.run()
