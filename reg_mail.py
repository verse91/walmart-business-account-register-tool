import requests
import random
import string
import time

BASE_URL = "https://api.mail.tm"

# Lấy danh sách domain hợp lệ
def getAvailableDomains():
    response = requests.get(f"{BASE_URL}/domains")
    if response.status_code == 200:
        domains = response.json()["hydra:member"]
        return [domain["domain"] for domain in domains]
    else:
        print(f"Failed to fetch domains: {response.status_code}, {response.text}")
        return []

# Đăng ký tài khoản email
def regEmail(email, password="Walmart@"):
    response = requests.post(f"{BASE_URL}/accounts", json={
        "address": email,
        "password": password
    })
    if response.status_code == 201:  # HTTP 201: Created
        print(f"Registered email: {email}")
        return True
    else:
        print(f"Failed to register email {email}: {response.status_code}, {response.text}")
        return False

# Tạo email theo định dạng CompanyName_XXX@domain.com
def genMail(companyName, domain):
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    emailName = companyName.replace(" ", "").replace(",", "").replace(".", "") + f"_{random_suffix}"
    return f"{emailName.lower()}@{domain}"

# Đọc dữ liệu từ file và tạo email
def processFile(input_file, output_file):
    availableDomains = getAvailableDomains()
    if not availableDomains:
        print("No available domains found. Exiting...")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Mở file ở chế độ append ("a") để ghi thêm
    with open(output_file, "a", encoding="utf-8") as out_file:
        for i in range(0, len(lines), 5):  # Mỗi 5 dòng chọn 1 công ty
            companyLine = lines[i].strip()  # Lấy dòng chứa tên công ty
            if companyLine:
                domain = random.choice(availableDomains)
                email = genMail(companyLine, domain)
                password = "Walmart@" # Pass mặc định
                # Đăng ký email
                if regEmail(email, password):
                    # Ghi vào file output
                    out_file.write(f"{email}:{password}\n")
                    time.sleep(3)  # Delay 3s

def main():
    input_file = "data.txt"
    output_file = "email.txt"

    # Xử lý file
    processFile(input_file, output_file)
    print(f"Email generation complete. Check {output_file} for details.")
