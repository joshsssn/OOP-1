"""
Adapter Pattern - Reporting System
===================================
Refactored from scattered XML-to-JSON conversion logic
into an Adapter that wraps the legacy XML report generator
and exposes a JSON-compatible interface.
"""

import json
import re
from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
# Legacy system (CAN'T MODIFY - external library)
# ─────────────────────────────────────────────

class LegacyReportGenerator:
    """Returns XML format - old system we cannot touch."""

    def generate_report(self, data: dict) -> str:
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


# ─────────────────────────────────────────────
# New system (expects JSON)
# ─────────────────────────────────────────────

class AnalyticsDashboard:
    """New analytics dashboard that only accepts JSON."""

    def display(self, json_data: str):
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


# ─────────────────────────────────────────────
# 1. The Interface (expected by the new system)
# ─────────────────────────────────────────────

class ReportGeneratorInterface(ABC):
    """
    Contract: any report generator must return JSON.
    This is what the new dashboard and tools expect.
    """

    @abstractmethod
    def generate(self, data: dict) -> str:
        """Generate a report and return it as a JSON string."""
        pass


# ─────────────────────────────────────────────
# 2. The Adapter (bridges legacy XML → JSON)
# ─────────────────────────────────────────────

class LegacyReportAdapter(ReportGeneratorInterface):
    """
    Wraps the legacy XML generator and converts its
    output to JSON. The dashboard never knows it's
    talking to an old XML system underneath.
    """

    def __init__(self, legacy_generator: LegacyReportGenerator):
        self._legacy = legacy_generator

    def _xml_to_dict(self, xml: str) -> dict:
        """Parse the legacy XML format into a Python dict."""
        result = {}
        pattern = r"<(\w+)>(.*?)</\1>"
        matches = re.findall(pattern, xml)

        for key, value in matches:
            if key == "report":
                continue
            # Preserve numeric types
            try:
                if "." in value:
                    result[key] = float(value)
                else:
                    result[key] = int(value)
            except ValueError:
                result[key] = value

        return result

    def generate(self, data: dict) -> str:
        """
        1. Call the legacy system (gets XML)
        2. Parse XML → dict
        3. Convert dict → JSON string
        """
        xml_report = self._legacy.generate_report(data)
        parsed = self._xml_to_dict(xml_report)
        return json.dumps(parsed)


# ─────────────────────────────────────────────
# Usage (clean, no conversion logic scattered)
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # Set up once: wrap the legacy system in the adapter
    legacy = LegacyReportGenerator()
    report_generator = LegacyReportAdapter(legacy)
    dashboard = AnalyticsDashboard()

    # Sales report
    print("--- Sales Report ---")
    sales_data = {"total_sales": 150000, "orders": 1234, "avg_order": 121.55}
    json_report = report_generator.generate(sales_data)
    dashboard.display(json_report)

    # Inventory report — same clean flow, no repeated conversion
    print("\n--- Inventory Report ---")
    inventory_data = {"total_items": 5000, "low_stock": 45, "out_of_stock": 12}
    json_report = report_generator.generate(inventory_data)
    dashboard.display(json_report)

    # Proof: show what happens at each step
    print("\n--- Under the hood ---")
    xml_output = legacy.generate_report(sales_data)
    print(f"Legacy XML:\n{xml_output}")
    print(f"\nAdapter JSON:\n{report_generator.generate(sales_data)}")
