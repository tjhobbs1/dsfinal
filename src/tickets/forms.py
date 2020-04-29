from django import forms




class TicketForm(forms.Form):
    def __init__(self, *args, **kwargs):
        my_arg = kwargs.pop('my_arg')
        my_new_arg = []
        Stops = (
    (0, 0),         
    (1, 1), 
    (2, 2), 
    (3, 3),  
) 

        for i in my_arg:
            y = ()
            y = y + (i,i)
            my_new_arg.append(y)

       
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['flightFrom'] = forms.ChoiceField(choices=my_new_arg, widget=forms.Select(attrs={'class':'select-css'}), required=True)
        self.fields['destination'] = forms.ChoiceField(choices=my_new_arg, widget=forms.Select(attrs={'class':'select-css'}), required=True)
        self.fields['numOfStops'] = forms.ChoiceField(choices=Stops, widget=forms.Select(attrs={'class':'select-css'}), required=True)
        
    # flight_num = forms.CharField(label="Flight Number")
    # flight_num2 = forms.CharField(label="Flight Number")
    #depart_airport = forms.ChoiceField(choices=[])