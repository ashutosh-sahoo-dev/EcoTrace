from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ElectronicAsset",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("asset_id", models.CharField(db_index=True, max_length=50, unique=True)),
                ("device_name", models.CharField(max_length=150)),
                ("device_type", models.CharField(
                    choices=[
                        ("Laptop", "Laptop"),
                        ("Desktop Lab Unit", "Desktop Lab Unit"),
                        ("Server", "Server"),
                        ("Projector", "Projector"),
                    ],
                    max_length=50,
                )),
                ("purchase_date", models.DateField()),
                ("condition_score", models.PositiveSmallIntegerField(
                    validators=[
                        django.core.validators.MinValueValidator(1),
                        django.core.validators.MaxValueValidator(10),
                    ]
                )),
                ("operational_status", models.CharField(
                    choices=[
                        ("Active", "Active"),
                        ("Maintenance", "Maintenance"),
                        ("Retired", "Retired"),
                        ("Recycled", "Recycled"),
                    ],
                    default="Active",
                    max_length=30,
                )),
                ("ai_recommendation", models.TextField(
                    blank=True,
                    default="Pending AI assessment.",
                )),
                ("ai_decision", models.CharField(
                    choices=[
                        ("CONTINUE", "Continue"),
                        ("MAINTAIN", "Maintain"),
                        ("REPAIR", "Repair"),
                        ("RECYCLE", "Recycle"),
                        ("Pending", "Pending"),
                    ],
                    default="Pending",
                    max_length=30,
                )),
                ("ai_confidence", models.DecimalField(
                    decimal_places=2,
                    default=0,
                    max_digits=5,
                )),
                ("ai_model", models.CharField(
                    default="EcoTrace Rules Engine",
                    max_length=150,
                )),
                ("ai_source", models.CharField(
                    default="Local deterministic fallback",
                    max_length=150,
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="SustainabilityLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("carbon_saved_kg", models.DecimalField(
                    decimal_places=2,
                    default=0,
                    max_digits=12,
                    validators=[django.core.validators.MinValueValidator(0)],
                )),
                ("ewaste_diverted_kg", models.DecimalField(
                    decimal_places=2,
                    default=0,
                    max_digits=12,
                    validators=[django.core.validators.MinValueValidator(0)],
                )),
                ("action", models.CharField(default="Lifecycle assessment", max_length=150)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("asset", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="sustainability_logs",
                    to="lifecycle.electronicasset",
                )),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
