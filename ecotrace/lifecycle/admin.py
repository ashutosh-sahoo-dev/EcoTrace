from django.contrib import admin
from .models import ElectronicAsset, SustainabilityLog


@admin.register(ElectronicAsset)
class ElectronicAssetAdmin(admin.ModelAdmin):
    list_display = (
        "asset_id",
        "device_name",
        "device_type",
        "condition_score",
        "operational_status",
        "ai_decision",
        "ai_confidence",
        "ai_model",
    )
    list_filter = ("device_type", "operational_status", "ai_decision")
    search_fields = ("asset_id", "device_name")
    readonly_fields = (
        "ai_recommendation",
        "ai_confidence",
        "ai_model",
        "ai_source",
        "created_at",
        "updated_at",
    )


@admin.register(SustainabilityLog)
class SustainabilityLogAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "action",
        "carbon_saved_kg",
        "ewaste_diverted_kg",
        "created_at",
    )
    search_fields = ("asset__asset_id", "asset__device_name")
    list_filter = ("action",)
