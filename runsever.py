from project import app

if __name__ == '__main__':
    app.debug = True

    app.run(host ="192.168.50.99",port =5001)