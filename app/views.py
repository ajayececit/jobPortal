from app import app, db, ma
from flask import render_template, request, redirect, url_for, flash, jsonify, Response
from app.models import JobPortal
import requests
import json

def get_json_resp(url):
	if url is None:
		return

	resp = requests.get(url)
	return resp.json()


@app.route('/')
@app.route('/jobs', methods = ['POST', 'GET'])
def jobList():
    '''
    API for home page and view all the JOBS which are active.
    API will query the DB and show all the values in front end
    
    On Post request API will serve the filtered values for the 
    job search
    '''

    if request.method == "GET":
        jobs = db.session.query(JobPortal).all() 
        return render_template('mainHome.html', jobs=jobs)
    elif request.method == "POST":   
        titleSearch = request.form['title']
        locationSearch = request.form["location"]

        if locationSearch and titleSearch:
            jobs = get_json_resp("http://localhost:8080/v1.0/api/jobs?location={}&title={}".format(locationSearch, titleSearch))
            return render_template('mainHome.html', jobs=jobs)

        if not titleSearch and not  locationSearch:
            jobs = get_json_resp("http://localhost:8080/v1.0/api/jobs")
            
        if locationSearch:
            jobs = get_json_resp("http://localhost:8080/v1.0/api/jobs?location=" + str(locationSearch))
            
        if titleSearch:
            jobs = get_json_resp("http://localhost:8080/v1.0/api/jobs?title=" + str(titleSearch))
        
        return render_template('mainHome.html', jobs=jobs)

    

# Marshmallow Model Schema
class JobSchema(ma.Schema):
    class Meta:
        fields = ("id", "company", "title", "jobID", "location" )

resultSchema = JobSchema(many=True)

# Backend API Calls for the JOB Search
@app.route("/v1.0/api/jobs", methods = ['POST', 'GET'])
def jobUI():

    title = request.args.get('title')
    location = request.args.get('location')

    if not title and not location:
        jobs =  db.session.query(JobPortal).all() 

    if location:
        jobs = JobPortal.query.filter(JobPortal.location.contains(location)).all()

    if title:
        jobs = JobPortal.query.filter(JobPortal.title.contains(title)).all()
    

    result = resultSchema.dump(jobs)
    return jsonify(result)
    

@app.route('/sync/', methods=['POST', 'GET'])
def syncJob():
    """
    API to sync all the job list from github's job API
    github job API : https://jobs.github.com/positions.json

    """
    urlToFetch = "https://jobs.github.com/positions.json"
    response = requests.get(urlToFetch)
    if response.status_code == 200:
        jobPosts = response.json()

        for i in range(len(jobPosts)):
            # sync the new job posts if it is not exists in DB
            if JobPortal.query.filter_by(jobID = jobPosts[i]['id']) == None:

                jobs = JobPortal(
                    company=jobPosts[i]['company'],
                    title=jobPosts[i]['title'],
                    jobID=jobPosts[i]['id'],
                    location=jobPosts[i]['location']
                )
                db.session.add(jobs)
        db.session.commit()
        jobs = db.session.query(JobPortal).all() 
        flash("kjsadkjasdkjhd")
        return render_template('mainHome.html', jobs=jobs)
    return render_template('404.html'), 404



@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="5000")