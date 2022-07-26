from contextlib import redirect_stderr
import functools
from flaskr import hngrGeocode

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
) 

bp = Blueprint('home', __name__, url_prefix='/') 

@bp.route('', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        try:
            location = request.form.get('location')
            longLat = hngrGeocode.geoLocate(location)
            type = request.form.get('type')
            return redirect(url_for('search.results', location=location, type=type, longLat = longLat ))
        except:
            return redirect(url_for('search.results'))
    return render_template('home/index.html')



