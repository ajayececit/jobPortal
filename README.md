Application which will fetch the job opening by using github's job API


# APIs urls
1) v1.0/api/jobs -> Provide all the json data of opening across the location
2) v1.0/api/jobs?title=cloud -> Provide all the json data of opening for the given job title
3) v1.0/api/jobs?location=germany -> Provide all the json data of opening for the given job location
4) v1.0/api/jobs?title=cloud&location=germany -> Provide all the json data of opening for the given job location and job title

# UI
1) jobs -> shows all the opening jobs in a table format
2) sync -> will fetch new jobs from git's job API
3) By selecting the job title or job location we can find the opening accrodingly



