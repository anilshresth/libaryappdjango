from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter the date between now and three weeks")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # check if the date is not in the past
        if data < datetime.date.today():
            raise ValidationError(
                _('Invalid date trying to renew in the past'))

        # check if the allowed range is in the allowed range
        if data > datetime.date.today() and datetime.timedelta(weeks=4):
            raise ValidationError(_("the renewal date 4 weeks ahead of time"))

        # Remember to send the data back
        return data
