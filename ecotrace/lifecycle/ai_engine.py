import json
import logging
from datetime import date

from django.conf import settings

logger = logging.getLogger(__name__)


class IBMBOBAIEngine:
    """
    Application-level AI orchestration layer for EcoTrace.

    "BOB" is treated here as the application workflow/orchestration layer:
    it builds a structured sustainability prompt, invokes IBM Granite when
    configured, validates the response, and falls back to deterministic
    explainable rules when live inference is unavailable.

    The fallback is NOT represented as an IBM model prediction.
    """

    def __init__(self):
        self.model_id = getattr(
            settings,
            "IBM_GRANITE_MODEL_ID",
            "ibm/granite-4-h-small",
        )
        self.enabled = getattr(settings, "IBM_GRANITE_ENABLED", False)
        self.model = None

        if self.enabled:
            self._initialize_granite()

    def _initialize_granite(self):
        try:
            from ibm_watsonx_ai import APIClient, Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference

            credentials = Credentials(
                url=settings.IBM_WATSONX_URL,
                api_key=settings.IBM_WATSONX_API_KEY,
            )
            client = APIClient(
                credentials=credentials,
                project_id=settings.IBM_WATSONX_PROJECT_ID,
            )

            self.model = ModelInference(
                model_id=self.model_id,
                api_client=client,
                project_id=settings.IBM_WATSONX_PROJECT_ID,
                params={
                    "max_new_tokens": 500,
                    "temperature": 0.2,
                },
            )
            logger.info("IBM Granite initialized: %s", self.model_id)
        except Exception:
            logger.exception("IBM Granite initialization failed.")
            self.enabled = False
            self.model = None

    @staticmethod
    def _calculate_age(purchase_date):
        days = max((date.today() - purchase_date).days, 0)
        return round(days / 365.25, 1)

    @staticmethod
    def _build_prompt(
        *,
        asset_id,
        device_name,
        device_type,
        purchase_date,
        age_years,
        condition_score,
        operational_status,
    ):
        return f"""
You are the EcoTrace Responsible Technology AI Agent.

Goal:
Support responsible electronic-device lifecycle management aligned
with UN SDG 12: Responsible Consumption and Production.

Use only the supplied asset information. Do not infer protected personal
characteristics or use personal data. Prefer extending useful life when
repair/maintenance is technically reasonable. Do not recommend replacement
solely because a device is old.

Asset ID: {asset_id}
Device: {device_name}
Device type: {device_type}
Purchase date: {purchase_date}
Estimated age: {age_years} years
Condition score: {condition_score}/10
Operational status: {operational_status}

Return ONLY valid JSON in this schema:
{{
  "decision": "CONTINUE|MAINTAIN|REPAIR|RECYCLE",
  "diagnosis": "brief explainable diagnosis",
  "maintenance_priority": "LOW|MEDIUM|HIGH|CRITICAL",
  "recommendation": "actionable next step",
  "environmental_reason": "sustainability rationale",
  "confidence": 0.0
}}
"""

    def analyze_asset(
        self,
        *,
        asset_id,
        device_name,
        device_type,
        purchase_date,
        condition_score,
        operational_status,
    ):
        age_years = self._calculate_age(purchase_date)
        prompt = self._build_prompt(
            asset_id=asset_id,
            device_name=device_name,
            device_type=device_type,
            purchase_date=purchase_date,
            age_years=age_years,
            condition_score=condition_score,
            operational_status=operational_status,
        )

        if self.enabled and self.model:
            try:
                return self._run_granite(prompt)
            except Exception:
                logger.exception("Granite inference failed; using fallback.")

        return self._fallback_analysis(
            age_years=age_years,
            condition_score=condition_score,
            device_type=device_type,
            operational_status=operational_status,
        )

    def _run_granite(self, prompt):
        response = self.model.generate_text(prompt=prompt)
        parsed = self._parse_json_response(response)

        result = {
            "decision": parsed.get("decision", "MAINTAIN"),
            "diagnosis": parsed.get(
                "diagnosis",
                "AI diagnosis was not returned.",
            ),
            "maintenance_priority": parsed.get(
                "maintenance_priority",
                "MEDIUM",
            ),
            "recommendation": parsed.get(
                "recommendation",
                "Schedule technical inspection.",
            ),
            "environmental_reason": parsed.get(
                "environmental_reason",
                "Extending useful device life can reduce premature e-waste.",
            ),
            "confidence": self._safe_confidence(
                parsed.get("confidence", 0.75)
            ),
            "model": self.model_id,
            "source": "IBM Granite via watsonx.ai",
        }

        if result["decision"] not in {"CONTINUE", "MAINTAIN", "REPAIR", "RECYCLE"}:
            result["decision"] = "MAINTAIN"

        return result

    @staticmethod
    def _parse_json_response(response):
        if isinstance(response, dict):
            return response
        if not isinstance(response, str):
            return {}

        text = response.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start, end = text.find("{"), text.rfind("}")
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start:end + 1])
                except json.JSONDecodeError:
                    pass
        return {}

    @staticmethod
    def _safe_confidence(value):
        try:
            confidence = float(value)
            if confidence > 1:
                confidence /= 100
            return round(min(max(confidence, 0), 1), 2)
        except (TypeError, ValueError):
            return 0.75

    @staticmethod
    def _fallback_analysis(
        *,
        age_years,
        condition_score,
        device_type,
        operational_status,
    ):
        if operational_status == "Recycled":
            return {
                "decision": "RECYCLE",
                "diagnosis": "Asset is already marked for recycling.",
                "maintenance_priority": "LOW",
                "recommendation": (
                    "Complete data sanitization and route the asset "
                    "through an approved e-waste recycling pathway."
                ),
                "environmental_reason": (
                    "Controlled recycling supports material recovery "
                    "and reduces uncontrolled e-waste disposal."
                ),
                "confidence": 0.99,
                "model": "EcoTrace Rules Engine",
                "source": "Local deterministic fallback",
            }

        if condition_score <= 3:
            decision = "RECYCLE"
            priority = "CRITICAL"
            recommendation = (
                "Perform final technical and data-security assessment, "
                "then prioritize certified e-waste recycling."
            )
            reason = (
                "Very low condition suggests limited remaining useful life; "
                "controlled end-of-life processing is preferable to indefinite storage."
            )
            confidence = 0.91
        elif condition_score <= 5:
            decision = "REPAIR"
            priority = "HIGH"
            recommendation = (
                "Schedule technical inspection and repair before considering replacement."
            )
            reason = (
                "Repair may extend useful life and defer premature e-waste."
            )
            confidence = 0.84
        elif condition_score <= 7:
            decision = "MAINTAIN"
            priority = "MEDIUM"
            recommendation = (
                "Continue operation with preventive maintenance and periodic reassessment."
            )
            reason = (
                "Preventive maintenance can preserve useful life and reduce unnecessary replacement."
            )
            confidence = 0.87
        else:
            decision = "CONTINUE"
            priority = "LOW"
            recommendation = (
                "Continue normal operation and monitor lifecycle health."
            )
            reason = (
                "The current condition score supports continued use."
            )
            confidence = 0.93

        return {
            "decision": decision,
            "diagnosis": (
                f"{device_type} is approximately {age_years} years old "
                f"with a condition score of {condition_score}/10."
            ),
            "maintenance_priority": priority,
            "recommendation": recommendation,
            "environmental_reason": reason,
            "confidence": confidence,
            "model": "EcoTrace Rules Engine",
            "source": "Local deterministic fallback",
        }


ai_engine = IBMBOBAIEngine()
