import datetime

base = datetime.datetime.today()
numdays = 5
date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]


a = date_list[0]
print(a.strftime('%A %d %B'))
days = []
for a in date_list:
	days.append(a.strftime('%A %d %B'))

print(days)


# datetime.strftime(str(a),'%Y-%b-%A')
# print(date_list[1])