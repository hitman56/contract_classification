import datefinder
matches=datefinder.find_dates("obama was born on January 4th,2017 at 8:00.He got married on 12 june 2008")
for match in matches:
 print(match)
