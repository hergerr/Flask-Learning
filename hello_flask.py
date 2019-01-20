from flask import Flask, render_template, request
# moduł dodany do repozytorium uzetkowanika
from vsearch import search_for_letters

app = Flask(__name__)


@app.route('/search_for', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Oto twoje wyniki: '
    results = str(search_for_letters(phrase, letters))
    return render_template('results.html', the_phrase=phrase, the_letters=letters, the_title=title, the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Witamy na stronie internetowej search4letters')


if __name__ == '__main__':
    app.run(debug=True)
