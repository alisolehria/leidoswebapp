from django import forms
from django.contrib.auth.models import User
from accounts.models import profile, location, projects, skills, holidays
from .models import location
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Field
from datetimewidget.widgets import DateTimeWidget
from django_countries.fields import LazyTypedChoiceField, countries
import datetime
from django.contrib.auth.models import User



class UserForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name:")
    last_name = forms.CharField(label="Last Name:")
    email = forms.EmailField(label="Email:")

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            'Name:',
           Div('first_name',
            'last_name'),
        ),
        Fieldset(
            'Email Address:',
        )
    )
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_query = User.objects.filter(email=email)
        if email_query.exists():
            raise forms.ValidationError("This Email Address Exists, Please Check Again!")
        return super(UserForm,self).clean(*args,**kwargs)

    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-xs-2'
    helper.field_class = 'col-lg-4'

class UserProfileForm(forms.ModelForm):
    dateTimeOptions = {
        'format': 'mm/dd/yyyy',
        'autoclose': True,
        'minView': 2,
        'maxView': 4,
    }

    dateOfBirth = forms.DateField(label="Date of Birth:",widget=DateTimeWidget(options=dateTimeOptions,bootstrap_version=3))
    nationality = LazyTypedChoiceField(choices=countries,label="Nationality:")
    preferredLocation= forms.ModelChoiceField(queryset=location.objects.all(),label="Location: ")
    gender = forms.ChoiceField(label="Gender:",choices=profile.GENDER)
    designation = forms.ChoiceField(label="Designation:",choices=profile.DESIGNATIONS)

    class Meta:
        model = profile
        fields = [
            'dateOfBirth',
            'nationality',
            'gender',
            'preferredLocation',
            'designation'
        ]

    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
          'General Information:',
            Div(Div('dateOfBirth',
            'nationality'),
                HTML("""
                <br><br><br>
            """),
            'gender')
        ),
        Fieldset(
            'Work Information:',
            Div('preferredLocation',
            'designation'),


        )
    )
    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-4'


class ProjectForm(forms.ModelForm):
    dateTimeOptions = {
        'format': 'mm/dd/yyyy',
        'autoclose': True,
        'minView': 2,
        'maxView': 4,
    }

    projectName = forms.CharField(label="Project Name:")
    location = forms.ModelChoiceField(queryset=location.objects.all(),label="Location: ")
    type = forms.ChoiceField(label="Project Type:",choices=projects.TYPE)
    startDate = forms.DateField(label="Start Date:",
                                  widget=DateTimeWidget(options=dateTimeOptions, bootstrap_version=3))
    endDate = forms.DateField(label="End Date:",
                                widget=DateTimeWidget(options=dateTimeOptions, bootstrap_version=3))
    description = forms.CharField(widget=forms.Textarea,label="Description:")
    budget = forms.IntegerField(label="Budget:",min_value=1)
    numberOfStaff = forms.IntegerField(label="Number of Staff:",min_value=1)
    class Meta:
        model=projects
        fields = [
            'projectName',
            'location',
            'type',
            'startDate',
            'endDate',
            'description',
            'budget',
            'numberOfStaff',
        ]

    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            'Project General Information:',
            Div(
            'projectName',
            'location',
                HTML("""
                        <br><br><br>
                    """),
            'type'),
             HTML("""
                    <br><br><br>
                """),
        ),
        Fieldset(
            'Project Dates:',
             Div('startDate',
            'endDate'),
             HTML("""
                    <br><br><br>
                """),
        ),
        Fieldset(
            'Project Description:',
            'description',

             Div('budget',
                 HTML("""
                       <br><br><br>
                   """),
            'numberOfStaff'),
             HTML("""
                    <br><br><br>
                """)
        ),
        Fieldset(
            '  '
        ),

        Fieldset(

            'Project Manager for the Project:',

         )
    )

    def clean(self, *args, **kwargs):
        startDate = self.cleaned_data.get('startDate')
        endDate = self.cleaned_data.get('endDate')
        numberOfStaff = self.cleaned_data.get('numberOfStaff')
        if startDate > endDate:
            raise forms.ValidationError('Start Date Cannot Precede End Date')
        if startDate == endDate:
            raise forms.ValidationError('Start Date Cannot be same as End Date')
        if numberOfStaff == 0:
            raise forms.ValidationError("The number of Staff cant be 0!")
        return super(ProjectForm, self).clean(*args, **kwargs)

    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-xs-2'
    helper.field_class = 'col-lg-4'

class SkillForm(forms.ModelForm):

    skillName = forms.CharField(label="Skill Name:")
    class Meta:
        model = skills
        fields = [
            'skillName'
        ]

    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            'Add Skill to the system by typing in skill name and pressing the add skill button',
            'skillName',
            HTML("""
                      <br><br><br>
                  """),
        ))
    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-4'

    def clean(self, *args, **kwargs):
        skillName = self.cleaned_data.get('skillName')
        name_query = skills.objects.filter(skillName = skillName)
        if name_query.exists():
            raise forms.ValidationError('This Skill already exists!')
        return super(SkillForm, self).clean(*args, **kwargs)


class LocationForm(forms.ModelForm):

    country = forms.CharField(label="Country Name:")
    city = forms.CharField(label="City Name:")

    class Meta:
        model = location
        fields = [
            'country',
            'city'
        ]

    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            'Add Location to the system by typing in country and city and then pressing the add location button',
            'country',
            HTML("""
                           <br><br><br>
                       """)
        ),
        Fieldset(
            '',
            'city',
            HTML("""
                       <br><br><br>
                   """)
        ))
    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-4'

    def clean(self, *args, **kwargs):
        countryName = self.cleaned_data.get('country')
        cityName = self.cleaned_data.get('city')
        country_query = location.objects.filter(country = countryName)
        city_query = location.objects.filter(city = cityName)

        if country_query.exists() and city_query.exists():
            raise forms.ValidationError('This Location already exists!')
        return super(LocationForm, self).clean(*args, **kwargs)

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name:")
    last_name = forms.CharField(label="Last Name:")
    email = forms.EmailField(label="Email:")

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            'Name:',
           Div('first_name',
            'last_name'),
        ),
        Fieldset(
            'Email Address:',
        )
    )

    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-xs-2'
    helper.field_class = 'col-lg-4'

class HolidaysForm(forms.ModelForm):
    dateTimeOptions = {
        'format': 'mm/dd/yyyy',
        'autoclose': True,
        'minView': 2,
        'maxView': 4,
    }

    startDate = forms.DateField(label="Start Date:",
                                widget=DateTimeWidget(options=dateTimeOptions, bootstrap_version=3))
    endDate = forms.DateField(label="End Date:",
                              widget=DateTimeWidget(options=dateTimeOptions, bootstrap_version=3))
    type = forms.ChoiceField(label="Project Type:", choices=holidays.TYPE)

    class Meta:
        model = holidays
        fields = [
            'type',
            'startDate',
            'endDate',
        ]

    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            'Vacation Dates:',
            Div('startDate',
                'endDate'),
            HTML("""
                        <br><br><br>
                    """),
        ),
        Fieldset(
            'Vacation Type:',
            'type',
            HTML("""
                            <br><br><br>
                        """),
        ),

    )


    def clean(self, *args, **kwargs):
        # username = User
        # query = profile.objects.get(user=username)
        # holiday = query.holidays_set.all()
        startDate = self.cleaned_data.get('startDate')
        endDate = self.cleaned_data.get('endDate')

        if startDate > endDate:
            raise forms.ValidationError('Start Date Cannot Precede End Date')
        if startDate < datetime.date.today():
            raise forms.ValidationError('Cannot Start Holiday From Date Earlier Than Today')
        # for hol in holiday:
        #         if startDate >= hol.startDate and startDate <= hol.endDate or endDate >= hol.startDate and endDate <= hol.endDate:
        #             raise forms.ValidationError('You Have Already Requested a Leave in Given Dates')
        return super(HolidaysForm, self).clean(*args, **kwargs)

    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-xs-2'
    helper.field_class = 'col-lg-4'