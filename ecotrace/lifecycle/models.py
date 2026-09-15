from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ElectronicAsset(models.Model):
    DEVICE_TYPES = [
        ("Laptop", "Laptop"),
        ("Desktop Lab Unit", "Desktop Lab Unit"),
        ("Server", "Server"),
        ("Projector", "Projector"),
    ]

    OPERATIONAL_STATUS = [
        ("Active", "Active"),
        ("Maintenance", "Maintenance"),
        ("Retired", "Retired"),
        ("Recycled", "Recycled"),
    ]

    AI_DECISIONS = [
        ("CONTINUE", "Continue"),
        ("MAINTAIN", "Maintain"),
        ("REPAIR", "Repair"),
        ("RECYCLE", "Recycle"),
        ("Pending", "Pending"),
    ]

    asset_id = models.CharField(max_length=50, unique=True, db_index=True)
    device_name = models.CharField(max_length=150)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    purchase_date = models.DateField()
    condition_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    operational_status = models.CharField(
        max_length=30,
        choices=OPERATIONAL_STATUS,
        default="Active",
    )
    ai_recommendation = models.TextField(
        blank=True,
        default="Pending AI assessment.",
    )
    ai_decision = models.CharField(
        max_length=30,
        choices=AI_DECISIONS,
        default="Pending",
    )
    ai_confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    ai_model = models.CharField(
        max_length=150,
        default="EcoTrace Rules Engine",
    )
    ai_source = models.CharField(
        max_length=150,
        default="Local deterministic fallback",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset_id} — {self.device_name}"

    @property
    def lifecycle_status(self):
        if self.operational_status == "Recycled":
            return "Recycled"
        if self.condition_score >= 8:
            return "Healthy"
        if self.condition_score >= 5:
            return "Monitor"
        return "At Risk"


class SustainabilityLog(models.Model):
    asset = models.ForeignKey(
        ElectronicAsset,
        on_delete=models.CASCADE,
        related_name="sustainability_logs",
    )
    carbon_saved_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    ewaste_diverted_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    action = models.CharField(max_length=150, default="Lifecycle assessment")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.asset.asset_id} — {self.action}"
