from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/test", methods=["GET", "POST", "PUT", "DELETE"])
def test():
    print "Raw data: ", request.data
    print "Form keys: ", request.form.keys()
    return "OK"

if __name__ == "__main__":
    app.debug = True
    app.run()
