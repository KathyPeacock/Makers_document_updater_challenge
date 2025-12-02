import os
from faker import Faker


# Set up Faker with UK locale
fake = Faker('en_UK')

def create_document(folder_path, surname):

    """
    Creates a document file with UK address inside it
    
    folder_path: where to create the file (e.g., "originals" folder)
    surname: the filename to use
    """
    # Seed Faker based on surname so same surname = same first name
    Faker.seed(hash(surname))

    # Generate a first name (will be consistent for same surname)
    # ... and join to make full name
    first_name = fake.first_name()
    full_name = f"{first_name} {surname}"

    # Reset seed with folder name so addresses differ between originals/updates
    Faker.seed(hash(surname + folder_path))

    # Generate UK address with consistent single-line street address
    building_number = fake.building_number()
    street_name = fake.street_name()
    street = f"{building_number} {street_name}"
    city = fake.city()
    postcode = fake.postcode()
    
    # Combine into consistent 4 line format: Name, Street, City, Postcode
    address_content = f"{full_name}\n{street}\n{city}\n{postcode}"

    # Create the full file path
    file_path = os.path.join(folder_path, surname)

    # Write the name and address to the file
    with open(file_path, 'w') as file:
        file.write(address_content)
    
    print(f"Created: {file_path}")

    # Quick test of create_document method
# os.makedirs("test_folder", exist_ok=True)
# create_document("test_folder", "TestSurname")

def create_test_scenario(scenario_name):
    
    """
    Creates a complete test scenario with:
    - originals folder with some documents
    - updates folder with some documents  
    - allowlist or droplist file
    """

    # Create the base directory for this scenario
    base_dir = f"test_{scenario_name}"

    # Create the folder structure
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)

    print(f"\n=== Creating test scenario: {scenario_name} ===")

    # Generate some random UK surnames to use
    surname1 = fake.last_name()
    surname2 = fake.last_name()
    surname3 = fake.last_name()

    print(f"Using surnames: {surname1}, {surname2}, {surname3}")

    # Create documents in originals folder
    originals_path = os.path.join(base_dir, "originals")
    create_document(originals_path, surname1)
    create_document(originals_path, surname2)
    
    # Create documents in updates folder
    updates_path = os.path.join(base_dir, "updates")
    create_document(updates_path, surname2)  # Same as one in originals!
    create_document(updates_path, surname3)

    # Create an allowlist file
    allowlist_path = os.path.join(base_dir, "allowlist")
    with open(allowlist_path, 'w') as f:
        f.write(surname1)  # Allow surname1 from originals
    
    print(f"Created allowlist with: {surname1}")
    print(f"\n✓ Test scenario ready: {base_dir}")

    # Quick test of create_test_scenario function
# create_test_scenario("my_first_test")


def create_example_1():
    """
    Scenario 1: 'Droplist blocks originals'. File in originals + in droplist = NOT in finals
    """
    scenario_name = "example_1_droplist_blocks_originals"
    base_dir = f"test_{scenario_name}"
    
    # Create folder structure
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)
    
    print(f"\n=== Example 1: Droplist blocks originals ===")
    
    # Generate a surname
    surname = fake.last_name()
    print(f"Using surname: {surname}")
    
    # Create file in originals only
    originals_path = os.path.join(base_dir, "originals")
    create_document(originals_path, surname)
    
    # Create droplist that mentions this surname
    droplist_path = os.path.join(base_dir, "droplist")
    with open(droplist_path, 'w') as file:
        file.write(surname)
    
    print(f"Created droplist containing: {surname}")
    print(f"EXPECTED: {surname} should NOT appear in finals")
    print(f"Run with: python document_updater.py {base_dir}\n")


"""
Uncomment to run scenario 1 ...
"""
# create_example_1()


def create_example_2():
    """
    Scenario 2: 'Updates supersedes allowlist'. 
    File in originals (in allowlist) + same file in updates = updates version wins
    """
    scenario_name = "example_2_updates_wins"
    base_dir = f"test_{scenario_name}"
    
    # Create folder structure
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)
    
    print(f"\n=== Example 2: Updates supersedes allowlist ===")
    
    # Generate a surname
    surname = fake.last_name()
    print(f"Using surname: {surname}")
    
    # Create file in originals and updates
    originals_path = os.path.join(base_dir, "originals")
    updates_path = os.path.join(base_dir, "updates")
    
    create_document(originals_path, surname)
    create_document(updates_path, surname)  # Same surname, different address
    
    # Create allowlist that mentions this surname
    allowlist_path = os.path.join(base_dir, "allowlist")
    with open(allowlist_path, 'w') as file:
        file.write(surname)
    
    print(f"Created allowlist containing: {surname}")
    print(f"EXPECTED: {surname} from UPDATES folder in finals (not originals version)")
    print(f"Run with: python document_updater.py {base_dir}\n")


"""
Uncomment to run scenario 2 ...
"""
# create_example_2()


def create_example_3():
    """
    Scenario 3: 'Droplist irrelevant for updates-only files'.
    File NOT in originals, only in updates, droplist mentions it = updates version in finals
    """
    scenario_name = "example_3_droplist_irrelevant"
    base_dir = f"test_{scenario_name}"
    
    # Create folder structure
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)
    
    print(f"\n=== Example 3: Droplist irrelevant for updates-only files ===")
    
    # Generate a surname
    surname = fake.last_name()
    print(f"Using surname: {surname}")
    
    # Create file ONLY in updates (not in originals)
    updates_path = os.path.join(base_dir, "updates")
    create_document(updates_path, surname)
    
    # Create droplist that mentions this surname
    droplist_path = os.path.join(base_dir, "droplist")
    with open(droplist_path, 'w') as file:
        file.write(surname)
    
    print(f"Created droplist containing: {surname}")
    print(f"EXPECTED: {surname} from updates SHOULD appear in finals (droplist has no effect)")
    print(f"Run with: python document_updater.py {base_dir}\n")


"""
Uncomment to run scenario 3 ...
"""
# create_example_3()  


def create_example_4():
    """
    Example 4: 'Droplist doesn't mention file'.
    File in originals, droplist exists but doesn't mention this file = in finals
    """
    scenario_name = "example_4_droplist_nomatch"
    base_dir = f"test_{scenario_name}"
    
    # Create folder structure
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "originals"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "updates"), exist_ok=True)
    
    print(f"\n=== Example 4: Droplist doesn't mention file ===")
    
    # Generate TWO surnames
    surname1 = fake.last_name()
    surname2 = fake.last_name()
    print(f"Using surnames: {surname1} and {surname2}")
    
    # Create file in originals
    originals_path = os.path.join(base_dir, "originals")
    create_document(originals_path, surname1)
    
    # Create droplist that mentions DIFFERENT surname
    droplist_path = os.path.join(base_dir, "droplist")
    with open(droplist_path, 'w') as file:
        file.write(surname2)  # Different surname!
    
    print(f"Created droplist containing: {surname2} (NOT {surname1})")
    print(f"EXPECTED: {surname1} SHOULD appear in finals (not blocked by droplist)")
    print(f"Run with: python document_updater.py {base_dir}\n")


"""
Uncomment to run scenario 4 ...
"""
# create_example_4() 