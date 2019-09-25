from api import API

app = API()


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"