from todo import create_app

if __name__ == "__main__":

    app = create_app()
    app.run(PORT='0.0.0.0')

