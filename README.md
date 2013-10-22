AgoraD-LoadingDock
==================
A django project that will sit on top of a datastore. The datastore will likely be that of another large player in the mobile data space in the future. Initially it will be used internally with our own datastore. There is no need to envision this partnership at the conception of the datastore, and as such integration will be an easy process.

Setup
-----
The user will configure their datastore by appending to the DATABASES in settings.py. They will then initiate a setup script which auto discovers the schema and certain characteristics about the DB. When they want to transfer to another person, loading dock will ship the schema over to the buyer's db and create a new db instance with that schema (using django's serializers). It will then break the data up into blocks and transfer it over using json, reconstructing it into the new database

Current State
-------------
The repository at this point is a mostly empty, but complete django project. It does contain a short README and clearly labeled structure. Technical content included is a models file for the datastores and a python script for adding datastores to the project.
