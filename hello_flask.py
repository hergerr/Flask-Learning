from flask import Flask, render_template, request, escape
# moduł dodany do repozytorium uzetkowanika
from vsearch import search_for_letters

app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    dbconfig = {'host': '127.0.0.1',
                'user': 'vsearch',
                'password': 'vsearchpasswd',
                'database': 'vsearchlogDB', }
    import mysql.connector
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log 
                (phrase, letters, ip, browser_string, results)
                values  
                (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, req.user_agent.browser, res,))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Dane z formularza', 'Adres Klienta', 'Agent urzytkownika', 'Wyniki')
    return render_template('viewlog.html', the_title='Widok logu', the_row_titles=titles, the_data=contents)


@app.route('/search_for', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Oto twoje wyniki: '
    results = str(search_for_letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html', the_phrase=phrase, the_letters=letters, the_title=title, the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Witamy na stronie internetowej search4letters')


if __name__ == '__main__':
    app.run(debug=True)
