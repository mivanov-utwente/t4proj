# -*- coding: utf-8 -*-
from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text


class RatingRadioWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        htmls = []
        final_attrs = self.build_attrs(attrs, type='radio', name=name, value=0,
                                       checked="checked")
        htmls.append(format_html('<input{} /><span class="hide"></span>',
                     flatatt(final_attrs)))

        for i in range(1, 5 + 1):
            final_attrs = self.build_attrs(attrs, type='radio', name=name,
                value=force_text(str(i)),)
            if str(i) == value:
                final_attrs['checked'] = 'checked'
            htmls.append(format_html('<input{} /><span></span>',
                         flatatt(final_attrs)))

        return '<div class="rating">{}</div>'.format(''.join(htmls))
