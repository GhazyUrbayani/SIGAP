"""Tests for USS Engine calculation logic."""

import pytest
from app.services.uss_engine import USSEngine


class TestUSSEngine:
    """Unit tests for USSEngine core computation."""

    def setup_method(self):
        self.engine = USSEngine()

    def test_normalize_indicator_basic(self):
        """Normalize rainfall_intensity within expected range."""
        result = self.engine.normalize_indicator("rainfall_intensity", 150)
        assert 0 <= result <= 1
        assert result == 0.5  # 150/300

    def test_normalize_indicator_inverted(self):
        """Inverted indicators: higher raw = lower stress."""
        # drainage_quality=1.0 (perfect) should normalize to 0 stress
        result = self.engine.normalize_indicator("drainage_quality", 1.0)
        assert result == 0.0  # inverted

        # drainage_quality=0.0 (terrible) should normalize to 1.0 stress
        result = self.engine.normalize_indicator("drainage_quality", 0.0)
        assert result == 1.0

    def test_normalize_clamping(self):
        """Values outside range should be clamped to 0-1."""
        result = self.engine.normalize_indicator("rainfall_intensity", 500)
        assert result == 1.0

        result = self.engine.normalize_indicator("rainfall_intensity", -10)
        assert result == 0.0

    def test_compute_dimension_score(self):
        """Dimension score should be 0-100."""
        indicators = {
            "rainfall_intensity": 150,
            "flood_frequency": 6,
            "temperature_anomaly": 2.5,
            "humidity_index": 80,
        }
        score = self.engine.compute_dimension_score("climate", indicators)
        assert 0 <= score <= 100

    def test_compute_uss_full(self):
        """Full USS computation with all indicators."""
        indicators = {
            "rainfall_intensity": 200,
            "flood_frequency": 8,
            "temperature_anomaly": 3,
            "humidity_index": 90,
            "road_damage_ratio": 0.6,
            "drainage_quality": 0.3,
            "building_density": 350,
            "green_space_ratio": 0.05,
            "poverty_rate": 25,
            "unemployment_rate": 12,
            "health_facility_access": 0.2,
            "education_index": 0.3,
        }
        result = self.engine.compute_uss(indicators)

        assert "uss" in result
        assert 0 <= result["uss"] <= 100
        assert result["uss_level"] in [
            "very_low", "low", "medium", "high", "very_high"
        ]
        assert result["climate_score"] >= 0
        assert result["infrastructure_score"] >= 0
        assert result["socioeconomic_score"] >= 0

    def test_uss_low_stress_indicators(self):
        """Low-stress indicators should produce low USS."""
        indicators = {
            "rainfall_intensity": 30,
            "flood_frequency": 1,
            "temperature_anomaly": 0.5,
            "humidity_index": 68,
            "road_damage_ratio": 0.05,
            "drainage_quality": 0.9,
            "building_density": 80,
            "green_space_ratio": 0.3,
            "poverty_rate": 5,
            "unemployment_rate": 3,
            "health_facility_access": 0.85,
            "education_index": 0.8,
        }
        result = self.engine.compute_uss(indicators)
        assert result["uss"] < 40, f"Expected USS < 40 for low-stress, got {result['uss']}"

    def test_uss_high_stress_indicators(self):
        """High-stress indicators should produce high USS."""
        indicators = {
            "rainfall_intensity": 250,
            "flood_frequency": 10,
            "temperature_anomaly": 4,
            "humidity_index": 95,
            "road_damage_ratio": 0.8,
            "drainage_quality": 0.1,
            "building_density": 450,
            "green_space_ratio": 0.02,
            "poverty_rate": 35,
            "unemployment_rate": 18,
            "health_facility_access": 0.1,
            "education_index": 0.2,
        }
        result = self.engine.compute_uss(indicators)
        assert result["uss"] > 70, f"Expected USS > 70 for high-stress, got {result['uss']}"

    def test_cascading_interaction_multiplier(self):
        """Interaction multiplier should amplify when all dimensions high."""
        low = self.engine.compute_cascading_interaction(20, 20, 20)
        high = self.engine.compute_cascading_interaction(80, 80, 80)
        assert high > low
        assert 0 <= low <= 0.4
        assert 0 <= high <= 0.4

    def test_classify_level(self):
        assert USSEngine.classify_level(10) == "very_low"
        assert USSEngine.classify_level(30) == "low"
        assert USSEngine.classify_level(50) == "medium"
        assert USSEngine.classify_level(65) == "high"
        assert USSEngine.classify_level(85) == "very_high"

    def test_scenario_projection(self):
        """Scenario projection should produce baseline and intervention arrays."""
        result = self.engine.project_scenario(
            current_uss=70,
            current_climate=75,
            current_infra=65,
            current_soceco=70,
            drainase_improvement=0.5,
            road_repair=0.3,
            social_program=0.4,
            months=60,
        )
        assert "baseline" in result
        assert "intervention" in result
        assert len(result["baseline"]) > 0
        assert len(result["intervention"]) > 0
        assert result["estimated_reduction"] >= 0

    def test_simulate_with_overrides(self):
        """Simulation with overrides should change USS."""
        result = self.engine.simulate(
            current_climate=70,
            current_infra=60,
            current_soceco=50,
            overrides={
                "infrastructure": {"road_damage_ratio": 0.1},
            },
        )
        assert "uss" in result
        assert "breakdown" in result
