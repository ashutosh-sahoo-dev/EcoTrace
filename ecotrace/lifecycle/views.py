from decimal import Decimal

from django.contrib import messages
from django.conf import settings
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .ai_engine import ai_engine
from .forms import ElectronicAssetForm, OperationalStatusForm
from .models import ElectronicAsset, SustainabilityLog


def dashboard_view(request):
    total_assets = ElectronicAsset.objects.count()

    active_passports = ElectronicAsset.objects.exclude(
        operational_status__in=["Retired", "Recycled"]
    ).count()

    total_carbon_offset = (
        SustainabilityLog.objects.aggregate(total=Sum("carbon_saved_kg"))["total"]
        or Decimal("0")
    )
    total_ewaste_diverted = (
        SustainabilityLog.objects.aggregate(total=Sum("ewaste_diverted_kg"))[
            "total"
        ]
        or Decimal("0")
    )

    healthy_assets = ElectronicAsset.objects.filter(condition_score__gte=8).count()
    maintenance_assets = ElectronicAsset.objects.filter(
        operational_status="Maintenance"
    ).count()
    recycling_assets = ElectronicAsset.objects.filter(ai_decision="RECYCLE").count()
    repair_assets = ElectronicAsset.objects.filter(ai_decision="REPAIR").count()

    lifecycle_health = (
        round((healthy_assets / total_assets) * 100) if total_assets else 0
    )

    recent_assets = ElectronicAsset.objects.all()[:6]

    return render(
        request,
        "lifecycle/dashboard.html",
        {
            "total_assets": total_assets,
            "active_passports": active_passports,
            "total_carbon_offset": total_carbon_offset,
            "total_ewaste_diverted": total_ewaste_diverted,
            "healthy_assets": healthy_assets,
            "maintenance_assets": maintenance_assets,
            "recycling_assets": recycling_assets,
            "repair_assets": repair_assets,
            "lifecycle_health": lifecycle_health,
            "recent_assets": recent_assets,
            "granite_enabled": getattr(
                settings,
                "IBM_GRANITE_ENABLED",
                False,
            ),
        },
    )


def asset_list_view(request):
    query = request.GET.get("q", "").strip()
    device_type = request.GET.get("device_type", "")
    status = request.GET.get("status", "")

    assets = ElectronicAsset.objects.all()

    if query:
        assets = assets.filter(
            Q(asset_id__icontains=query)
            | Q(device_name__icontains=query)
            | Q(ai_recommendation__icontains=query)
        )

    if device_type:
        assets = assets.filter(device_type=device_type)

    if status:
        assets = assets.filter(operational_status=status)

    return render(
        request,
        "lifecycle/asset_list.html",
        {
            "assets": assets,
            "query": query,
            "selected_device_type": device_type,
            "selected_status": status,
            "device_types": ElectronicAsset.DEVICE_TYPES,
            "statuses": ElectronicAsset.OPERATIONAL_STATUS,
        },
    )


def add_asset_view(request):
    if request.method == "POST":
        form = ElectronicAssetForm(request.POST)

        if form.is_valid():
            asset = form.save(commit=False)

            analysis = ai_engine.analyze_asset(
                asset_id=asset.asset_id,
                device_name=asset.device_name,
                device_type=asset.device_type,
                purchase_date=asset.purchase_date,
                condition_score=asset.condition_score,
                operational_status=asset.operational_status,
            )

            asset.ai_decision = analysis["decision"]
            asset.ai_confidence = Decimal(str(analysis["confidence"]))
            asset.ai_model = analysis["model"]
            asset.ai_source = analysis["source"]

            asset.ai_recommendation = (
                f"Diagnosis: {analysis['diagnosis']}\n\n"
                f"Maintenance Priority: {analysis['maintenance_priority']}\n\n"
                f"Recommendation: {analysis['recommendation']}\n\n"
                f"Environmental Rationale: {analysis['environmental_reason']}"
            )
            asset.save()

            # Educational prototype estimates. Replace with validated
            # campus-specific LCA/carbon factors in production.
            carbon_saved = Decimal("18.00") if analysis["decision"] in {
                "CONTINUE", "MAINTAIN", "REPAIR"
            } else Decimal("0.00")

            ewaste_diverted = (
                Decimal("2.50")
                if analysis["decision"] == "RECYCLE"
                else Decimal("0.00")
            )

            SustainabilityLog.objects.create(
                asset=asset,
                carbon_saved_kg=carbon_saved,
                ewaste_diverted_kg=ewaste_diverted,
                action=f"AI lifecycle decision: {analysis['decision']}",
                notes=analysis["environmental_reason"],
            )

            messages.success(
                request,
                f"{asset.asset_id} registered. AI recommendation: {analysis['decision']}.",
            )
            return redirect("dashboard")
    else:
        form = ElectronicAssetForm()

    return render(
        request,
        "lifecycle/add_asset.html",
        {"form": form},
    )


def asset_detail_view(request, asset_id):
    asset = get_object_or_404(ElectronicAsset, asset_id=asset_id)
    sustainability_logs = asset.sustainability_logs.all()

    if request.method == "POST":
        form = OperationalStatusForm(request.POST, instance=asset)
        if form.is_valid():
            previous_status = ElectronicAsset.objects.get(pk=asset.pk).operational_status
            updated_asset = form.save()
            new_status = updated_asset.operational_status

            # Record the human-review action in the sustainability log.
            SustainabilityLog.objects.create(
                asset=updated_asset,
                carbon_saved_kg=Decimal("0.00"),
                ewaste_diverted_kg=Decimal("0.00"),
                action=f"Human review: status updated from {previous_status} to {new_status}",
                notes=(
                    f"Operational status changed by responsible user after reviewing AI "
                    f"recommendation ({updated_asset.ai_decision}, "
                    f"confidence {updated_asset.ai_confidence})."
                ),
            )

            messages.success(
                request,
                f"{asset.asset_id}: operational status updated to '{new_status}'. "
                "Action recorded in the lifecycle passport.",
            )
            return redirect("asset_detail", asset_id=asset.asset_id)
    else:
        form = OperationalStatusForm(instance=asset)

    return render(
        request,
        "lifecycle/asset_detail.html",
        {
            "asset": asset,
            "form": form,
            "sustainability_logs": sustainability_logs,
        },
    )


def responsible_ai_view(request):
    return render(
        request,
        "lifecycle/responsible_ai.html",
    )
