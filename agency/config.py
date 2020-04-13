import os

SECRET_KEY = 'OMZ8%/Gve(_SfKG^+|,|np+V#|zSqP9.0xPEFuzb(PQ9U!Enu2:)k]83c-cBEx'
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Turn off track modifications warning
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Connect to the database
# DONE IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://postgres@localhost:5432/agency'
