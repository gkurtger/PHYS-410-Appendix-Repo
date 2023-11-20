import numpy as np

# convert calendar date to Julian Date
# from https://quasar.as.utexas.edu/BillInfo/JulianDatesG.html
def date_to_JD(yr,mo,da,UT_h,UT_m,UT_s):
    round_time = 6
    y = yr
    m = mo
    d = da
    if mo <= 2:
        y = yr -1
        m = mo + 12
       
    fraction_day = np.round((UT_h + (UT_m/60.0) + (UT_s/3600.0))/24.0, round_time)
   
    a = np.int(np.floor(y/100.0))
    b = np.int(np.floor(a/4.0))
    c = 2 - a + b
    e = np.int(np.floor(365.25 * (y+4716)))
    f = np.int(np.floor(30.6001*(m+1)))
    output_JD_at0UT = c + d + e + f -1524.5
    output_JD = np.round(output_JD_at0UT + fraction_day, round_time)
    return (output_JD)    

# convert Julian Date to calendar date
# from https://quasar.as.utexas.edu/BillInfo/JulianDatesG.html
def JD_to_date(input_JD):
    # extract the fraction of day
    day_frac,dayJD = np.modf(input_JD-0.5)
    day_JD = dayJD + 0.5
    frac_hr,hr = np.modf(day_frac*24.0)
    hour = np.int(hr)
    frac_mi,mi = np.modf(frac_hr*60.0)
    minute = np.int(mi)
    second = np.round(frac_mi * 60.0, 1)
   
    # extract the calendar date; works only for dates since 1582
    q = day_JD + 0.5
    z = np.int(np.floor(q))
    w = np.int(np.floor((z - 1867216.25)/36524.25))
    x = np.int(np.floor(w / 4.0))
    a = z + 1 + w - x
    b = a + 1524
    c = np.int(np.floor((b - 122.1)/365.25))
    d = np.int(np.floor(365.25 * c))
    e = np.int(np.floor((b - d) / 30.6001))
    f = np.int(np.floor(30.60001 * e))

    month = e - 1
    if month > 12:
        month = e - 13
    year = c - 4716
    if month <= 2:
        year = c - 4715
    day = np.int(np.floor(b - d - f + (q - z)))
   
    return (year,month,day,hour,minute,second)

print(date_to_JD(2022,10,29,6,50,43))
print (JD_to_date(2459881.78522))