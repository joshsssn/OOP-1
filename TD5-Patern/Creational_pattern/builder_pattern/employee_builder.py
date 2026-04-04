"""
Builder Pattern - HR Employee Onboarding System
================================================
Refactored from a 17-parameter telescoping function
into a Fluent Builder that forces labeled, step-by-step
construction of Employee objects.
"""


# ─────────────────────────────────────────────
# 1. The Product (data container)
# ─────────────────────────────────────────────

class Employee:
    """
    Simple data class holding the final state
    of an employee record. Created only by the Builder.
    """

    def __init__(self):
        # Identity
        self.first_name: str = None
        self.last_name: str = None
        self.email: str = None

        # Job info
        self.department: str = None
        self.position: str = None
        self.salary: float = 0.0
        self.start_date: str = None
        self.manager_id: int = None
        self.contract_type: str = "permanent"

        # Contact
        self.phone: str = None
        self.address: str = None
        self.emergency_contact: str = None

        # Equipment
        self.has_laptop: bool = False
        self.has_parking: bool = False

        # Access
        self.has_vpn_access: bool = False
        self.has_admin_rights: bool = False

        # Location
        self.office_location: str = None

    def __repr__(self):
        return (
            f"Employee({self.first_name} {self.last_name}, "
            f"{self.position} @ {self.department}, "
            f"salary={self.salary}, contract={self.contract_type})"
        )


# ─────────────────────────────────────────────
# 2. The Builder (fluent, chainable methods)
# ─────────────────────────────────────────────

class EmployeeBuilder:
    """
    Fluent builder that constructs an Employee step by step.
    Each with_*() method returns self for chaining.
    build() validates and returns the final Employee.
    """

    def __init__(self):
        self._employee = Employee()

    def with_name(self, first_name: str, last_name: str) -> "EmployeeBuilder":
        self._employee.first_name = first_name
        self._employee.last_name = last_name
        return self

    def with_email(self, email: str) -> "EmployeeBuilder":
        self._employee.email = email
        return self

    def with_job(self, department: str, position: str, salary: float) -> "EmployeeBuilder":
        self._employee.department = department
        self._employee.position = position
        self._employee.salary = salary
        return self

    def with_start_date(self, start_date: str) -> "EmployeeBuilder":
        self._employee.start_date = start_date
        return self

    def with_manager(self, manager_id: int) -> "EmployeeBuilder":
        self._employee.manager_id = manager_id
        return self

    def with_contact(self, phone: str = None, address: str = None, emergency: str = None) -> "EmployeeBuilder":
        self._employee.phone = phone
        self._employee.address = address
        self._employee.emergency_contact = emergency
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False) -> "EmployeeBuilder":
        self._employee.has_laptop = laptop
        self._employee.has_parking = parking
        return self

    def with_access(self, vpn: bool = False, admin: bool = False) -> "EmployeeBuilder":
        self._employee.has_vpn_access = vpn
        self._employee.has_admin_rights = admin
        return self

    def with_office(self, location: str, contract: str = "permanent") -> "EmployeeBuilder":
        self._employee.office_location = location
        self._employee.contract_type = contract
        return self

    def build(self) -> Employee:
        """Validate required fields and return the Employee."""
        emp = self._employee

        if not emp.first_name or not emp.last_name:
            raise ValueError("Name is required")
        if not emp.email or "@" not in emp.email:
            raise ValueError("Valid email is required")
        if emp.salary < 0:
            raise ValueError("Salary cannot be negative")

        return emp


# ─────────────────────────────────────────────
# 3. Preset Builder (for common employee types)
# ─────────────────────────────────────────────

class DeveloperBuilder(EmployeeBuilder):
    """
    Preset builder for developers.
    Automatically sets department, equipment, and access
    so HR doesn't have to remember these every time.
    """

    def __init__(self, first_name: str, last_name: str, email: str):
        super().__init__()
        # Pre-fill the common developer settings
        self.with_name(first_name, last_name)
        self.with_email(email)
        self.with_job("Engineering", "Developer", 60000)
        self.with_equipment(laptop=True, parking=False)
        self.with_access(vpn=True, admin=True)
        self.with_office("Paris HQ", "permanent")


# ─────────────────────────────────────────────
# Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # ── Senior Developer (full manual build) ──
    print("=== Senior Developer (fluent build) ===")
    dev = (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Senior Developer", 75000)
        .with_start_date("2024-01-15")
        .with_contact(phone="+33612345678")
        .with_equipment(laptop=True, parking=False)
        .with_access(vpn=True, admin=True)
        .with_office("Paris HQ", "permanent")
        .build()
    )
    print(dev)
    print(f"  Laptop: {dev.has_laptop}, VPN: {dev.has_vpn_access}, Admin: {dev.has_admin_rights}")

    # ── Intern (minimal info, skip what you don't need) ──
    print("\n=== Intern (minimal build) ===")
    intern = (
        EmployeeBuilder()
        .with_name("Jane", "Smith")
        .with_email("jane.smith@company.com")
        .with_job("Marketing", "Intern", 15000)
        .with_start_date("2024-02-01")
        .with_manager(42)
        .with_equipment(laptop=True)
        .with_office("Paris HQ", "internship")
        .build()
    )
    print(intern)
    print(f"  Laptop: {intern.has_laptop}, VPN: {intern.has_vpn_access}, Admin: {intern.has_admin_rights}")

    # ── Developer Preset (one line!) ──
    print("\n=== Developer Preset ===")
    quick_dev = DeveloperBuilder("Alice", "Martin", "alice@company.com").build()
    print(quick_dev)
    print(f"  Laptop: {quick_dev.has_laptop}, VPN: {quick_dev.has_vpn_access}, Admin: {quick_dev.has_admin_rights}")

    # ── Developer Preset with overrides ──
    print("\n=== Developer Preset + custom salary ===")
    senior = (
        DeveloperBuilder("Bob", "Dupont", "bob@company.com")
        .with_job("Engineering", "Lead Developer", 90000)
        .with_equipment(laptop=True, parking=True)
        .build()
    )
    print(senior)
    print(f"  Laptop: {senior.has_laptop}, Parking: {senior.has_parking}")

    # ── Validation test ──
    print("\n=== Validation test ===")
    try:
        bad = EmployeeBuilder().with_name("", "").with_email("no-at-sign").build()
    except ValueError as e:
        print(f"Error caught: {e}")
