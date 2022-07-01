from application import app

# Para correr en debug mode
# docker run -it -p 8000:80 flaskapp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)