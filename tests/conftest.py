# tests/conftest.py
"""
Pytest fixtures and configuration
"""
import pytest
import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_spec():
    """Sample building specification for testing"""
    return {
        "parameters": {
            "height_m": 20,
            "width_m": 30,
            "depth_m": 20,
            "setback_m": 3,
            "floor_height_m": 3,
            "type": "residential",
            "fsi": 2.0
        },
        "status": "compliant"
    }


@pytest.fixture
def sample_rule():
    """Sample DCR rule for testing"""
    return {
        "city": "Mumbai",
        "authority": "MCGM",
        "clause_no": "DCPR 2034-12.3",
        "page": 12,
        "rule_type": "Residential",
        "conditions": "Height <= 24m",
        "entitlements": "Max 7 floors",
        "notes": "Test rule",
        "parsed_fields": {
            "height_m": 24.0,
            "floors": 7,
            "setback_m": 3.0
        }
    }


@pytest.fixture
def sample_subject():
    """Sample subject for calculator agent testing"""
    return {
        "height_m": 20,
        "width_m": 30,
        "depth_m": 20,
        "setback_m": 3,
        "fsi": 2.0,
        "type": "residential"
    }


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary output directory for tests"""
    output_dir = tmp_path / "outputs"
    geometry_dir = output_dir / "geometry"
    geometry_dir.mkdir(parents=True)
    return str(output_dir)


@pytest.fixture
def mock_mcp_response():
    """Mock MCP API response"""
    return {
        "success": True,
        "inserted_id": "test_id_123",
        "message": "Rule saved successfully"
    }


@pytest.fixture
def sample_cities():
    """List of supported cities"""
    return ["Mumbai", "Ahmedabad", "Pune", "Nashik"]


@pytest.fixture
def sample_building_spec():
    """Alias for sample_spec for compatibility"""
    return {
        "parameters": {
            "height_m": 20,
            "width_m": 30,
            "depth_m": 20,
            "setback_m": 3,
            "floor_height_m": 3,
            "type": "residential",
            "fsi": 2.0
        },
        "status": "compliant"
    }


@pytest.fixture
def temp_spec_file(tmp_path):
    """Create a temporary spec file for testing"""
    spec_file = tmp_path / "test_spec.json"
    spec_data = {
        "parameters": {
            "height_m": 20,
            "width_m": 30,
            "depth_m": 20,
            "setback_m": 3,
            "type": "residential"
        }
    }
    with open(spec_file, 'w') as f:
        json.dump(spec_data, f)
    return str(spec_file)


@pytest.fixture
def mcp_base_url():
    """MCP API base URL"""
    return "http://127.0.0.1:5001"


@pytest.fixture
def mcp_url():
    """MCP API full URL"""
    return "http://127.0.0.1:5001/api/mcp"
