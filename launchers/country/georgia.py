import time
import os, pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
userdb = mydb["user"]
companydb = mydb["companies"]

# --------------------------------------------         GEORGIA          ------------------------------------------------------------------------------------------------
# Hr
os.system("python3 /home/miriani/Desktop/rightnao/georgia/hr/final/hr.py")
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