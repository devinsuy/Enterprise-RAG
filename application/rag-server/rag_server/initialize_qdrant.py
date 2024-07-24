"""
The sole purpose of this script is to be run before main.py
to restore the db from snapshot. Ensure the docker container
is running first before running this script.
"""

from data_utils import initialize_vector_db

initialize_vector_db(needs_init=True)
