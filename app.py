"""Flask application for Weichselmarke.

Refactored to use an application factory and helper functions.
"""

from functools import lru_cache
import json
from typing import List, Dict

from flask import Flask, render_template
import polars as pl


@lru_cache(maxsize=1)
def load_ampost_df() -> pl.DataFrame:
    """Load and pivot the `ampost.csv` file (cached).

    Returns:
        pl.DataFrame: pivoted dataframe with variants as columns.
    """
    # keep the original pivot behavior
    return pl.read_csv("ampost.csv").pivot(values="variante", index="Nr", on="variante")


@lru_cache(maxsize=1)
def load_raw_ampost_df() -> pl.DataFrame:
    """Load the raw `ampost.csv` file (cached).

    Returns:
        pl.DataFrame: dataframe representing the raw CSV file.
    """
    return pl.read_csv("ampost.csv")



def calculate_set_statistics(saetze: List[Dict]) -> Dict:
    """Calculate statistics for a list of stamp sets."""
    total_sets = len(saetze)
    complete_sets = 0
    total_stamps = 0
    complete_stamps = 0
    
    for satz in saetze:
        is_set_complete = True
        for marke in satz.get('marken', []):
            total_stamps += 1
            # Check for both mint ("**") and used ("o")
            val = marke.get('value', '')
            if "**" in val and "o" in val:
                complete_stamps += 1
            else:
                is_set_complete = False
        
        if is_set_complete and satz.get('marken'):
            complete_sets += 1
            
    return {
        "total_sets": total_sets,
        "complete_sets": complete_sets,
        "total_stamps": total_stamps,
        "complete_stamps": complete_stamps,
        "percent_stamps": round(complete_stamps / total_stamps * 100) if total_stamps > 0 else 0
    }

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
        with open("sbz_saetze.json", "r", encoding="utf-8") as f:
            saetze = json.load(f)
        stats = calculate_set_statistics(saetze)
        return render_template("sbz.html", saetze=saetze, stats=stats)

    @app.route("/ampost")
    def ampost():
        with open("ampost_saetze.json", "r", encoding="utf-8") as f:
            saetze = json.load(f)
        stats = calculate_set_statistics(saetze)
        return render_template("ampost.html", saetze=saetze, stats=stats)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
