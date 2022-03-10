from datetime import date, datetime
from flask import Flask, request
from flask_cors import CORS
from requests import get, post

# import any blueprints from routes folder
app = Flask(__name__)

@app.route('/token')
def get_token():
    req = request.get_json(force=True)
    id = req.get('id', None)
    secret = req.get('secret', None)
    url = 'https://api.servicefusion.com/oauth/access_token'
    data = {
            "grant_type": "client_credentials",
            "client_id": id,
            "client_secret": secret
        }
    headers = {
        "Content-Type": "application/json"
    }
    result = post(url, json=data, headers=headers)
    return result.json()

@app.route('/jobs')
def get_jobs():
    req = request.get_json(force=True)
    token = req.get('token', None)
    phone = req.get('phone', None)
    daysMargin = int(req.get('daysMargin', None))
    year = int(req.get('year', None))
    month = int(req.get('month', None))
    day = int(req.get('day', None))
    date_ = date(year, month, day)
    total_spent = 0
    amount_of_jobs = 0
    current_page = 1
    total_pages = 2
    while (current_page < total_pages):
        jobs = get(f"https://api.servicefusion.com/v1/jobs?access_token={token}&filters[phone]={phone}&page={current_page}&per-page=50")
        total_pages = jobs.json()['_meta']['pageCount']
        current_page += 1
        for item in jobs.json()['items']:
            days_diff = (datetime.fromisoformat(item['closed_at']).date() - date_).days
            if (days_diff > daysMargin):
                continue
            total_spent += item['payments_deposits_total']
            amount_of_jobs += 1


    name = jobs.json()["items"][0]["customer_name"]
    return {"name": name, "total spent": total_spent, "amount of jobs": amount_of_jobs}


@app.route('/jobs', methods=["POST"])
def new_job():
    req = request.get_json(force=True)
    phoneNumber = req.get('phone', None)
    return {'phone': phoneNumber}

CORS(app)

if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True)
