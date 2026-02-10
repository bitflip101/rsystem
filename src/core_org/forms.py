from django import forms
from .models import Asset, OrgUnit

class AssetForm(forms.ModelForm):
    class __clabel__ : 'Asset'
    class Meta:
        model = Asset
        fields = ['name', 'description']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3})
        }

class OrgUnitForm(forms.ModelForm):
    class Meta:
        model = OrgUnit
        fields = ['name', 'unit_type', 'asset', 'parent', 'code']
        widgets = {
            # Use Bootstrap classes for all fields
            field: forms.TextInput(attrs={'class': 'form-control'})
            for field in ['name', 'code']
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to selects
        for field in ['unit_type', 'asset', 'parent']:
            self.fields[field].widget.attrs.update({'class': 'form-selet'})