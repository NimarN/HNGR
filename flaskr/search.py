from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
) 

bp =  Blueprint('search', __name__, url_prefix='/search') 
@bp.route('/results', methods=('GET', 'POST'))
def results():
    location = request.args.get('location', None)
    type = request.args.get('type', None)
    return render_template('search/results.html', location = location, type=type)
