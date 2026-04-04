"""
Strategy Pattern - Report Generator
=====================================
Refactored from a single class with if/elif chains
into interchangeable format strategies.

Problems with the original implementation:
──────────────────────────────────────────
1. OPEN/CLOSED VIOLATION — Adding a new format (XML, HTML, Markdown)
   requires modifying the existing generate_report() AND save_report()
   methods. Every change risks breaking existing formats.

2. SINGLE RESPONSIBILITY VIOLATION — One class handles PDF formatting,
   Excel formatting, CSV formatting, JSON formatting, AND file saving.
   That's at least 5 reasons to change.

3. CODE DUPLICATION — The save_report() method repeats the same
   if/elif structure as generate_report(). Every new format must be
   added in TWO places, doubling the maintenance cost.

4. UNTESTABLE IN ISOLATION — You can't test PDF generation without
   also having CSV, JSON, Excel code loaded. Each format's logic is
   tangled inside one method, making unit tests coarse-grained.

5. NO RUNTIME FLEXIBILITY — The format is passed as a string, so
   there's no way to inject a custom formatter or swap strategies
   dynamically without touching the core if/elif chain.
"""

import json
from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
# 1. Strategy Interface
# ─────────────────────────────────────────────

class FormatStrategy(ABC):
    """
    Contract for all format strategies.
    Each strategy knows how to format data AND
    what file extension it produces.
    """

    @abstractmethod
    def format_report(self, data: list) -> str:
        """Format the data into a report string."""
        pass

    @abstractmethod
    def get_extension(self) -> str:
        """Return the file extension (e.g. '.csv')."""
        pass


# ─────────────────────────────────────────────
# 2. Concrete Strategies
# ─────────────────────────────────────────────

class PDFFormatStrategy(FormatStrategy):
    """Formats report as a styled PDF-like text output."""

    def format_report(self, data: list) -> str:
        report = "PDF REPORT\n"
        report += "=" * 50 + "\n"
        for item in data:
            report += f"| {item['name']:20} | {item['value']:10} |\n"
        report += "=" * 50 + "\n"
        report += "End of PDF Report"
        return report

    def get_extension(self) -> str:
        return ".pdf"


class ExcelFormatStrategy(FormatStrategy):
    """Formats report as tab-separated values (Excel-like)."""

    def format_report(self, data: list) -> str:
        report = "EXCEL REPORT\n"
        report += "-" * 50 + "\n"
        report += "Name\tValue\n"
        for item in data:
            report += f"{item['name']}\t{item['value']}\n"
        report += "-" * 50 + "\n"
        return report

    def get_extension(self) -> str:
        return ".xlsx"


class CSVFormatStrategy(FormatStrategy):
    """Formats report as comma-separated values."""

    def format_report(self, data: list) -> str:
        report = "name,value\n"
        for item in data:
            report += f"{item['name']},{item['value']}\n"
        return report

    def get_extension(self) -> str:
        return ".csv"


class JSONFormatStrategy(FormatStrategy):
    """Formats report as pretty-printed JSON."""

    def format_report(self, data: list) -> str:
        return json.dumps(data, indent=2)

    def get_extension(self) -> str:
        return ".json"


# ─────────────────────────────────────────────
# 3. Context Class
# ─────────────────────────────────────────────

class ReportGenerator:
    """
    Context that holds data and delegates formatting
    to whichever strategy is currently set.
    The strategy can be swapped at runtime.
    """

    def __init__(self, data: list):
        self._data = data
        self._strategy: FormatStrategy = None

    def set_strategy(self, strategy: FormatStrategy) -> None:
        """Swap the format strategy at runtime."""
        self._strategy = strategy

    def generate_report(self) -> str:
        """Delegate formatting to the current strategy."""
        if not self._strategy:
            raise ValueError("No format strategy set. Call set_strategy() first.")
        return self._strategy.format_report(self._data)

    def save_report(self, filename: str) -> None:
        """Save the formatted report with the correct extension."""
        if not self._strategy:
            raise ValueError("No format strategy set. Call set_strategy() first.")

        content = self.generate_report()
        full_path = filename + self._strategy.get_extension()

        with open(full_path, "w") as f:
            f.write(content)
        print(f"Report saved to '{full_path}'")


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
