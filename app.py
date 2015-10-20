"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
# import acp_limits


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404


###############
#
# Algorithm logic...
#
###############

# This is backwards, it should be obvious.......
speed_min = [13.333, 11.428, 15.0, 15.0, 15.0]
speed_max = [26.0, 28.0, 30.0, 32.0, 34.0]
speed_int = [1000, 600, 400, 200, 0]

def calc_min_time(d,b):
	if d <= 0.0:
		return 0.0
	t_min_time = 0
	t_cur_dist = d
	for i,v in enumerate(speed_int):
		if b > v:
			t_dist_left = max(t_cur_dist - v, 0)
			t_min_time += t_dist_left / speed_max[i]
			t_cur_dist -= t_dist_left
	return t_min_time

def calc_max_time(d,b):
	if d <= 0.0:
		return 1.0
	t_max_time = 0
	t_cur_dist = d
	for i,v in enumerate(speed_int):
		if b >= v:
			t_dist_left = max(t_cur_dist - v, 0)
			t_max_time += t_dist_left / speed_min[i]
			t_cur_dist -= t_dist_left
	return t_max_time

###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############

@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from miles, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of miles. 
  """
  app.logger.debug("Got a JSON request");
  miles = request.args.get('km', 0, type=int)
  brevet = request.args.get('brevet', 0, type=int)
  start_time = request.args.get('start', 0)
  if miles > brevet * 1.1:
  	 return jsonify(error="ERROR: Longer than 110% brevet distance")
  start_time = arrow.get(start_time)
  time_start = start_time.replace(hours=+calc_min_time(miles, brevet)).isoformat()
  time_end = start_time.replace(hours=+calc_max_time(miles, brevet)).isoformat()
  return jsonify(result=[time_start, time_end])
 
#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
