from db.companyDB import CompanyDB
from db.userDB import UserDB
from db.jobDB import JobDB
from instantiate import InstantiateUser, InstantiateJob, InstantiateCompany

_job = InstantiateJob()
print(_job)
_job['user_id'] = "5ea1a1c12b69f7c1755688a0"
_job['company_id'] = "5ea1a1c12b69f7c1755688a0"
JobDB(_job)
