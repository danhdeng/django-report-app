from django import forms

CHART_CHOICES=(
    ('#1', "Bar Chart"),
    ('#2', "Pie Chart"),
    ('#3', "Line Chart"),
)

RESULT_CHOICES=(
    ('#1', "Transaction"),
    ('#2', "Sale Date"),
)

class SearchSaleForm(forms.Form):
    date_from=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    date_to=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    chart_type=forms.ChoiceField(choices=CHART_CHOICES)
    result_by=forms.ChoiceField(choices=RESULT_CHOICES)

