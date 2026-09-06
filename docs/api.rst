API reference
=============

Repeated comparisons
--------------------

These functions are available directly from ``statys``. Rows of a score
matrix are experimental blocks; columns identify treatments consistently
across blocks.

.. autosummary::

   statys.friedman
   statys.nemenyi
   statys.plot_critical_difference

Measures and pairwise tests
---------------------------

``statys.measures`` applies a NumPy or SciPy measure independently to each
sample. Results retain the delegate's scalar or array type and keyword
behavior. The wrappers add no copying or missing-data policy of their own.

``statys.pairwise`` compares each unique pair of samples and returns
``(reject, p_value)`` tuples. The signed-rank test is for paired observations;
Mann-Whitney U and rank-sum tests are for independent samples.
``statys.significance`` plots those results without recomputing decisions.

Module reference
----------------

.. autosummary::
   :toctree: generated
   :recursive:

   statys
