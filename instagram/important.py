def mask_email(email):
    # Split the email address into username and domain parts
    username, domain = email.split('@')

    # If the username is less than 3 characters, return the original email
    if len(username) < 3:
        return email

    # Replace characters between the first and last characters with '*'
    masked_username = username[0:3] + '*' * (len(username) - 2) + username[-1]

    # Concatenate the masked username with the domain and return the result
    return f"{masked_username}@{domain}"

