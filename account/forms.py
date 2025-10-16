from django import forms

from .models import Shipment, LiveUpdate


class DateInput(forms.DateInput):
	input_type = 'date'


class ShipmentCreateForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = '__all__'
        exclude = ['date_created']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make tracking_number readonly (disabled) only during creation
        if not self.instance.pk:  # Means it's a "create" form
            self.fields['tracking_number'].disabled = True
            self.fields['tracking_number'].required = False  # Avoid validation error

        self.fields['content'].widget = forms.Textarea(attrs={'rows': 1, 'cols': 15})

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class LiveUpdateCreateForm(forms.ModelForm):
    created_on = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
            }
        ),
        required=True
    )

    class Meta:
        model = LiveUpdate
        fields = '__all__'
        exclude = ['date_created', 'shipment', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        # Pre-fill created_on with correctly formatted datetime if instance exists
        if self.instance and self.instance.created_on:
            self.initial['created_on'] = self.instance.created_on.strftime('%Y-%m-%dT%H:%M')