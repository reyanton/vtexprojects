from datetime import datetime as dt
from datetime import timedelta 

def asignar_time(dateini, dateend):
   
    dateini = dateini + ' 00:00:00'
    dateend = dateend + ' 23:59:59'
    
    dt_ini = dt.strptime(dateini, '%Y/%m/%d %H:%M:%S') + timedelta(hours=5)
    dt_end = dt.strptime(dateend, '%Y/%m/%d %H:%M:%S') + timedelta(hours=5)

    sdate_ini = dt.strftime(dt_ini, '%Y-%m-%d %H:%M:%S')
    sdate_end = dt.strftime(dt_end, '%Y-%m-%d %H:%M:%S')
    sdate_ini = sdate_ini[:10] + 'T' + sdate_ini[11:] + '.000Z'
    sdate_end = sdate_end[:10] + 'T' + sdate_end[11:] + '.999Z'
    return(sdate_ini + ' TO ' + sdate_end )
    
def format_time(dateini, dateend):
   
    dateini = dateini + ' 00:00:00'
    dateend = dateend + ' 23:59:59'
    
    dt_ini = dt.strptime(dateini, '%Y/%m/%d %H:%M:%S')
    dt_end = dt.strptime(dateend, '%Y/%m/%d %H:%M:%S')

    sdate_ini = dt.strftime(dt_ini, '%Y-%m-%d %H:%M:%S')
    sdate_end = dt.strftime(dt_end, '%Y-%m-%d %H:%M:%S')
    sdate_ini = sdate_ini[:10] + 'T' + sdate_ini[11:] + '.000Z'
    sdate_end = sdate_end[:10] + 'T' + sdate_end[11:] + '.999Z'
    return(sdate_ini + ' TO ' + sdate_end )


#print(asignar_time('2020/09/01', '2020/09/01'))
