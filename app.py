import sqlite3
from flask import Flask, render_template, request, redirect, jsonify, g, url_for


app = Flask(__name__)


@app.before_request
def init_db():
	g.db = sqlite3.connect("db.sqlite3")


@app.after_request
def close_db(r):
	g.db.commit()
	g.db.close()
	return r


@app.route('/',  methods=('GET', 'POST'))
def show():
	cursor = g.db.execute("select * from currency order by date desc")
	values = cursor.fetchall()
	return render_template('index.html', values=values)


@app.route('/add/',  methods=('GET', 'POST'))
def add():
	print(request.method)
	if request.method == 'POST':
		date = request.form.get('date')
		buy_usd = float(request.form.get('buy_usd'))
		sell_usd = float(request.form.get('sell_usd'))
		cursor = g.db.execute("insert into currency (date, buy_usd, sell_usd) values (?, ?, ?)", [date, buy_usd, sell_usd])
		return redirect('/')
	return render_template('forms.html', head='Добавить данные')


@app.route('/delete/',  methods=['POST'])
def delete():
	if request.method == 'POST':
		id_ = request.form.get('id_')
		cursor = g.db.execute("delete from currency where id=?", (id_,))
		return redirect('/')


@app.route('/<int:id_>/edit',  methods=['GET', 'POST'])
def update(id_):
	if request.method == 'POST':
		date = request.form.get('date')
		buy_usd = float(request.form.get('buy_usd'))
		sell_usd = float(request.form.get('sell_usd'))
		g.db.execute("update currency set date=?, buy_usd=?, sell_usd=? where id==?", (date, buy_usd, sell_usd, id_))
		return redirect('/')
	return render_template('forms.html', head='Обновить данные')	


@app.route('/charts/',  methods=['GET', 'POST'])
def charts():
	cursor = g.db.execute("select * from currency")
	values = cursor.fetchall()
	return render_template('charts.html', values=values)


@app.route("/get/", methods=['GET'])
def get_all():
    cursor = g.db.execute("select id, date, buy_usd, sell_usd from currency order by date desc")
    values = cursor.fetchall()
    values = [{"id": id_, "date": date, "buy_usd": buy, "sell_usd": sell}
        for id_, date, buy, sell in values]
    return jsonify(values)