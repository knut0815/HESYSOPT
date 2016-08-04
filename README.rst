HESYSOPT stands for "Heating System Optimization Tool" and is a free, open source
tool to simulate district heating systems. It is developed in Python and
based on the open energy modelling framework (https://github.com/oemof/oemof),
specifically the solph-package. The mathematical approach is mixed-integer-linear
programming. 

Documentation
=============

To come....


Installing HESYSOPT
=====================

At the moment you need to clone the repository:

.. code:: bash

  git clone git@github.com:znes/HESYSOPT.git

Running HESYSOPT
=====================

Once you downloaded the repository, change to the directory with the source code. 
You can now run the application via terminal command. 

To get information about app options, run the following command in your
terminal:

.. code:: bash

	python3 app.py --help


Provide the data in a csv-file. To see what structure is needed, checkout the
example directory inside the repository. 
