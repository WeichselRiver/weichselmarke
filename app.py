"""Flask application for Weichselmarke.

Refactored to use an application factory and helper functions.
"""

from functools import lru_cache
from typing import List, Dict

from flask import Flask, render_template
import polars as pl


SBZ_SAETZE: List[Dict[str, object]] = [
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
    {"name": "Plattenfehler Köpfe I", "marken": [{"name": "212 I", "value": ""}]},
    {"name": "228-229", "marken": [{"name": "228", "value": "o;**"}, {"name": "229", "value": "o;**"}]},
    {"name": "Leipziger Frühjahrsmesse", "marken": [{"name": "230", "value": "o;**"}, {"name": "231", "value": "o;**"}]},
    {"name": "Leipziger Frühjahrsmesse Farben", "marken": [{"name": "231 a", "value": "o;**"}, {"name": "231 b", "value": "**geprüft"}]},
    {"name": "3. Volkskongress", "marken": [{"name": "232", "value": "o;**"}, {"name": "233", "value": "o;**"}]},
    {"name": "Goethe", "marken": [{"name": "234", "value": "o;**"}, {"name": "235", "value": "o;**"}, {"name": "236", "value": "o;**"}, {"name": "237", "value": "o;**"}, {"name": "238", "value": "o;**"}]},
    {"name": "Goethe-Block", "marken": [{"name": "239 6", "value": ""}, {"name": "Block 6", "value": "**"}]},
    {"name": "Leipziger Herbstmesse", "marken": [{"name": "240", "value": "o;**"}, {"name": "241", "value": "o;**"}]},
]


@lru_cache(maxsize=1)
def load_ampost_df() -> pl.DataFrame:
    """Load and pivot the `ampost.csv` file (cached).

    Returns:
        pl.DataFrame: pivoted dataframe with variants as columns.
    """
    # keep the original pivot behavior
    return pl.read_csv("ampost.csv").pivot(values="variante", index="Nr", columns="variante")


@lru_cache(maxsize=1)
def load_raw_ampost_df() -> pl.DataFrame:
    """Load the raw `ampost.csv` file (cached).

    Returns:
        pl.DataFrame: dataframe representing the raw CSV file.
    """
    return pl.read_csv("ampost.csv")


def create_app() -> Flask:
    """Create and configure the Flask application.

    Routes are defined inside this factory so the module can be imported
    without side effects (useful for testing and deployments).
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")


    @app.route("/sbz")
    def sbz():
        return render_template("sbz.html", saetze=SBZ_SAETZE)

    @app.route("/ampost")
    def ampost():
        df = load_ampost_df()
        html = df.to_pandas().to_html(index=False, escape=False)
        return render_template("ampost.html", data=html, cols=df.columns)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
