import time
import os, pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
userdb = mydb["user"]
companydb = mydb["companies"]

# --------------------------------------------         GEORGIA          ------------------------------------------------------------------------------------------------
# Hr
# os.system("python3 /home/miriani/Desktop/rightnao/georgia/hr/final/hr.py")
try:
    # x = jobdb.delete_many({"source" : "hr.ge"})
    # print(x.deleted_count, " documents deleted.")
    os.system("python3 /home/miriani/Desktop/rightnao/georgia/hr/final/daily/hr.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"Hr.ge: {e}") 


# Hiro
try:
    # os.system("python3 /home/miriani/Desktop/rightnao/georgia/hiro/final/daily/hiro.py")
    # x = jobdb.delete_many({"source" : "hiro.ge"})
    # print(x.deleted_count, " documents deleted.")
    os.system("python3 /home/miriani/Desktop/rightnao/georgia/hiro/daily/hiro.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"Hiro.ge: {e}") 


# SS
try:
    os.system("python3 /home/miriani/Desktop/rightnao/georgia/ss/daily/ss.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"ss.ge: {e}")


# Jobs
try:
    os.system("python3 /home/miriani/Desktop/rightnao/georgia/jobs/daily/jobs.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"jobs.ge: {e}")


# Dasaqmeba
try:
    os.system("python3 /home/miriani/Desktop/rightnao/georgia/dasaqmeba/daily/dasaqmeba.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"dasaqmeba.ge: {e}")


# Doctor
try:
    os.system("python3 /home/miriani/Desktop/rightnao/georgia/doctor/daily/doctor.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"doctor.ge: {e}")

# Jobs24
try:
    # os.system("python3 /home/miriani/Desktop/rightnao/georgia/jobs24/daily/jobs24.py")
    # x = jobdb.delete_many({"source" : "jobs24.ge"})
    # print(x.deleted_count, " documents deleted.")
    os.system("python3 /home/miriani/Desktop/rightnao/georgia/jobs24/daily/jobs24.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"jobs24.ge: {e}")


# CV
try:
    os.system("python3 /home/miriani/Desktop/rightnao/georgia/cv/daily/cv.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"cv.ge: {e}")




# -----------------------------------------------------     ARMENIA      --------------------------------------------------------------------------------------------------

# Staff.am
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/staff/daily/staff.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"staff.am: {e}")

# Job.am    ------------
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/job/daily/job.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"job.am: {e}")

# Repatarmenia.org
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/repatarmenia/daily/repatarmenia.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"repatarmenia.org: {e}")

# Myjob.am
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/myjob/daily/myjob.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"myjob.am: {e}")

# list.am   ----------------
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/list/daily/list.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"list.am: {e}")

# rezume.am
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/rezume/daily/rezume.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"rezume.am: {e}")

# full.am
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/full/daily/full.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"full.am: {e}")

# jobfinder.am
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/jobfinder/daily/jobfinder.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"jobfinder.am: {e}")

# careercenter.am
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/careercenter/daily/careercenter.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"careercenter.am: {e}")

# worknet.am
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/worknet/daily/worknet.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"worknet.am: {e}")

# hr.am -----------------
try:
    os.system("python3 /home/miriani/Desktop/rightnao/armenia/hr/daily/hr.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"hr.am: {e}")



# ----------------------------------------------------          AZERBAIJAN           ---------------------------------------------------------------------------------------------

# azinka.az
try:
    os.system('python3 /home/miriani/Desktop/rightnao/azerbaijan/azinka/daily/azinka.py')
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"azinka.az: {e}")

# boss.az
try:
    os.system("python3 /home/miriani/Desktop/rightnao/azerbaijan/boss/daily/boss.py")
except Exception as e:
    f = open("error.txt", "a")
    f.write(f"boss.az: {e}")






















# -------------------------------------------------     MODIFICATORS            --------------------------------------------------------------------------------------------------


# Modificators
os.system("python3 /home/miriani/Desktop/rightnao/modificators/all.py")


# os.system("python3 /home/miriani/Desktop/rightnao/georgia/hr/final/hr_main.py")
# # os.system("python3 /home/miriani/Desktop/rightnao/georgia/ss/final/ss.py")
# os.system("python3 /home/miriani/Desktop/rightnao/georgia/hiro/final/hiro_main.py")
# # os.system("python3 /home/miriani/Desktop/rightnao/georgia/dasaqmeba/final/dasaqmeba.py")
# time.sleep(3600)

# This is the cheduled scraper