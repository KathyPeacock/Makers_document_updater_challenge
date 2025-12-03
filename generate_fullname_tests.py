from faker import Faker
import os

fake = Faker('en_UK')

def create_document_fullname(folder_path, full_name):
    """
    Create a document where the filename is the full name (with space)
    """
    first_name = full_name.split()[0]
    surname = full_name.split()[1] if len(full_name.split()) > 1 else full_name
    
    # Re-seed for different addresses per folder
    Faker.seed(hash(full_name + folder_path))
    
    street = fake.building_number() + " " + fake.street_name()
    city = fake.city()
    postcode = fake.postcode()
    
    address_content = f"{full_name}\n{street}\n{city}\n{postcode}"
    
    file_path = os.path.join(folder_path, full_name)
    
    with open(file_path, 'w') as file:
        file.write(address_content)
    
    print(f"Created: {file_path}")


def test_fullname_allowlist():
    """
    TEST: Full name in filename + allowlist
    Bug check: Does it handle spaces in filenames/allowlist correctly?
    """
    scenario_name = "fullname_allowlist"
    base_dir = f"test_{scenario_name}"
    
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)
    
    print(f"\n=== TEST: Full name with space in allowlist ===")
    
    full_name = "John Smith"
    
    originals_path = os.path.join(base_dir, "originals")
    create_document_fullname(originals_path, full_name)
    
    # Create allowlist with full name
    allowlist_path = os.path.join(base_dir, "allowlist")
    with open(allowlist_path, 'w') as file:
        file.write(full_name)
    
    print(f"Allowlist contains: '{full_name}'")
    print(f"EXPECTED: File 'John Smith' in finals")
    print(f"Run: python document_updater.py {base_dir}\n")


def test_fullname_updates():
    """
    TEST: Full name in updates folder
    Bug check: Does updates handle spaces correctly?
    """
    scenario_name = "fullname_updates"
    base_dir = f"test_{scenario_name}"
    
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)
    
    print(f"\n=== TEST: Full name in updates ===")
    
    full_name = "Sarah Jones"
    
    updates_path = os.path.join(base_dir, "updates")
    create_document_fullname(updates_path, full_name)
    
    # Create droplist (should be irrelevant for updates)
    droplist_path = os.path.join(base_dir, "droplist")
    with open(droplist_path, 'w') as file:
        file.write(full_name)
    
    print(f"Droplist contains: '{full_name}'")
    print(f"EXPECTED: File 'Sarah Jones' in finals (droplist irrelevant)")
    print(f"Run: python document_updater.py {base_dir}\n")


def test_fullname_both_folders():
    """
    TEST: Same full name in both originals and updates
    Bug check: Does updates supersede when full names used?
    """
    scenario_name = "fullname_both"
    base_dir = f"test_{scenario_name}"
    
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)
    
    print(f"\n=== TEST: Full name in BOTH folders ===")
    
    full_name = "Emma Brown"
    
    originals_path = os.path.join(base_dir, "originals")
    updates_path = os.path.join(base_dir, "updates")
    
    create_document_fullname(originals_path, full_name)
    create_document_fullname(updates_path, full_name)
    
    # Create allowlist
    allowlist_path = os.path.join(base_dir, "allowlist")
    with open(allowlist_path, 'w') as file:
        file.write(full_name)
    
    print(f"Allowlist contains: '{full_name}'")
    print(f"EXPECTED: Updates version of 'Emma Brown' in finals")
    print(f"Run: python document_updater.py {base_dir}\n")


def test_mixed_surname_and_fullname():
    """
    TEST: Mix of surname-only and full names
    Bug check: Can system handle both formats?
    """
    scenario_name = "mixed_formats"
    base_dir = f"test_{scenario_name}"
    
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)
    
    print(f"\n=== TEST: Mixed surname-only and full names ===")
    
    originals_path = os.path.join(base_dir, "originals")
    updates_path = os.path.join(base_dir, "updates")
    
    # Surname only (old format)
    surname_only = fake.last_name()
    Faker.seed(hash(surname_only))
    first = fake.first_name()
    street = fake.building_number() + " " + fake.street_name()
    city = fake.city()
    postcode = fake.postcode()
    
    with open(os.path.join(originals_path, surname_only), 'w') as file:
        file.write(f"{first} {surname_only}\n{street}\n{city}\n{postcode}")
    
    print(f"Created originals/{surname_only} (surname only format)")
    
    # Full name format
    full_name = "James Wilson"
    create_document_fullname(updates_path, full_name)
    
    # Allowlist with both formats
    allowlist_path = os.path.join(base_dir, "allowlist")
    with open(allowlist_path, 'w') as file:
        file.write(f"{surname_only}\n{full_name}")
    
    print(f"Allowlist contains: '{surname_only}' and '{full_name}'")
    print(f"EXPECTED: Both files in finals")
    print(f"Run: python document_updater.py {base_dir}\n")


def test_surname_in_allowlist_but_fullname_file():
    """
    TEST: Mismatch between allowlist format and filename format
    Bug check: If file is "John Smith" but allowlist says "Smith", does it match?
    """
    scenario_name = "mismatch_format"
    base_dir = f"test_{scenario_name}"
    
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)
    
    print(f"\n=== TEST: Format mismatch - filename vs allowlist ===")
    
    full_name = "Oliver Taylor"
    surname = "Taylor"
    
    originals_path = os.path.join(base_dir, "originals")
    create_document_fullname(originals_path, full_name)
    
    # Allowlist only has surname
    allowlist_path = os.path.join(base_dir, "allowlist")
    with open(allowlist_path, 'w') as file:
        file.write(surname)
    
    print(f"Filename: '{full_name}'")
    print(f"Allowlist contains: '{surname}'")
    print(f"EXPECTED: ???")
    print(f"Run: python document_updater.py {base_dir}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("AUTOMATED TESTS - FULL NAME FILENAMES")
    print("=" * 60)
    
    test_fullname_allowlist()
    test_fullname_updates()
    test_fullname_both_folders()
    test_mixed_surname_and_fullname()
    test_surname_in_allowlist_but_fullname_file()
    
    print("=" * 60)
    print("ALL TESTS GENERATED!")
    print("=" * 60)