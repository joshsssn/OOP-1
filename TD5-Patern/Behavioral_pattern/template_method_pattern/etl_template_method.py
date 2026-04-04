"""
Template Method Pattern - Data ETL Pipeline
=============================================
Refactored from three copy-pasted pipeline classes
into a base class with a fixed algorithm skeleton
and subclasses that only override what's unique.

Problems with the original implementation:
──────────────────────────────────────────
1. MASSIVE DUPLICATION — The validation logic is copy-pasted
   3 times, the cleanup logic 3 times, the load logic 3 times.
   A bug fix in one must be manually replicated to all others.

2. WORKFLOW NOT ENFORCED — Nothing prevents a subclass from
   skipping validation or cleanup. Each pipeline defines its
   own run() with its own step order — if one developer forgets
   a step, it silently fails.

3. CROSS-CUTTING CHANGES ARE PAINFUL — Want to add logging
   or timing to all pipelines? You must edit all three run()
   methods identically. With 10 pipelines, that's 10 edits.

4. INCONSISTENT STEP ORDER — Nothing guarantees that CSV,
   API, and Database pipelines execute steps in the same
   order. One could validate before transform by accident.

5. NO HOOK POINTS — There's no way to inject optional behavior
   (like sending a notification after load) without modifying
   the entire run() method in each class.
"""

import time
from abc import ABC, abstractmethod


# ─────────────────────────────────────────────
# 1. Abstract Base Class (template method)
# ─────────────────────────────────────────────

class DataPipeline(ABC):
    """
    Defines the ETL workflow skeleton in run().
    Subclasses override only the steps that differ:
    extract(), transform(), validate().

    Common steps (connect, load, cleanup) are implemented
    once here and shared by all pipelines.
    """

    def __init__(self, source: str):
        self._source = source
        self._data = None

    # ── Template Method (fixed skeleton — do NOT override) ──

    def run(self) -> str:
        """
        The template method. Defines the algorithm's step order.
        Subclasses cannot change this order — only the individual steps.
        """
        self._connect()
        self._before_extract()          # hook (optional)
        self._data = self._extract()
        self._data = self._transform(self._data)
        self._validate(self._data)
        self._load(self._data)
        self._after_load()              # hook (optional)
        self._cleanup()
        return f"{self.__class__.__name__} finished successfully"

    # ── Common steps (implemented once, shared by all) ──

    def _connect(self) -> None:
        """Connect to the data source."""
        print(f"  Connecting to: {self._source}")
        time.sleep(0.3)
        print("  Connection established")

    def _load(self, data: list) -> None:
        """Load transformed data to destination."""
        print(f"  Loading {len(data)} records to destination...")
        time.sleep(0.3)
        print(f"  Loaded {len(data)} records successfully")

    def _cleanup(self) -> None:
        """Release resources."""
        print("  Cleaning up resources...")
        self._data = None
        print("  Cleanup complete")

    # ── Hook methods (optional — subclasses CAN override) ──

    def _before_extract(self) -> None:
        """Hook: called before extraction. Override for custom logic."""
        pass

    def _after_load(self) -> None:
        """Hook: called after loading. Override for notifications, etc."""
        pass

    # ── Abstract methods (subclasses MUST override) ──

    @abstractmethod
    def _extract(self) -> list:
        """Extract data from source. Each pipeline has its own logic."""
        pass

    @abstractmethod
    def _transform(self, data: list) -> list:
        """Transform extracted data. Each pipeline has its own rules."""
        pass

    @abstractmethod
    def _validate(self, data: list) -> None:
        """Validate data integrity. Each pipeline checks different fields."""
        pass


# ─────────────────────────────────────────────
# 2. Concrete Pipelines
# ─────────────────────────────────────────────

class CSVPipeline(DataPipeline):
    """ETL pipeline for CSV file sources."""

    def _extract(self) -> list:
        print("  Extracting data from CSV file...")
        data = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25}
        ]
        print(f"  Extracted {len(data)} records from CSV")
        return data

    def _transform(self, data: list) -> list:
        print("  Transforming CSV data...")
        for record in data:
            record["age"] = int(record["age"])
            record["name"] = record["name"].upper()
        print("  CSV transformation complete")
        return data

    def _validate(self, data: list) -> None:
        print("  Validating CSV data...")
        for record in data:
            if "id" not in record or "name" not in record:
                raise ValueError("CSV record missing required fields: id, name")
        print("  CSV validation passed")


class APIPipeline(DataPipeline):
    """ETL pipeline for REST API sources."""

    def _extract(self) -> list:
        print("  Extracting data from API...")
        data = [
            {"user_id": 101, "username": "charlie", "score": 85},
            {"user_id": 102, "username": "diana", "score": 92}
        ]
        print(f"  Extracted {len(data)} records from API")
        return data

    def _transform(self, data: list) -> list:
        print("  Transforming API data...")
        for record in data:
            record["score"] = int(record["score"])
            record["username"] = record["username"].lower()
            record["grade"] = "A" if record["score"] >= 90 else "B"
        print("  API transformation complete")
        return data

    def _validate(self, data: list) -> None:
        print("  Validating API data...")
        for record in data:
            if "user_id" not in record or "username" not in record:
                raise ValueError("API record missing required fields: user_id, username")
        print("  API validation passed")


class DatabasePipeline(DataPipeline):
    """ETL pipeline for database sources."""

    def _extract(self) -> list:
        print("  Extracting data from database...")
        data = [
            {"product_id": 501, "product_name": "Laptop", "price": 1200},
            {"product_id": 502, "product_name": "Mouse", "price": 25}
        ]
        print(f"  Extracted {len(data)} records from database")
        return data

    def _transform(self, data: list) -> list:
        print("  Transforming database data...")
        for record in data:
            record["price"] = float(record["price"])
            record["product_name"] = record["product_name"].title()
            record["tax"] = record["price"] * 0.2
        print("  Database transformation complete")
        return data

    def _validate(self, data: list) -> None:
        print("  Validating database data...")
        for record in data:
            if "product_id" not in record or "price" not in record:
                raise ValueError("DB record missing required fields: product_id, price")
        print("  Database validation passed")


# ─────────────────────────────────────────────
# 3. Extensibility Proof: XML Pipeline
#    (added without modifying ANY existing class)
# ─────────────────────────────────────────────

class XMLPipeline(DataPipeline):
    """ETL pipeline for XML file sources."""

    def _extract(self) -> list:
        print("  Extracting data from XML file...")
        data = [
            {"order_id": 1001, "customer": "Eve", "total": 250.00},
            {"order_id": 1002, "customer": "Frank", "total": 89.99}
        ]
        print(f"  Extracted {len(data)} records from XML")
        return data

    def _transform(self, data: list) -> list:
        print("  Transforming XML data...")
        for record in data:
            record["total"] = float(record["total"])
            record["customer"] = record["customer"].strip().title()
            record["currency"] = "EUR"
        print("  XML transformation complete")
        return data

    def _validate(self, data: list) -> None:
        print("  Validating XML data...")
        for record in data:
            if "order_id" not in record or "total" not in record:
                raise ValueError("XML record missing required fields: order_id, total")
        print("  XML validation passed")

    # ── Using a hook: log after load ──

    def _after_load(self) -> None:
        print("  [XMLPipeline hook] Sending notification: XML load complete!")


# ─────────────────────────────────────────────
# Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":

    print("RUNNING CSV PIPELINE")
    print("=" * 70)
    csv_pipeline = CSVPipeline("data/users.csv")
    result = csv_pipeline.run()
    print(f"\n{result}\n")

    print("RUNNING API PIPELINE")
    print("=" * 70)
    api_pipeline = APIPipeline("https://api.example.com/users")
    result = api_pipeline.run()
    print(f"\n{result}\n")

    print("RUNNING DATABASE PIPELINE")
    print("=" * 70)
    db_pipeline = DatabasePipeline("postgresql://localhost/mydb")
    result = db_pipeline.run()
    print(f"\n{result}\n")

    print("RUNNING XML PIPELINE (NEW!)")
    print("=" * 70)
    xml_pipeline = XMLPipeline("data/orders.xml")
    result = xml_pipeline.run()
    print(f"\n{result}\n")
