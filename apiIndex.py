from src.appConfig import getAppConfigDict
from src.sessionDataFetcher import fetchSessionsByDistId
from src.availabilityExcelGenerator import generateAvailabilityExcel
import datetime as dt
import argparse



appConfig = getAppConfigDict()

noOfDays = appConfig['noOfDays']


startDate = dt.datetime.now()
endDate = startDate + dt.timedelta(days=noOfDays)


parser = argparse.ArgumentParser()
parser.add_argument('--start_date', help="Enter start date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(startDate, '%Y-%m-%d'))
parser.add_argument('--end_date', help="Enter end date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(endDate, '%Y-%m-%d'))

args = parser.parse_args()
startDate = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
endDate = dt.datetime.strptime(args.end_date, '%Y-%m-%d')

startDate = startDate.replace(
    hour=0, minute=0, second=0, microsecond=0)
endDate = endDate.replace(
    hour=0, minute=0, second=0, microsecond=0)

currDate= startDate

distIdsList = appConfig['districtIds']
excelDumpPath = appConfig['availabilityExcelDumpPath']


finalOpList =[]
for distId in distIdsList:
    while currDate<=endDate:
        sessions =fetchSessionsByDistId(distId, currDate )
        for centre in sessions:
            if centre['available_capacity']>0:
                availableObj = {"date": centre['date'], "district_name":centre['district_name'], "block_name":centre['district_name'], "address":centre['address'], 
                "fee_type":centre['fee_type'], "available_capacity":centre['available_capacity'], "available_capacity_dose1":centre['available_capacity_dose1'], "available_capacity_dose2":centre['available_capacity_dose2'],
                "vaccine_name":centre['vaccine']}
    
                if centre["allow_all_age"]==False:
                    availableObj['min_age_limit']= centre["min_age_limit"]
                    availableObj['max_age_limit']= centre["max_age_limit"]
                elif centre["allow_all_age"]==True:
                    availableObj['min_age_limit']= centre["min_age_limit"]
                    availableObj['max_age_limit']= "NA"
                    
                finalOpList.append(availableObj)
        currDate = currDate + dt.timedelta(days=1)
    currDate= startDate


generateAvailabilityExcel(finalOpList,excelDumpPath, startDate, endDate )
