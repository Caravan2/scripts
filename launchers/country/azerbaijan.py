import time
import os, pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sales_db"]
jobdb = mydb["jobs"]
userdb = mydb["user"]
companydb = mydb["companies"]

# ----------------------------------------------------          AZERBAIJAN           ---------------------------------------------------------------------------------------------

# azinka.az
os.system('python3 /home/miriani/Desktop/rightnao/azerbaijan/azinka/final/azinka.py')








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