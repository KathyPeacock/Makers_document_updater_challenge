from faker import Faker
fake = Faker('en_UK')

def generate_manual_test_data():
    """
    Generates random UK surnames and addresses for manual testing
    Saves to a text file
    """
    output = []
    
    output.append("MANUAL TEST DATA")
    output.append("=" * 60)
    
    output.append("\nRandom UK Surnames (for filenames):")
    surnames = []
    for x in range(5):
        surname = fake.last_name()
        surnames.append(surname)
        output.append(surname)
    
    output.append("\nSample UK Addresses (for document content):")
    for surname in surnames[:3]:  # Just first 3
        first_name = fake.first_name()
        street = fake.building_number() + " " + fake.street_name()
        city = fake.city()
        postcode = fake.postcode()
        
        output.append(f"\n{first_name} {surname}")
        output.append(street)
        output.append(city)
        output.append(postcode)
    
    output.append("\nEdge Case Surnames:")
    output.append("Smith")
    output.append("smith")
    output.append("O'Brien")
    output.append("Smith-Jones")
    
    output.append("\n" + "=" * 60)
    
    # Write to file
    full_output = "\n".join(output)
    with open("manual_test_data.txt", 'w') as file:
        file.write(full_output)
    
    print("✓ Manual test data saved to: manual_test_data.txt")

generate_manual_test_data()