def convertDDMMYYToUnixTime(date, hourTimes):
    splitDate = date.split('.')

    ye = int(splitDate[2])+2000
    dday = int(splitDate[0])
    mmonth = int(splitDate[1])

    hoursTime = int( hourTimes.split(':')[0] )
    minuteTime = int( hourTimes.split(':')[1] )

    ftime = dt.datetime( ye ,  mmonth, dday,  hoursTime, minuteTime,0 ).timetuple()
    utime = time.mktime(ftime)
 
    return utime 

def convertUnixToDDMMYY(theTime):
    
    dateString = str( time.localtime(theTime).tm_mday )+ "."+str(time.localtime(theTime).tm_mon) +"."+ str(time.localtime(theTime).tm_year-2000)

    timeString = str(time.localtime(theTime).tm_hour) +":" +str( time.localtime(theTime).tm_min)
    return [dateString,timeString]

def printTheTimeFromDDMMYY(theTime, includeYear=False):

    weekDays = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]
    theMonths = [  "January", "February",  "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    myDay = weekDays[ time.localtime(theTime).tm_wday    ]

    myMonth = theMonths[ time.localtime(theTime).tm_mon-1 ]
    
    if includeYear:
        return myMonth + " " + str(time.localtime(theTime).tm_mday) +"," + str( time.localtime(theTime).tm_year )


    return myDay +" " + myMonth + " " + str(time.localtime(theTime).tm_mday)


def checkBeforeAfter(time1,time2):

    if time1>time2:
        return 1
    if time2>time1:
        return -1
    if time2==time1:
        return 0

def checkPastDay( time1, time2 ):

    if checkBeforeAfter(time1,time2)==1:
        return False
    else:
        if convertUnixToDDMMYY(time1)[0] == convertUnixToDDMMYY(time2)[0]:
            return False
        else:
            return True

def timeSortDict( myDict ):
    timeIndices = np.argsort(myDict["Time"])
    return truncateDict(myDict, timeIndices)



    

    
    

