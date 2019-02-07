from flask import Flask, render_template, request, session
from vsearch import search_for_letters
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
from checker import check_logged_in

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }

app.secret_key = 'ddwwqffttyrguky'


def log_request(req: 'flask_request', res: str) -> None:
    """Loguje szczegóły żądania sieciowego oraz wyniki"""

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log 
                (phrase, letters, ip, browser_string, results)
                values  
                (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, req.user_agent.browser, res,))


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    """Wyświetla logi wszystkim zalogowanym użytkownikom"""
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('Fraza', 'Litery', 'Adres Klienta', 'Agent urzytkownika', 'Wyniki')
        return render_template('viewlog.html', the_title='Widok logu', the_row_titles=titles, the_data=contents)
    except ConnectionError as err:
        print('Baza moze byc wyłączona. Error:', str(err))
    except CredentialsError as err:
        print('Problem z danymi uzytkownika', str(err))
    except SQLError as err:
        print('Problem z zapytaniem SQL. Error:', str(err))
    except Exception as err:
        print('Coś poszło nie tak. Error:', str(err))
    return 'ERROR'


@app.route('/search_for', methods=['POST'])
def do_search() -> 'html':
    """Odpowiada za wyswietlenie strony z wynikami wyszukiwania"""
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Oto twoje wyniki: '
    results = str(search_for_letters(phrase, letters))
    try:
        log_request(request, results)
    except Exception as err:
        print('Wystąpił błąd:', str(err))
    return render_template('results.html', the_phrase=phrase, the_letters=letters, the_title=title, the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Wyświetla strone startową"""
    return render_template('entry.html', the_title='Witamy na stronie internetowej search4letters')


@app.route('/login')
def login() -> str:
    session['logged in'] = True
    return 'Teraz jestes zalogowany'


@app.route('/logout')
def logout() -> str:
    session.pop('logged in')
    return 'Teraz jestes wylogowany'


if __name__ == '__main__':
    app.run(debug=True)
