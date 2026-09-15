from django import forms
from .models import ElectronicAsset


class OperationalStatusForm(forms.ModelForm):
    """Minimal human-review form: update operational status after reviewing AI recommendation."""

    class Meta:
        model = ElectronicAsset
        fields = ["operational_status"]
        widgets = {
            "operational_status": forms.Select(attrs={"class": "form-input"}),
        }


class ElectronicAssetForm(forms.ModelForm):
    class Meta:
        model = ElectronicAsset
        fields = [
            "asset_id",
            "device_name",
            "device_type",
            "purchase_date",
            "condition_score",
            "operational_status",
        ]
        widgets = {
            "asset_id": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. CAMPUS-LT-001",
                "autocomplete": "off",
            }),
            "device_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "e.g. ThinkPad Engineering Lab Laptop",
            }),
            "device_type": forms.Select(attrs={"class": "form-input"}),
            "purchase_date": forms.DateInput(attrs={
                "class": "form-input",
                "type": "date",
            }),
            "condition_score": forms.NumberInput(attrs={
                "class": "form-input",
                "min": "1",
                "max": "10",
                "placeholder": "1–10",
            }),
            "operational_status": forms.Select(attrs={"class": "form-input"}),
        }

    def clean_asset_id(self):
        value = self.cleaned_data["asset_id"].strip().upper()
        if not value:
            raise forms.ValidationError("Asset ID cannot be empty.")
        return value

    def clean_condition_score(self):
        score = self.cleaned_data["condition_score"]
        if not 1 <= score <= 10:
            raise forms.ValidationError("Condition score must be between 1 and 10.")
        return score
