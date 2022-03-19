from src.appConfig import getAppConfigDict
from src.emailSender import sendEmail
import datetime as dt
import argparse


appConfig =getAppConfigDict()
noOfDays = appConfig['noOfDays']
excelDumpPath = appConfig['availabilityExcelDumpPath']


startDate = dt.datetime.now()
endDate = startDate + dt.timedelta(days=noOfDays)


parser = argparse.ArgumentParser()
parser.add_argument('--start_date', help="Enter start date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(startDate, '%Y-%m-%d'))
parser.add_argument('--end_date', help="Enter end date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(endDate, '%Y-%m-%d'))

args = parser.parse_args()

genFilename= f"{args.start_date}_to_{args.end_date}.xlsx"
filePath =f"{excelDumpPath}/{genFilename}"

mailBody= f"<b>Hi Sir/Ma'am, <br><br>  <i>Please find the attached excel availabilty of vaccine between date {args.start_date} and {args.end_date}</i> <br><br> Regards <br> Mayank Verma </b>"
mailSub = "Cowin Vaccine Availability Alert with Excel attachment"

isMailSent = sendEmail(appConfig,mailSub,mailBody, filePath)

if isMailSent:
    print('Mail sent successfully')
else:
    print('Mail sent unsuccessfully')
