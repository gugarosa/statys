"""Descriptive measures for one or more samples.

Each function returns a dictionary keyed by input order: ``arg0``, ``arg1``,
and so on. Values retain the underlying NumPy or SciPy result type, including
array-valued reductions. Keyword arguments are passed unchanged to each call.
Options such as ``out`` and ``overwrite_input`` retain their mutation and
aliasing behavior. The adapters themselves do not copy inputs or keyword
arguments; any copying inside NumPy or SciPy follows that function's options.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import ArrayLike
from scipy import stats


def _apply(
    function: Callable[..., Any], samples: tuple[ArrayLike, ...], **kwargs: Any
) -> dict[str, Any]:
    if not samples:
        raise ValueError("at least one sample is required")

    return {
        f"arg{index}": function(sample, **kwargs)
        for index, sample in enumerate(samples)
    }


def kurtosis(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate kurtosis for each sample.

    Parameters
    ----------
    *samples
        One or more array-like samples.
    **kwargs
        Passed to ``scipy.stats.kurtosis``. Defaults include ``axis=0``,
        ``fisher=True`` (excess kurtosis), and ``bias=True``.

    Returns
    -------
    dict
        Input-order keys ``arg0``, ``arg1``, etc., mapped to SciPy scalars
        or arrays. Constant samples have undefined (NaN) kurtosis.

    Raises
    ------
    ValueError
        If no samples are supplied.

    Examples
    --------
    >>> from statys import measures
    >>> round(float(measures.kurtosis([1, 2, 3, 4])["arg0"]), 2)
    -1.36
    """

    return _apply(stats.kurtosis, samples, **kwargs)


def max(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the maximum for each sample.

    Parameters
    ----------
    *samples
        One or more array-like samples.
    **kwargs
        Passed to ``numpy.max``, including ``axis``, ``out``, and
        ``keepdims``. By default, each sample is reduced over all axes.

    Returns
    -------
    dict
        Input-order keys ``arg0``, ``arg1``, etc., mapped to NumPy results.
        The result shape and dtype follow the input and keyword arguments.

    Raises
    ------
    ValueError
        If no samples are supplied, or NumPy cannot perform the reduction.

    Examples
    --------
    >>> from statys import measures
    >>> int(measures.max([1, 4, 2])["arg0"])
    4
    """

    return _apply(np.max, samples, **kwargs)


def mean(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the arithmetic mean for each sample.

    Parameters
    ----------
    *samples
        One or more array-like samples.
    **kwargs
        Passed to ``numpy.mean``, including ``axis``, ``dtype``, ``out``,
        and ``keepdims``. By default, each sample is reduced over all axes.

    Returns
    -------
    dict
        Input-order keys ``arg0``, ``arg1``, etc., mapped to NumPy scalars
        or arrays. No conversion to Python scalars is performed.

    Raises
    ------
    ValueError
        If no samples are supplied.

    Examples
    --------
    >>> from statys import measures
    >>> measures.mean([[1, 3], [5, 7]], axis=0)["arg0"].tolist()
    [3.0, 5.0]
    """

    return _apply(np.mean, samples, **kwargs)


def median(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the median for each sample.

    Parameters
    ----------
    *samples
        One or more array-like samples.
    **kwargs
        Passed to ``numpy.median``. The default ``axis=None`` reduces each
        sample over all axes. ``overwrite_input=True`` permits mutation.

    Returns
    -------
    dict
        Input-order keys ``arg0``, ``arg1``, etc., mapped to NumPy scalars
        or arrays.

    Raises
    ------
    ValueError
        If no samples are supplied.

    Examples
    --------
    >>> from statys import measures
    >>> float(measures.median([1, 2, 7, 8])["arg0"])
    4.5
    """

    return _apply(np.median, samples, **kwargs)


def min(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the minimum for each sample.

    Parameters
    ----------
    *samples
        One or more array-like samples.
    **kwargs
        Passed to ``numpy.min``, including ``axis``, ``out``, and
        ``keepdims``. By default, each sample is reduced over all axes.

    Returns
    -------
    dict
        Input-order keys ``arg0``, ``arg1``, etc., mapped to NumPy results.
        The result shape and dtype follow the input and keyword arguments.

    Raises
    ------
    ValueError
        If no samples are supplied, or NumPy cannot perform the reduction.

    Examples
    --------
    >>> from statys import measures
    >>> int(measures.min([1, 4, 2])["arg0"])
    1
    """

    return _apply(np.min, samples, **kwargs)


def rank(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Assign increasing ranks to the values in each sample.

    Parameters
    ----------
    *samples
        One or more array-like samples.
    **kwargs
        Passed to ``scipy.stats.rankdata``. The default ``axis=None``
        flattens each sample; ``method="average"`` gives ties their
        average rank. Use ``axis=1`` to rank rows independently.

    Returns
    -------
    dict
        Input-order keys ``arg0``, ``arg1``, etc., mapped to rank arrays.
        The smallest value has rank one.

    Raises
    ------
    ValueError
        If no samples are supplied.

    Examples
    --------
    >>> from statys import measures
    >>> measures.rank([3, 1, 1])["arg0"].tolist()
    [3.0, 1.5, 1.5]
    """

    return _apply(stats.rankdata, samples, **kwargs)


def skewness(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the Fisher-Pearson skewness coefficient for each sample.

    Parameters
    ----------
    *samples
        One or more array-like samples.
    **kwargs
        Passed to ``scipy.stats.skew``. Defaults include ``axis=0`` and
        ``bias=True``; ``bias=False`` requests bias correction.

    Returns
    -------
    dict
        Input-order keys ``arg0``, ``arg1``, etc., mapped to SciPy scalars
        or arrays. Constant samples have undefined (NaN) skewness.

    Raises
    ------
    ValueError
        If no samples are supplied.

    Examples
    --------
    >>> from statys import measures
    >>> float(measures.skewness([1, 2, 3])["arg0"])
    0.0
    """

    return _apply(stats.skew, samples, **kwargs)


def std(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate standard deviation for each sample.

    Parameters
    ----------
    *samples
        One or more array-like samples.
    **kwargs
        Passed to ``numpy.std``. Defaults include ``axis=None`` and
        ``ddof=0`` (population standard deviation); use ``ddof=1`` for
        the square root of the unbiased sample variance.

    Returns
    -------
    dict
        Input-order keys ``arg0``, ``arg1``, etc., mapped to NumPy scalars
        or arrays.

    Raises
    ------
    ValueError
        If no samples are supplied.

    Examples
    --------
    >>> from statys import measures
    >>> float(measures.std([1, 2, 3], ddof=1)["arg0"])
    1.0
    """

    return _apply(np.std, samples, **kwargs)


def var(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate variance for each sample.

    Parameters
    ----------
    *samples
        One or more array-like samples.
    **kwargs
        Passed to ``numpy.var``. Defaults include ``axis=None`` and
        ``ddof=0`` (population variance); use ``ddof=1`` for the unbiased
        sample variance.

    Returns
    -------
    dict
        Input-order keys ``arg0``, ``arg1``, etc., mapped to NumPy scalars
        or arrays.

    Raises
    ------
    ValueError
        If no samples are supplied.

    Examples
    --------
    >>> from statys import measures
    >>> float(measures.var([1, 2, 3], ddof=1)["arg0"])
    1.0
    """

    return _apply(np.var, samples, **kwargs)
