import time
from abc import ABC, abstractmethod

class DataPipeline(ABC):
    def __init__(self, source: str):
        self._source = source
        self._data = None

    def run(self) -> str:
        self._connect()
        self._before_extract()
        self._data = self._extract()
        self._data = self._transform(self._data)
        self._validate(self._data)
        self._load(self._data)
        self._after_load()
        self._cleanup()
        return f"{self.__class__.__name__} finished successfully"

    def _connect(self) -> None:
        print(f"Connecting to: {self._source}")
        time.sleep(0.3)

    def _load(self, data: list) -> None:
        print(f"Loading {len(data)} records")

    def _cleanup(self) -> None:
        self._data = None

    def _before_extract(self) -> None:
        pass

    def _after_load(self) -> None:
        pass

    @abstractmethod
    def _extract(self) -> list:
        pass

    @abstractmethod
    def _transform(self, data: list) -> list:
        pass

    @abstractmethod
    def _validate(self, data: list) -> None:
        pass

class CSVPipeline(DataPipeline):
    def _connect(self) -> None:
        print(f"CSVPipeline connecting to {self._source}")

    def _extract(self) -> list:
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    def _transform(self, data: list) -> list:
        return data

    def _validate(self, data: list) -> None:
        pass

class APIPipeline(DataPipeline):
    def _connect(self) -> None:
        print(f"APIPipeline connecting to {self._source}")

    def _extract(self) -> list:
        return [{"id": 3, "name": "Charlie"}]

    def _transform(self, data: list) -> list:
        return data

    def _validate(self, data: list) -> None:
        pass

class DatabasePipeline(DataPipeline):
    def _connect(self) -> None:
        print(f"DatabasePipeline connecting to {self._source}")

    def _extract(self) -> list:
        return [{"id": 4, "name": "Dave"}]

    def _transform(self, data: list) -> list:
        return data

    def _validate(self, data: list) -> None:
        pass

class XMLPipeline(DataPipeline):
    def _connect(self) -> None:
        print(f"XMLPipeline connecting to {self._source}")

    def _extract(self) -> list:
        return [{"id": 5, "name": "Eve"}]

    def _transform(self, data: list) -> list:
        return data

    def _validate(self, data: list) -> None:
        pass

    def _after_load(self) -> None:
        print("XMLPipeline finished loading")


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
