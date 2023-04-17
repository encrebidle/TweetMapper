from flask import Flask
from flask import request, render_template
from etlfunc import tweetretreive
from flask_jsonpify import jsonpify
app = Flask(__name__)

@app.route("/", methods= ['GET', 'POST'])
def index():
    if request.method == "POST":
        sword = request.form.get("sword") #
        fdate = request.form.get("fdate") #
        return "HEHEHEHEHEHEHEHEHEHEHEHEHEHEHEHEHEHEHEHEHE"
        
    return render_template("home.html")
        
        

@app.route("/<string:sword>/")

def form(sword):
    tweetretreive(sword,"2021-01-01")
    
    return "Done"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)