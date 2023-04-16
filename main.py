from flask import Flask
from flask import request
from etlfunc import tweetretreive
from flask_jsonpify import jsonpify
app = Flask(__name__)

@app.route("/")
def index():
    sword = request.args.get("sword", "")
    if sword:
        result = form(sword)
    else:
        result = ""
    return (
        """<form action="" method="get">
                <input type="text" name="sword">
                <input type="submit" value="Generate Data">
            </form>"""
        +  result
    )

@app.route("/<string:sword>/")

def form(sword):
    tweetretreive(sword,"2021-01-01")
    
    return "Done"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)