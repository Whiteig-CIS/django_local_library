import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Book, StudyRoom, StudyRoomBooking


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'language', 'summary', 'isbn', 'genre']


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


class StudyRoomForm(forms.ModelForm):
    class Meta:
        model = StudyRoom
        fields = [
            'name', 'location', 'seats', 'capacity', 'availability',
            'description', 'equipment', 'has_windows',
        ]


class StudyRoomBookingForm(forms.ModelForm):
    class Meta:
        model = StudyRoomBooking
        fields = ['start_time', 'end_time', 'status', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
