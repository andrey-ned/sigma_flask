from webapp import app


# App configs
app.run(
	debug=True, # Delete if want to use in Production
    host=app.config.get('HOST', '0.0.0.0'),
    port=app.config.get('PORT', 5000)
)