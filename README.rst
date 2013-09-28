####################
Districts API Client
####################

Interface to the `NY Times Districts API <http://developer.nytimes.com/docs/districts_api>`_.

Install
=======

This module's only necessary external dependency is the requests module.

::
   
   pip install requests
   pip install -e git+<URL>
   
An additional list of dependencies for building the documentation and running tests can be found in REQUIREMENTS_FULL.TXT:

::

   pip install -r REQUIREMENTS_FULL.TXT

Configure
=========

::

`Request an API key <http://developer.nytimes.com/apps/register/>`_ from the New York Times

Use
===

::

.. code-block:: Python

   >>> from district_api.api import DistrictsApi
   
   >>> # Instantiate client
   >>> client = DistrictsApi('my_api_key_here')
   
   >>> # Get the districts for a location in NYC
   >>> lat_lng = (40.606031, -74.082686,)
   >>> districts = client.get_districts(lat_lng)
   
   >>> # Use the returned data
   >>> districts['State Senate'].district
   "24"
   >>> districts['State Senate'].kml_url
   "http://graphics8.nytimes.com/packages/xml/represent/1382.xml"
   
   
.. note:: 
   Refer to `NY Times Documentation <http://developer.nytimes.com/docs/districts_api>`_ for details on specific data that may be returned

Test
====

::

   py.test

More Information
================

Refer to docs directory for further info.