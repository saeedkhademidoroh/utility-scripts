# Import standard libraries
import os
from datetime import datetime

# Function to generate an iCloud-compatible VCF from a filtered text file
def generate_icloud_vcf(txt_path):
    """
    Convert a filtered text file into an iCloud-compatible .vcf file.

    Assumes names begin with letters and phone numbers do not.
    Each contact is separated by name and one or more phone lines.

    Args:
        txt_path (str): Path to the filtered extract.txt file.

    Returns:
        str: Path of the generated .vcf file.
    """
    vcf_path = os.path.join(os.path.dirname(txt_path), "contacts.vcf")

    print("📂 Reading extracted contacts...")
    with open(txt_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    contacts = []
    current_contact = {"first_name": "X", "last_name": "", "phones": []}

    for line in lines:
        if line[0].isalpha():
            if current_contact["last_name"] and current_contact["phones"]:
                contacts.append(current_contact)
            current_contact = {"first_name": "X", "last_name": line, "phones": []}
        else:
            current_contact["phones"].append(line)

    if current_contact["last_name"] and current_contact["phones"]:
        contacts.append(current_contact)

    print(f"📄 {len(contacts)} contacts extracted. Generating iCloud-compatible VCF...")

    with open(vcf_path, "w", encoding="utf-8") as vcf_file:
        for idx, contact in enumerate(contacts, start=1):
            last_name = contact["last_name"]
            rev_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            vcf_file.write("BEGIN:VCARD\n")
            vcf_file.write("VERSION:3.0\n")
            vcf_file.write("PRODID:-//Apple Inc.//iOS 18.3.1//EN\n")
            vcf_file.write(f"N:;{last_name};;;\n")
            vcf_file.write(f"FN:{contact['first_name']} {contact['last_name']}\n")
            vcf_file.write(f"TEL;TYPE=CELL;TYPE=VOICE;TYPE=pref:{contact['phones'][0]}\n")

            for i, phone in enumerate(contact["phones"][1:], start=1):
                vcf_file.write(f"item{i}.TEL;type=pref:{phone}\n")

            vcf_file.write(f"REV:{rev_time}\n")
            vcf_file.write("END:VCARD\n\n")

    print(f"✅ iCloud-compatible VCF file created: {vcf_path}")
    return vcf_path

# Print confirmation message
print("\n✅ generate.py successfully executed")
