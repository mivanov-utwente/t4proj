# -*- coding: utf-8 -*-
from datetime import time, datetime, timedelta
from django import forms


def data_filter_form_class_factory(room_choices, survey_choices):
    class DataFilterForm(forms.Form):
        room_ids = forms.MultipleChoiceField(choices=room_choices)
        survey_id = forms.ChoiceField(choices=survey_choices)
        daterange = forms.RegexField(
            regex=r'^\d{4}-\d{2}-\d{2} - \d{4}-\d{2}-\d{2}$')
        timerange = forms.RegexField(regex=r'^\d+;\d+$')

        def clean_timerange(self):
            data = self.cleaned_data['timerange']
            minute_start, minute_end = (int(_) for _ in data.split(';'))
            time_start = time(minute_start // 60, minute_start % 60)
            time_end = time(minute_end // 60, minute_end % 60)
            return (time_start, time_end)

        def clean_daterange(self):
            data = self.cleaned_data['daterange']
            start_date_str, end_date_str = data.split(' - ')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = (datetime.strptime(end_date_str, '%Y-%m-%d') +
                    timedelta(1)).date()
            return (start_date, end_date)


    return DataFilterForm

