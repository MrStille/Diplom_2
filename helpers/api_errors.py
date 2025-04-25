import os
import sys

sys.path.append(os.getcwd())

class ApiErrors:
    USER_EXISTS_ERROR = "User already exists"
    USER_NO_REQUIRED_FIELDS_ERROR = "Email, password and name are required fields"