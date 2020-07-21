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
x = jobdb.delete_many({"source" : "hr.ge"})
print(x.deleted_count, " documents deleted.")
os.system("python3 /home/miriani/Desktop/rightnao/georgia/hr/final/hr.py")


# Hiro
os.system("python3 /home/miriani/Desktop/rightnao/georgia/hiro/final/hiro.py")
x = jobdb.delete_many({"source" : "hiro.ge"})
print(x.deleted_count, " documents deleted.")
os.system("python3 /home/miriani/Desktop/rightnao/georgia/hiro/final/hiro.py")


# SS
os.system("python3 /home/miriani/Desktop/rightnao/georgia/ss/final/ss.py")


# Jobs
os.system("python3 /home/miriani/Desktop/rightnao/georgia/jobs/final/jobs.py")


# Dasaqmeba
os.system("python3 /home/miriani/Desktop/rightnao/georgia/dasaqmeba/final/dasaqmeba.py")


# Doctor
os.system("python3 /home/miriani/Desktop/rightnao/georgia/doctor/final/doctor.py")


# Jobs24
os.system("python3 /home/miriani/Desktop/rightnao/georgia/jobs24/final/jobs24.py")
x = jobdb.delete_many({"source" : "jobs24.ge"})
print(x.deleted_count, " documents deleted.")
os.system("python3 /home/miriani/Desktop/rightnao/georgia/jobs24/final/jobs24.py")


# CV
os.system("python3 /home/miriani/Desktop/rightnao/georgia/cv/final/cv.py")
x = jobdb.delete_many({"source" : "cv.ge"})
print(x.deleted_count, " documents deleted.")
os.system("python3 /home/miriani/Desktop/rightnao/georgia/cv/final/cv.py")





# -----------------------------------------------------     ARMENIA      --------------------------------------------------------------------------------------------------

# Staff.am
os.system("python3 /home/miriani/Desktop/rightnao/armenia/staff/final/staff.py")


# Job.ad
os.system("python3 /home/miriani/Desktop/rightnao/armenia/job/final/job.py")


# Repatarmenia.org
os.system("python3 /home/miriani/Desktop/rightnao/armenia/repatarmenia/final/repatarmenia.py")


# Myjob.am
os.system("python3 /home/miriani/Desktop/rightnao/armenia/myjob/final/myjob.py")


# list.am
os.system("python3 /home/miriani/Desktop/rightnao/armenia/list/final/list.py")


# rezume.am
os.system("python3 /home/miriani/Desktop/rightnao/armenia/rezume/final/rezume.py")


# full.am
os.system("python3 /home/miriani/Desktop/rightnao/armenia/full/final/full.py")


# jobfinder.am
os.system("python3 /home/miriani/Desktop/rightnao/armenia/jobfinder/final/jobfinder.py")


# careercenter.am
os.system("python3 /home/miriani/Desktop/rightnao/armenia/careercenter/final/careercenter.py")


# worknet.am
os.system("python3 /home/miriani/Desktop/rightnao/armenia/worknet/final/worknet.py")


# hr.am
os.system("python3 /home/miriani/Desktop/rightnao/armenia/hr/final/hr.py")




# ----------------------------------------------------          AZERBAIJAN           ---------------------------------------------------------------------------------------------

# azinka.az
os.system('python3 /home/miriani/Desktop/rightnao/azerbaijan/azinka/final/azinka.py')

# boss.az
os.system("python3 /home/miriani/Desktop/rightnao/azerbaijan/boss/final/boss.py")























# -------------------------------------------------     MODIFICATORS            --------------------------------------------------------------------------------------------------


# Modificators
os.system("python3 /home/miriani/Desktop/rightnao/georgia/modificators/fix.py")

# Reassign
os.system("python3 /home/miriani/Desktop/rightnao/georgia/modificators/redefine.py")

# os.system("python3 /home/miriani/Desktop/rightnao/georgia/hr/final/hr_main.py")
# # os.system("python3 /home/miriani/Desktop/rightnao/georgia/ss/final/ss.py")
# os.system("python3 /home/miriani/Desktop/rightnao/georgia/hiro/final/hiro_main.py")
# # os.system("python3 /home/miriani/Desktop/rightnao/georgia/dasaqmeba/final/dasaqmeba.py")
# time.sleep(3600)

# This is the cheduled scraper