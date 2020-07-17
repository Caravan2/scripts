import pymongo
from bson import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Jobs"]
_job = mydb["job"]


def JobDB(job):
    x = {
        "user_id":ObjectId(f"{job['user_id']}"),
        "company_id":ObjectId(f"{job['company_id']}"),
        "job_details":{
            "url": job['web_url'],
            "title":f"{job['title']}",
            "vacancy_type":job['vacancy_type'],
            "country":job['country_id'],
            "region":job['region'],
            "city":job['city'],
            "location_type":job['location_type'],
            "jobfunctions":f"{job['functions']}",
            "employment_types":f"{job['employment_type']}",
            "descriptions":[
                {
                    "language":f"ka",
                    "description":f"{job['description_ka']}",
                    "whyus":f"{job['whyus_ka']}"
                },
                {
                    "language":f"en",
                    "description":f"{job['description_en']}",
                    "whyus":f"{job['whyus_en']}"
                },
                {
                    "language":f"ru",
                    "description":f"{job['description_ru']}",
                    "whyus":f"{job['whyus_ru']}"
                }
            ],
            "required":{
                "experience":f"{job['r_experience']}",
                "tools_technology":[],
                "languages": job['r_languages'],
                "skills": job['r_skills'],
                "education":job['r_education'],
                "license":f"{job['r_license']}",
                "work":f"{job['r_work']}"
            },
            "preferred":{
                "experience":f"{job['p_experience']}",
                "tools_technology":[],
                "languages": job['p_languages'],
                "skills": job['p_skills'],
                "education":job['p_education'],
                "license":f"{job['p_license']}",
                "work":f"{job['p_work']}"
            },
            "salarycurrency":f"{job['salary_currency']}",
            "salarymin":job['salary_min'],
            "salarymax":job['salary_max'],
            "salaryinterval":f"{job['salary_interval']}",
            "additional_compensation":job['additional_compensation'],
            "additional_info":{
                "suitable_for":job['suitable_for'],
                "travel_requirement":job['travel_requirements']
            },
            "benefits":job['benefits'],
            "numberofpositions":job['number_of_positions'],
            "publishday":job['publish_day'],
            "publishmonth":job['publish_month'],
            "publishyear":job['publish_year'],
            "deadlineday":job['deadline_day'],
            "deadlinemonth":job['deadline_month'],
            "deadlineyear":job['deadline_year'],
            "hiringday":job['hiring_day'],
            "hiringmonth":job['hiring_month'],
            "hiringyear":job['hiring_year'],
            "cover_letter":True,
            "work_remote":False,
            "headerurl":job['header_url']
        },
        "job_metadata":{
            "advertisement_countries":["GE"],
            "highlight":"None",
            "renewal":0,
            "amount_of_days":0,
            "anonymous":False,
            "num_of_languages":1,
            "currency":"None"
        },
        "normalized_salary_min":job['salary_min'],
        "normalized_salary_max":job['salary_max'],
        "priority":0,
        "created_at":job['created_at'],
        "activation_date":job['activation_date'],
        "expiration_date":job['expiration_date'],
        "last_pause_date":job['last_pause_date'],
        "paused_days":job['paused_days'],
        "status":"Active",
        "applications":[],
        "invited_candidates":[]
    }


    y = _job.insert(x)
    print(y)



