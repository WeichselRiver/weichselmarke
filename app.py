from flask import Flask, render_template
import polars as pl

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gemeinschaftsausgaben")
def gemeinschaftsausgaben():
    # df = pl.read_csv("ampost.csv").group_by("Nr", maintain_order=True).agg(pl.col("variante"))
    df = pl.read_csv("ampost.csv").pivot(values="variante", index="Nr", columns="variante")

    return render_template("gemeinschaftsausgaben.html", data=df.to_pandas().to_html(index=False, escape=False), cols=df.columns)



@app.route("/sbz")
def sbz():

    saetze = [
        {
            "name": "Köpfe I",
            "marken": [
                {"name": "212", "value": "o;**"},
                {"name": "213", "value": "o;**"},
                {"name": "214", "value": "o;**"},
                {"name": "215", "value": "o;**"},
                {"name": "216", "value": "o;**"},
                {"name": "217", "value": "o;**"},
                {"name": "218", "value": "o;**"},
                {"name": "219", "value": "o;**"},
                {"name": "220", "value": "o;**"},
                {"name": "221", "value": "o;**"},
                {"name": "222", "value": "o;**"},
                {"name": "223", "value": "o;**"},
                {"name": "224", "value": "o;**"},
                {"name": "225", "value": "o;**"},
            ],
        },
        {
            "name": "Farben Köpfe I",
            "marken": [
                {"name": "212 a", "value": "o"},
                {"name": "212 b", "value": "o"},
                {"name": "212 c", "value": "o geprüft"},
            ],
        },
        {
            "name": "Plattenfehler Köpfe I",
            "marken": [
                {"name": "212 I", "value": ""},
            ],
        },
        {
            "name": "228-229",
            "marken": [
                {"name": "228", "value": "o;**"},
                {"name": "229", "value": "o;**"},
            ],
        },
        {
            "name": "Leipziger Frühjahrsmesse",
            "marken": [
                {"name": "230", "value": "o;**"},
                {"name": "231", "value": "o;**"},
            ],
        },
        {
            "name": "Leipziger Frühjahrsmesse Farben",
            "marken": [
                {"name": "231 a", "value": "o;**"},
                {"name": "231 b", "value": "**geprüft"},
            ],
        },
        {
            "name": "3. Volkskongress",
            "marken": [
                {"name": "232", "value": "o;**"},
                {"name": "233", "value": "o;**"},
            ],
        },
        {
            "name": "Goethe",
            "marken": [
                {"name": "234", "value": "o;**"},
                {"name": "235", "value": "o;**"},
                {"name": "236", "value": "o;**"},
                {"name": "237", "value": "o;**"},
                {"name": "238", "value": "o;**"},
            ],
        },
        {
            "name": "Goethe-Block",
            "marken": [
                {"name": "239 6", "value": ""},
                {"name": "Block 6", "value": "**"},
            ],
        },
        {
            "name": "Leipziger Herbstmesse",
            "marken": [
                {"name": "240", "value": "o;**"},
                {"name": "241", "value": "o;**"},
            ],
        },
    ]
    return render_template("sbz.html", saetze=saetze)


if __name__ == "__main__":
    app.run(debug=True)
