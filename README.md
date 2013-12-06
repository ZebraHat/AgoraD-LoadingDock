AgoraD-LoadingDock
==================

The AgoraD Loading Dock is a small django project that sits on top of a datastore to facilitate datastore-agnostic data sharing. The accompanying software (AgoraD-MarketplaceUI), will communicate with this django project and facilitate transfers of data whenever and wherever you elect to transfer your data to.

This project has two main components:
* Loading Dock
* Highway

The Loading Dock
----------------

The Loading Dock is a magic bit of code that will autodiscover your database's schema and other introspection properties automatically. Please see the setup and wiki for instructions on how to use it.

The Highway
-----------

The Highway is a fancy term for an API, and it will facilitate the secure transfer of your data in manageable blocks to the destination's datastore. There should never be a need for a user to communicate with this directly.

--------------

Again, there is no need to call any of the functionality of the Loading Dock after the initial setup, as all record keeping and transfers are initiated by the Marketplace UI(s) that you are registered with.

Setup
-----
The user will configure their datastore by appending to the DATABASES in settings.py. They will then initiate a setup script which auto discovers the schema and certain characteristics about the DB. When they want to transfer to another person, loading dock will ship the schema over to the buyer's db and create a new db instance with that schema (using django's serializers). It will then break the data up into blocks and transfer it over using json, reconstructing it into the new database

Current State
-------------
The Loading Dock's packaging and introspection tools are mostly complete, but the Highway has not yet been fully tested or connected to the Marketplace's UI. Feature requests, a better wiki, and support tickets are coming soon.
