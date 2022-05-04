from django.shortcuts import redirect
from flask import *
from requests_html import HTMLSession

SECRET_KEY = "super secret"

app = Flask(__name__)


@app.route("/", methods= ["POST", "GET"])
def the_landing_page():
    if request.method == "POST":
        user = request.form["name"]
        return redirect(url_for("get_some_details", name=user))
    else:
        user = request.args.get("name")
        return render_template("index.html")

@app.route("/<string:name>")
def get_some_details(name):
    dict1 = {}
    url = f"https://www.google.com/search?q={name}"
    session = HTMLSession()
    r = session.get(url)
    div_tag = r.html.find("div.kno-rdesc")
    for tag in div_tag:
        summary = tag.find("span")
        summary_text = summary[0].text
        dict1["summary"]=summary_text
    
    
    links = r.html.absolute_links
    new_links = links.copy()
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')
    
    for i in new_links:
        if i.startswith(google_domains):
            links.remove(i)
    
    new_new_links = []
    for i in links:
        new_new_links.append(i)
    
    dict1["useful_links"]=new_new_links
    
    return jsonify({"query_name": name, "dict": dict1})


if __name__ == '__main__':
    app.run()