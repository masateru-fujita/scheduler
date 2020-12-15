from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import ListView, CreateView
from .models import User, Schedule
from datetime import datetime
from datetime import datetime, date, timedelta
from django.urls import reverse
import calendar
import locale
from django.core import serializers
from dateutil import relativedelta
from django.urls import reverse_lazy
from django.db import transaction
from .forms import ScheduleCreateForm

class ScheduleListView(CreateView):
    template_name = 'schedule_list.html'
    model = Schedule
    form_class = ScheduleCreateForm

    def post(self, request, *args, **kwargs):
        # 登録ボタン押下時
        if 'create' in request.POST:
            # 選択されているユーザ回数分登録する
            form = ScheduleCreateForm(request.POST)
            checks_users = request.POST.getlist('user_id')
            if form.is_valid():
                for user_id in checks_users:
                    form = ScheduleCreateForm(**self.get_form_kwargs())
                    form.instance.user_id = User.objects.get(pk=user_id)
                    form.save()

                # 登録日のスケジュールに遷移
                date = form.instance.date
                year = date.year
                month = date.month
                day = date.day
                return redirect('schedule:schedule_list', year=year, month=month, day=day)

            else:
                return redirect('schedule:schedule_list')

        # 削除ボタン押下時
        if 'delete' in request.POST:
            schedule_id = request.POST.get('schedule_id')
            Schedule.objects.filter(pk=schedule_id).delete()
            return redirect('schedule:schedule_list')

    def get_context_data(self, **kwargs):
        kwargs['dates'] = self.getDates()
        kwargs['schedules'] = self.getScheduleList(User.objects.all(), Schedule.objects.all())
        kwargs['next_week'] = self.getNextWeek()
        kwargs['prev_week'] = self.getPrevWeek()
        kwargs['today'] = self.getNow()
        return super(ScheduleListView, self).get_context_data(**kwargs)

    def getScheduleList(self, users, schedules):
        """1週間のスケジュール一覧を整形し返す
        引数：ユーザデータ、スケジュールデータ
        戻値：[{ユーザ、スケジュール[日付毎のスケジュール]}]
        """
        data = []
        for user in users:
            userschedulelist = {}
            userschedulelist['user_id'] = user.pk
            userschedulelist['name'] = user.name
            
            # 日付毎の一覧を格納する 
            dayschedulelist = []
            for day in self.getDates():

                # スケジュール一覧を格納する
                schedulelist = []
                for schedule in schedules.filter(user_id=user.pk, date=day).order_by('start_time'):
                    schedulelist.append(schedule)

                dayschedulelist.append(schedulelist)

            userschedulelist['schedule'] = dayschedulelist
            data.append(userschedulelist)

        return data

    def getDates(self):
        """今から1週間の日付を返す
        戻値：[日付]
        """
        locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day :
            date = datetime(year=int(year), month=int(month), day=int(day))
        else :
            date = datetime.now()
        # 曜日取得
        day = date.weekday()
        # 日曜日取得
        first = date - timedelta(days=day)

        datelist = []
        for index in range(7):
            dateindex = first + timedelta(days=index)
            datelist.append(dateindex)
        
        return datelist

    def getNextWeek(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day :
            date = datetime(year=int(year), month=int(month), day=int(day))
        else :
            date = datetime.now()

        return date + relativedelta.relativedelta(weeks=1)

    def getPrevWeek(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day :
            date = datetime(year=int(year), month=int(month), day=int(day))
        else :
            date = datetime.now()

        return date - relativedelta.relativedelta(weeks=1)

    def getNow(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day :
            date = datetime(year=int(year), month=int(month), day=int(day))
        else :
            date = datetime.now()

        return date

# class ScheduleCreateView(CreateView, generic.edit.ModelFormMixin):
#     template_name = 'schedule_create.html'
#     model = Schedule
#     success_url = reverse_lazy('schedule:schedule_list')
#     fields = ()

#     def post(self, request, *args, **kwargs):
#         # 選択されているユーザ回数分登録する
#         checks_users = request.POST.getlist('user_id')
#         for user_id in checks_users:
#             form = ScheduleCreateForm(**self.get_form_kwargs())
#             print(form.instance)
#             form.instance.user_id = User.objects.get(pk=user_id)
#             form.save()
        
#         # 登録日のスケジュールに遷移
#         year = form.instance.date.year
#         month = form.instance.date.month
#         day = form.instance.date.day
#         return redirect('schedule:schedule_list', year=year, month=month, day=day)

#     def get_context_data(self, **kwargs):
#         kwargs['users'] = User.objects.all()
#         return super(ScheduleCreateView, self).get_context_data(**kwargs)