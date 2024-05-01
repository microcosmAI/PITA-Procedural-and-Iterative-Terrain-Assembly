Logger Module
============

.. module:: pitapy.utils
   :synopsis: Manages log initialization and configuration within the PITA Algorithm framework.

The `Logger` class is tasked with the initialization of a logging system for the PITA Algorithm, facilitating the systematic capture of informational messages, warnings, and errors during runtime. It configures a log handler to output log messages to a file, aiding in the debugging process and monitoring the algorithm's execution.

Usage
-----

The `Logger` class provides a static method `initialize_logger` that sets up the logging environment. This method configures a file-based log handler, which stores log messages in a designated directory, ensuring that log data persists beyond the application's runtime.


.. automodule:: pitapy.utils.logger
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
