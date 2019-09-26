from api import API

app = API()


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/book")
class BooksHandler:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"