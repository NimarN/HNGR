from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
) 
from flaskr import hngrGeocode

bp =  Blueprint('search', __name__, url_prefix='/search') 
@bp.route('/results', methods=('GET', 'POST'))
def results():

    if request.method == 'POST':
        try:
            location = request.form.get('location')
            longLat = hngrGeocode.geoLocate(location)
            type = request.form.get('type')
            return redirect(url_for('search.results', location=location, type=type, longLat = longLat ))
        except:
            return redirect(url_for('search.results'))
    try:
        location = request.args.get('location', None)
        longLat = hngrGeocode.geoLocate(location)
        type = request.args.get('type', None)
        poi_dict = hngrGeocode.localSearch(longLat, type)
        return render_template('search/results.html', location = location, type=type, longLat=longLat, poi_dict=poi_dict)
    except:
        return render_template('search/results.html')
