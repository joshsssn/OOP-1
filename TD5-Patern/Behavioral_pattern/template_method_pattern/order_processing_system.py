import json
from abc import ABC, abstractmethod

class FormatStrategy(ABC):
    @abstractmethod
    def format_report(self, data: list) -> str:
        pass

    @abstractmethod
    def get_extension(self) -> str:
        pass

class PDFFormatStrategy(FormatStrategy):
    def format_report(self, data: list) -> str:
        return f"PDF Report: {data}"

    def get_extension(self) -> str:
        return ".pdf"

class ExcelFormatStrategy(FormatStrategy):
    def format_report(self, data: list) -> str:
        return f"Excel Report: {data}"

    def get_extension(self) -> str:
        return ".xlsx"

class CSVFormatStrategy(FormatStrategy):
    def format_report(self, data: list) -> str:
        return f"CSV Report: {data}"

    def get_extension(self) -> str:
        return ".csv"

class JSONFormatStrategy(FormatStrategy):
    def format_report(self, data: list) -> str:
        return json.dumps(data)

    def get_extension(self) -> str:
        return ".json"

class HTMLFormatStrategy(FormatStrategy):
    def format_report(self, data: list) -> str:
        return f"<html><body>{data}</body></html>"

    def get_extension(self) -> str:
        return ".html"

class ReportGenerator:
    def __init__(self, data: list):
        self._data = data
        self._strategy = None

    def set_strategy(self, strategy: FormatStrategy) -> None:
        self._strategy = strategy

    def generate_report(self) -> str:
        if self._strategy:
            return self._strategy.format_report(self._data)
        return ""

    def save_report(self, filename: str) -> None:
        if self._strategy:
            with open(filename + self._strategy.get_extension(), "w") as f:
                f.write(self.generate_report())


# ─────────────────────────────────────────────
# 4. NEW FORMAT: HTML (added without modifying
#    ANY existing strategy class)
# ─────────────────────────────────────────────

class HTMLFormatStrategy(FormatStrategy):
    """Formats report as an HTML table."""

    def format_report(self, data: list) -> str:
        html = "<html>\n<body>\n"
        html += "<h1>Report</h1>\n"
        html += "<table border='1'>\n"
        html += "  <tr><th>Name</th><th>Value</th></tr>\n"
        for item in data:
            html += f"  <tr><td>{item['name']}</td><td>{item['value']}</td></tr>\n"
        html += "</table>\n"
        html += "</body>\n</html>"
        return html

    def get_extension(self) -> str:
        return ".html"


# ─────────────────────────────────────────────
# Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":

    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000}
    ]

    generator = ReportGenerator(data)

    # PDF format
    print("=== PDF FORMAT ===")
    generator.set_strategy(PDFFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    # Switch to CSV dynamically
    print("=== CSV FORMAT ===")
    generator.set_strategy(CSVFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    # Switch to JSON
    print("=== JSON FORMAT ===")
    generator.set_strategy(JSONFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    # Switch to Excel
    print("=== EXCEL FORMAT ===")
    generator.set_strategy(ExcelFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    # NEW: HTML format — zero existing code modified
    print("=== HTML FORMAT (NEW!) ===")
    generator.set_strategy(HTMLFormatStrategy())
    print(generator.generate_report())

    # Save a report
    print("\n" + "=" * 60 + "\n")
    generator.set_strategy(CSVFormatStrategy())
    generator.save_report("sales_report")
