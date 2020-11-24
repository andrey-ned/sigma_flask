import sqlite3
from flask import render_template, request, redirect, jsonify, g, url_for
from webapp import app


# App processors
@app.before_request
def init_db():
    """
    init_db
    pre-proc before request
    for connect db
    """
    g.db = sqlite3.connect("db.sqlite3")


@app.after_request
def close_db(r):
    """
    close_db
    after-proc after request
    for close db
    """
    g.db.commit()
    g.db.close()
    return r
# End

@app.route('/', methods=('GET', 'POST'))
def show():
    """
    show
    view of main page
    """
    cursor = g.db.execute("select * from currency order by date desc")
    values = cursor.fetchall()
    return render_template('index.html', values=values)


@app.route('/add/', methods=('GET', 'POST'))
def add():
    """
    add
    view of adding page
    """
    if request.method == 'POST':
        date = request.form.get('date')
        buy_usd = float(request.form.get('buy_usd'))
        sell_usd = float(request.form.get('sell_usd'))
        cursor = g.db.execute("insert into currency (date, buy_usd, sell_usd) values (?, ?, ?)", [date, buy_usd, sell_usd])
        return redirect('/')
    return render_template('forms.html', head='Добавить данные', key='Добавить')


@app.route('/delete/', methods=['POST'])
def delete():
    """
    delete
    """
    if request.method == 'POST':
        id_ = request.form.get('id_')
        cursor = g.db.execute("delete from currency where id=?", (id_,))
        return redirect('/')


@app.route('/<int:id_>/edit', methods=['GET', 'POST'])
def update(id_):
    """
    update
    view of update page
    """
    if request.method == 'POST':
        date = request.form.get('date')
        buy_usd = float(request.form.get('buy_usd'))
        sell_usd = float(request.form.get('sell_usd'))
        g.db.execute("update currency set date=?, buy_usd=?, sell_usd=? where id==?", (date, buy_usd, sell_usd, id_))
        return redirect('/')
    return render_template('forms.html', head='Обновить данные', key='Обновить')


@app.route('/charts/', methods=['GET', 'POST'])
def charts():
    """
    charts
    view of charts page
    """
    cursor = g.db.execute("select * from currency")
    values = cursor.fetchall()
    return render_template('charts.html', values=values)


@app.route("/get/", methods=['GET'])
def get_all():
    """
    get_all
    return json for creating charts
    """
    cursor = g.db.execute("select id, date, buy_usd, sell_usd from currency order by date desc")
    values = cursor.fetchall()
    values = [{"id": id_, "date": date, "buy_usd": buy, "sell_usd": sell}
              for id_, date, buy, sell in values]
    return jsonify(values)


with app.test_request_context():
    print(url_for('show'))
    print(url_for('add'))
    print(url_for('update', id_='2'))
    print(url_for('get_all'))
