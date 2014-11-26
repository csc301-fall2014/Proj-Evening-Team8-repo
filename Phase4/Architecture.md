# Architecture

Our product is built on a web framework called Django, which provides a high-level implementation of the Model-View-Controller design pattern.  As such, the implementation of our product consists of three major components:

The model (models.py), which defines long-term objects to be saved to a database and manipulated.  These models, while defined in Python, correspond to a SQLite3 database, though they could easily be attached to any other relational database.

The views (templates directory), which are user interface specifications which define how the user interacts with our website, providing input options and useful visual output.  Views were written using HTML5, CSS, Javascript and AJAX technologies, with some embedded Python to help with the generation of HTML.

The controllers (views.py), which define the core logic of the website;  it processes requests from the user by accessing/manipulating the database through models and rendering views to be returned to the user.  These were written entirely in Python using built-in Django libraries.

Apart from these, there is a built-in development web server for actually handling the HTTP requests that are received.

