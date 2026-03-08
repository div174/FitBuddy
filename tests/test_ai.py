"""
FitBuddy – Unit tests for AI service layer
Run: pytest tests/ -v
"""
import pytest
from unittest.mock import patch, MagicMock
from app.ai import (
    _clean_json, _calculate_tdee, generate_ai_tips,
    generate_workout_plan, generate_diet_plan,
)

SAMPLE_PROFILE = {
    "name": "Alex",
    "age": 25,
    "gender": "male",
    "weight": 75.0,
    "height": 178.0,
    "goal": "muscle gain",
    "fitness_level": "intermediate",
    "days_per_week": 4,
    "workout_duration": 45,
    "equipment": "dumbbells, barbell",
    "dietary_preference": "no preference",
    "health_conditions": None,
    "activity_level": "moderate",
    "meals_per_day": 3,
    "budget": "moderate",
}


def test_clean_json_strips_fences():
    raw = "```json\n{\"key\": \"val\"}\n```"
    assert _clean_json(raw) == '{"key": "val"}'


def test_clean_json_no_fences():
    raw = '{"key": "val"}'
    assert _clean_json(raw) == '{"key": "val"}'


def test_calculate_tdee_male():
    tdee = _calculate_tdee(75, 178, 25, "male", "moderate")
    assert 2400 < tdee < 3200


def test_calculate_tdee_female():
    tdee = _calculate_tdee(60, 165, 28, "female", "light")
    assert 1600 < tdee < 2400


def test_calculate_tdee_activity_scaling():
    sedentary = _calculate_tdee(75, 178, 25, "male", "sedentary")
    very_active = _calculate_tdee(75, 178, 25, "male", "very active")
    assert very_active > sedentary


@patch("app.ai._call")
def test_generate_workout_plan_success(mock_call):
    mock_call.return_value = """{
        "planName": "Test Plan",
        "overview": "A great plan.",
        "durationWeeks": 8,
        "schedule": [],
        "principles": [],
        "weeklyStats": {
            "trainingDays": 4, "restDays": 3,
            "totalMinutes": 180, "estimatedWeeklyCalories": 1800,
            "primaryMuscles": ["Chest", "Back"]
        }
    }"""
    result = generate_workout_plan(SAMPLE_PROFILE)
    assert result["planName"] == "Test Plan"
    assert "schedule" in result


@patch("app.ai._call")
def test_generate_diet_plan_success(mock_call):
    mock_call.return_value = """{
        "planName": "Muscle Gain Diet",
        "overview": "High protein plan.",
        "dailyTargets": {"calories": 2800, "proteinG": 180, "carbsG": 300, "fatsG": 80, "fiberG": 30, "waterL": 3.0},
        "weeklyMeals": [],
        "shoppingList": {},
        "nutritionTips": [],
        "hydrationSchedule": []
    }"""
    result = generate_diet_plan(SAMPLE_PROFILE)
    assert result["dailyTargets"]["proteinG"] == 180


@patch("app.ai._call")
def test_generate_ai_tips(mock_call):
    mock_call.return_value = "1. Eat more protein.\n2. Sleep 8 hours.\n3. Train progressively."
    result = generate_ai_tips(SAMPLE_PROFILE)
    assert "protein" in result.lower() or len(result) > 10


@patch("app.ai._call")
def test_ai_call_failure_raises(mock_call):
    mock_call.side_effect = Exception("API error")
    with pytest.raises(Exception):
        generate_workout_plan(SAMPLE_PROFILE)
