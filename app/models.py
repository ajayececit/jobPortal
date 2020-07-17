from app import db

class JobPortal(db.Model):
    __tablename__ = 'jobportal'
    id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.String(255))
    title = db.Column(db.String(255))
    jobID = db.Column(db.String(255))
    location = db.Column(db.String(255))

    def __init__(self, company, title, jobID, location):
        self.company = company
        self.title = title
        self.location = location
        self.jobID = jobID

    def __repr__(self):
        return '<JOB %r>' % self.company



