from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from .models import ElectronicAsset, SustainabilityLog


class EcoTraceTests(TestCase):
    def test_dashboard_loads(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_add_asset_creates_ai_recommendation(self):
        response = self.client.post(
            reverse("add_asset"),
            {
                "asset_id": "TEST-LT-001",
                "device_name": "Test Laptop",
                "device_type": "Laptop",
                "purchase_date": date.today() - timedelta(days=365),
                "condition_score": 9,
                "operational_status": "Active",
            },
        )
        self.assertEqual(response.status_code, 302)
        asset = ElectronicAsset.objects.get(asset_id="TEST-LT-001")
        self.assertEqual(asset.ai_decision, "CONTINUE")
        self.assertTrue(asset.ai_recommendation)
        self.assertEqual(SustainabilityLog.objects.count(), 1)

    def test_asset_list_search(self):
        ElectronicAsset.objects.create(
            asset_id="SEARCH-001",
            device_name="Engineering Laptop",
            device_type="Laptop",
            purchase_date=date.today(),
            condition_score=8,
            operational_status="Active",
        )
        response = self.client.get(
            reverse("asset_list"),
            {"q": "Engineering"},
        )
        self.assertContains(response, "Engineering Laptop")

    def test_responsible_ai_loads(self):
        response = self.client.get(reverse("responsible_ai"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fairness")
        self.assertContains(response, "Transparency")
        self.assertContains(response, "Privacy")
        self.assertContains(response, "Ethics")


class AssetDetailViewTests(TestCase):
    def setUp(self):
        self.asset = ElectronicAsset.objects.create(
            asset_id="DETAIL-LT-001",
            device_name="Detail Test Laptop",
            device_type="Laptop",
            purchase_date=date.today() - timedelta(days=730),
            condition_score=7,
            operational_status="Active",
            ai_decision="MAINTAIN",
            ai_recommendation="Diagnosis: test\n\nRecommendation: maintain",
            ai_confidence=87,
            ai_model="EcoTrace Rules Engine",
            ai_source="Local deterministic fallback",
        )

    def test_detail_page_loads(self):
        response = self.client.get(
            reverse("asset_detail", kwargs={"asset_id": "DETAIL-LT-001"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DETAIL-LT-001")
        self.assertContains(response, "Detail Test Laptop")

    def test_detail_page_shows_ai_recommendation(self):
        response = self.client.get(
            reverse("asset_detail", kwargs={"asset_id": "DETAIL-LT-001"})
        )
        self.assertContains(response, "MAINTAIN")
        self.assertContains(response, "Decision support")

    def test_detail_page_shows_human_oversight_section(self):
        response = self.client.get(
            reverse("asset_detail", kwargs={"asset_id": "DETAIL-LT-001"})
        )
        self.assertContains(response, "AI recommends")
        self.assertContains(response, "Humans remain accountable")

    def test_detail_page_404_for_unknown_asset(self):
        response = self.client.get(
            reverse("asset_detail", kwargs={"asset_id": "DOES-NOT-EXIST"})
        )
        self.assertEqual(response.status_code, 404)

    def test_status_update_post_redirects(self):
        response = self.client.post(
            reverse("asset_detail", kwargs={"asset_id": "DETAIL-LT-001"}),
            {"operational_status": "Maintenance"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("asset_detail", kwargs={"asset_id": "DETAIL-LT-001"}),
        )

    def test_status_update_persists(self):
        self.client.post(
            reverse("asset_detail", kwargs={"asset_id": "DETAIL-LT-001"}),
            {"operational_status": "Maintenance"},
        )
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.operational_status, "Maintenance")

    def test_status_update_creates_sustainability_log(self):
        initial_log_count = SustainabilityLog.objects.filter(asset=self.asset).count()
        self.client.post(
            reverse("asset_detail", kwargs={"asset_id": "DETAIL-LT-001"}),
            {"operational_status": "Retired"},
        )
        self.assertEqual(
            SustainabilityLog.objects.filter(asset=self.asset).count(),
            initial_log_count + 1,
        )
        log = SustainabilityLog.objects.filter(asset=self.asset).first()
        self.assertIn("Human review", log.action)
        self.assertIn("Retired", log.action)

    def test_status_update_invalid_value_does_not_save(self):
        response = self.client.post(
            reverse("asset_detail", kwargs={"asset_id": "DETAIL-LT-001"}),
            {"operational_status": "InvalidStatus"},
        )
        # Should render the page again (200), not redirect
        self.assertEqual(response.status_code, 200)
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.operational_status, "Active")
