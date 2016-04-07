from django.db.models import Transform
from django.db.models import DateTimeField, TimeField
from django.utils.functional import cached_property


class TimeValue(Transform):
    lookup_name = 'time'
    function = 'time'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return 'TIME({})'.format(lhs), params

    @cached_property
    def output_field(self):
        return TimeField()


DateTimeField.register_lookup(TimeValue)