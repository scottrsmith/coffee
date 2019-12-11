
Coffee Shop Full Stack
----------------------

The coffee shop app is a new digitally enabled cafe for udacity students to order drinks, socialize, and study hard. The full stack drink menu application does the following:

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

Getting Started - Backend
-------------------------

Installing Dependencies
^^^^^^^^^^^^^^^^^^^^^^^

Python 3.7

.. code-block::


   This project uses python 3.7.

   To Install: `Python <https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python>`_

   PIP Dependencies
   ~~~~~~

Once you have your virtual environment setup and running, install dependencies by navigating to the root directory and running:

.. code-block:: bash

   pip install -r requirements.txt

This will install all of the required packages we selected within the ``requirements.txt`` file.

Key Dependencies
""""""""""""""""


* 
  `Flask <http://flask.pocoo.org/>`_  is a lightweight backend microservices framework. 

* 
  `SQLAlchemy <https://www.sqlalchemy.org/>`_ is the Python SQL toolkit and ORM. 

* 
  `Flask-CORS <https://flask-cors.readthedocs.io/en/latest/#>`_ is the extension used to handle cross-origin requests from the frontend server. 

Database Setup
--------------

The app is running with SQLite. No setup needs to be performed.

Running the server
------------------

From within the ``backend`` directory to run the server, execute:

.. code-block:: bash

   export FLASK_APP=flaskr
   export FLASK_ENV=development
   flask run

Documentation
-------------

Opening the API Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Documentation is generated with Sphinx.

HTML Documentation

.. code-block::


   From the root folder, open the index file in a browser

   .. code-block:: bash

      ./docs/build/html/index.html

   PDF Documentation
   ~~~~~~~~~~~~~~~~~

   The PDF version of the documentation is located in the root project directory. Named coffeeapi.pdf

   Generating documentation
   ^^^^^^^^^^^^^^^^^^^^^^^^

   Documentation is generated with Sphinx.

   Installing Sphinx and support tools
   ~~~~~~~~~~~~~~~~~

To install Sphinx, reference the documents at https://www.sphinx-doc.org/en/master/usage/installation.html

For example:

.. code-block:: bash

    pip install -U sphinx

Install dependencies by navigating to the ``root`` project directory and running:

.. code-block:: bash

   cd docs
   pip install m2r
   pip install recommonmark
   pip install rinohtype
   pip install -r requirements.txt

Generating the documentation

.. code-block::


   Generate the documentation with the following commands:

   .. code-block:: bash

      # From the root project directory
      # Convert readme to rst to be included in generated docs
      m2r README.md README.rst --overwrite
      cp -R README.rst ./docs/source
      cd ./docs
      make html
      # Make pdf
      make latexpdf
      cd ..
      cp -R ./docs/build/latex/coffeeaapi.pdf .

   API End Points
   --------------

   The following APIs are available. Detailed html documentation can be found in the 'docs' folder.

   Error Handling
   --------------

   Errors are returned as JSON objects in the following format:

   .. code-block:: bash

      {
          "success": False, 
          "error": 400,
          "message": "Bad Request"
      }

   The API will return three error types when requests fail:


   * 400: Bad Request
   * 404: Resource Not Found
   * 405: Method Not Allowed
   * 422: Not Processable 
   * 500: Internal Server Error

   Testing
   -------

   Testing is done with Postman

   To run postman. Run:

   .. code-block:: bash

      do somthing....... TODO:

   Full Stack coffee API Frontend
   ------------------------------

   Installing Dependencies
   ^^^^^^^^^^^^^^^^^^^^^^^

   Installing Node and NPM
   ~~~~~~~~~~~~~~~~~~~~~~~

   This app depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from `https://nodejs.com/en/download <https://nodejs.org/en/download/>`_.

   Installing Ionic Client
   ~~~~~~~~~~~~~~~~~~~~~~~

   The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI  is in the `Ionic Framework Docs <https://ionicframework.com/docs/installation/cli>`_.

   Installing project dependencies
   ~~~

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the ``frontend`` directory of this repository. After cloning, open your terminal and run:

.. code-block:: bash

   npm install

Required Tasks
--------------

Running Your Frontend in Dev Mode
---------------------------------

Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, cd into the ``frontend`` directory and run:

.. code-block:: bash

   ionic serve

..
   *tip*\ : Do not use **ionic serve**  in production. Instead, build Ionic into a build artifact for your desired platforms.
   `Checkout the Ionic docs to learn more <https://ionicframework.com/docs/cli/commands/build>`_
