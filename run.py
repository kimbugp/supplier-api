from app import create_app

application = create_app()
if application.config['ENV'] == "development":
    application.run(
        host=application.config['HOST'], port=application.config['PORT'], debug=True)
    print(
        f'''Server running on http://{application.config['HOST']}:{application.config['PORT']} ''')
