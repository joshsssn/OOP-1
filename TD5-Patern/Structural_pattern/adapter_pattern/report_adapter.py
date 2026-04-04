import json
import re
from abc import ABC, abstractmethod

class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml

class AnalyticsDashboard:
    def display(self, json_data: str):
        data = json.loads(json_data)
        for key, value in data.items():
            print(f"{key}: {value}")

class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        pass

class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy_generator: LegacyReportGenerator):
        self._legacy = legacy_generator

    def generate(self, data: dict) -> str:
        xml_report = self._legacy.generate_report(data)
        # Naive XML parsing to convert back dict for JSON
        result = {}
        for line in xml_report.split("\n"):
            if not line.strip() or line.strip() in ['<report>', '</report>']:
                continue
            match = re.search(r"<(.*?)>(.*?)</\1>", line)
            if match:
                result[match.group(1)] = match.group(2)
        return json.dumps(result)


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
