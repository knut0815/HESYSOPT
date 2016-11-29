HESYSOPT stands for "(He)ating (Sys)tem (Op)timization (T)ool" and is a free, open source
tool to simulate district heating systems. It is developed in Python and
based on the the `Open Energy Modelling Framework (oemof) <https://github.com/oemof/oemof>`_.,
The mathematical approach is mixed-integer-linear programming.

Currently, it is developed and maintained at the Center for Sustainable Energy Systems (Zentrum für nachhaltige Energysysteme (ZNES)) in Flensburg.For questions on the data, you can use our `contact details <#contact>`_ below.

This documentation is meant to explain the basic functionality and structured as follows:

.. contents::
    :depth: 1
    :local:
    :backlinks: top
.. sectnum::


Application Examples
====================

to come ...


Installtion
=====================

HESYSOPT is build on `oemof <https://github.com/oemof/oemof>`_ and works with the current stable version (v.0.1).

To get the repository clone it from github: 

.. code:: bash

  git clone https://github.com/znes/HESYSOPT.git

To install oemof, you can install the dependencies with pip:

.. code:: bash 
	
	pip install -r -U requirements.txt

If this does not work, please follow the installation guidelines in the `documentation <https://github.com/oemof/oemof#documentation>`_.

Once you installed successfully, you should be ready to start as all dependencies that are required for HESYSOPT are coming along with oemof (pandas, pyomo, etc.).  You can run your app from the 'hesysopt' directory. If you do not want to use a virtualenvironment, you might want to add the HESYSOPT repository to your python path by adding the following line to you ~/.bashrc file.

.. code:: bash

	export PYTHONPATH="${PYTHONPATH}:/home/user/path/to/HESYSOPT"


Running HESYSOPT
=====================

Once you downloaded the repository, change to the directory with the source code.
You can now run the application with terminal command.

To get information about app options, run the following command in your
terminal:

.. code:: bash

	python3 app.py --help


Provide the data in a csv-file. To see what structure is needed, checkout the
example directory inside the repository and/or the documentation of oemof's 
`csv-reader <http://oemof.readthedocs.io/en/latest/oemof_solph.html#csv-reader>`_

You can also use the classes inside your code if you like scripting more than
running the tool from the command-line.  

Contribution
============

We adhere strictly to the `oemof developer rules <http://oemof.readthedocs.io/en/stable/developing_oemof.html>`_.
For any questions concerning the contribution, you can use our `contact details <#contact>`_ below.


Contact
=======

If you have any questions or want to contribute, feel free to contact us!

For questions, bugs, or possible improvements please create an `issue <https://github.com/znes/HESYSOPT/issues>`_.

For all other concerns, please write us an e-mail:

* Simon Hilpert (University of Flensburg): <simon.hilpert(at)uni-flensburg.de>

* Cord Kaldemeyer (Flensburg University of Applied Sciences): <cord.kaldemeyer(at)hs-flensburg.de>

Citing
=======
There exist a short-paper for the EnvironInfo conference 2016.

Please cite as:

S. Hilpert (2016) HESYSOPT - An optimization tool to support district heating flexibilisation.
Short paper presented at the Environmental Informatics – Current trends and future perspectives based on 30 years of history, Berlin, 14-16 September 2016




