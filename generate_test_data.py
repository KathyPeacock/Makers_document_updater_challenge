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

    # Generate a UK name and address
    first_name = fake.first_name()
    full_name = f"{first_name} {surname}"
    street = fake.street_address()
    city = fake.city()
    postcode = fake.postcode()
    
    # Combine into address format
    address_content = f"{full_name}\n{street}\n{city}\n{postcode}"

    # Create the file path
    file_path = os.path.join(folder_path, surname)

    # Write the address to the file
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
create_test_scenario("my_first_test")