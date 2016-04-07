# -*- coding: utf-8 -*-
from t4proj.apps.survey.models import Survey, Answer
from django.db.models import Q


def answers_filtered_by_survey_rooms_daterange_timerange(
        survey_id, room_ids, daterange, timerange, order='-id'):
    s = Survey.objects.get(pk=survey_id)
    start_time, end_time = timerange
    answers = Answer.objects.order_by(order).filter(
                  Q(response__created_at__range=daterange) &
                  Q(response__created_at__time__gte=start_time) &
                  Q(response__created_at__time__lte=end_time) &
                  Q(response__survey=s) &
                  Q(response__room_id__in=room_ids))

    return answers