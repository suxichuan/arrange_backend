from datetime import date
import calendar
cal=calendar.Calendar()
now=date.today()
week_list=cal.monthdatescalendar(now.year,now.month)
# print(week_list)
print(week_list.pop())
# for week in week_list:
#     for day in week:
#         if day == now:
#             break
#     current_week=week

# staff_list=[
# '苏赫1',
# 'hudi',
# 'kudi',
# '西溪1',
# '西溪2',
# '西溪3',
# '西溪4',
# '西溪5',
# '西溪6',
# '西溪7',
# '西溪8',
# '西溪9',
# '西溪10',
# '西溪11',
# '西溪12',
# '西溪13',
# '西溪14',
# '西溪15',
# '西溪16',
# '西溪17',
# '西溪18',
# '西溪19',
# '西溪20',
# '西溪21',
# '西溪22',
# '西溪23',
# '西溪24',
# '西溪25',
# '西溪26',
# '西溪27',
# '西溪28',
# '西溪29',
# '西溪30',
# '西溪31',
# '西溪32',
# '西溪33',
# '西溪34',
# '西溪35',
# '西溪36',
# '西溪37',
# '西溪38',
# '西溪39',
# '西溪40',
# '西溪41',
# '西溪42',
# '西溪43',
# '西溪44',
# '西溪45',
# '西溪46']
# place_list=['扎西基地','区税务总局','娘热路基地','西城税务分局']
# staff_list=['10032', '10010', '10038', '10046', '10030', '10040', '10031', '10020', '10047', '10025', '10039', '10042']
# for i,x in zip(place_list,staff_list):
#     print(i+x)
# per_place_staff_number=3
# simple_place_list=[]
# for i in range(0,per_place_staff_number):
#     simple_place_list.extend([x for x in place_list])


# for i in range(0,0):
#     print(i)


