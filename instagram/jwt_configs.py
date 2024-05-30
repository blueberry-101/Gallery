
from datetime import datetime,timezone

def jwt_is_expired(payload):
    print("here")
    expiry_time = payload.get("exp")
    print(expiry_time)
    expiry_time = datetime.fromtimestamp(expiry_time,timezone.utc)
    current_time = datetime.now(timezone.utc)
    try:
        if expiry_time < current_time:
            print("The given datetime has already passed.")
            return True
        else:
            print("The given datetime is still in the future.")
            return False
    except Exception as e:
        print("exception in expiration",e)
