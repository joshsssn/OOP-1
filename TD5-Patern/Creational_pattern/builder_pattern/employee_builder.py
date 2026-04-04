class Employee:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.email = None
        self.department = None
        self.position = None
        self.salary = 0.0
        self.start_date = None
        self.manager_id = None
        self.phone = None
        self.address = None
        self.emergency_contact = None
        self.has_parking = False
        self.has_laptop = False
        self.has_vpn_access = False
        self.has_admin_rights = False
        self.office_location = None
        self.contract_type = "permanent"

class EmployeeBuilder:
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

    def with_contact(self, phone: str, address: str, emergency: str) -> "EmployeeBuilder":
        self._employee.phone = phone
        self._employee.address = address
        self._employee.emergency_contact = emergency
        return self

    def with_equipment(self, laptop: bool, parking: bool) -> "EmployeeBuilder":
        self._employee.has_laptop = laptop
        self._employee.has_parking = parking
        return self

    def with_access(self, vpn: bool, admin: bool) -> "EmployeeBuilder":
        self._employee.has_vpn_access = vpn
        self._employee.has_admin_rights = admin
        return self

    def with_office(self, location: str, contract: str) -> "EmployeeBuilder":
        self._employee.office_location = location
        self._employee.contract_type = contract
        return self

    def with_manager(self, manager_id: int) -> "EmployeeBuilder":
        self._employee.manager_id = manager_id
        return self

    def build(self) -> Employee:
        return self._employee

class DeveloperBuilder(EmployeeBuilder):
    def __init__(self, first: str, last: str, email: str):
        super().__init__()
        self.with_name(first, last)
        self.with_email(email)
        self.with_job("Engineering", "Developer", 60000.0)


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
