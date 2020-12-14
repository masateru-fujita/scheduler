from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView
from .models import User, Schedule
from datetime import datetime
from datetime import datetime, date, timedelta
import calendar
import locale

class ScheduleListView(ListView):
    template_name = 'schedule_list.html'
    model = Schedule
    fields = ('date')

    def get_context_data(self, **kwargs):
        kwargs['dates'] = self.getDates()
        kwargs['schedules'] = self.getScheduleList(User.objects.all(), Schedule.objects.select_related().all())
        return super(ScheduleListView, self).get_context_data(**kwargs)

    def getScheduleList(self, users, schedules):
        userschedulelist = {user: [] for user in users}   

        for user in users:

            # 日付毎の一覧を格納する
            day_schedules = {day: [] for day in self.getDates()}    
            for day in day_schedules:

                # スケジュール一覧を格納する
                schedulelist = []
                for schedule in schedules.filter(user_id=user.pk, date=day):
                    day_schedules[day].append(schedule)

            userschedulelist[user].append(day_schedules)
            
        print(userschedulelist)
        return userschedulelist

    def getDates(self):
        locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")
        
        date = datetime.now()
        # 曜日取得
        day = date.weekday()
        # 日曜日取得
        first = date - timedelta(days=day)

        daylist = ['月', '火', '水', '木', '金', '土', '日']

        datelist = []
        for index in range(7):
            dateindex = first + timedelta(days=index)
            datelist.append(dateindex)

            # datelist.append(dateindex.strftime('%m月%d日') + '(' + daylist[index] + ')')
        
        return datelist