import random
otp_store = {}

def generate_otp(phone):
    otp = str(random.randint(1000, 9999))
    otp_store[phone] = otp
    print("OTP:", otp)
    return otp

def verify_otp(phone, otp):
    return otp_store.get(phone) == otp