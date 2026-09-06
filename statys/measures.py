# Copyright (c) 2020-2026 Gustavo de Rosa.
# Licensed under the Apache License, Version 2.0.

"""Descriptive measures for one or more samples.

Each function returns a dictionary keyed by input order: ``arg0``, ``arg1``,
and so on. Values retain the underlying NumPy or SciPy result type, including
array-valued reductions. Keyword arguments are passed unchanged to each call.
Options such as ``out`` and ``overwrite_input`` retain their mutation and
aliasing behavior. The adapters themselves do not copy inputs or keyword
arguments. Any copying inside NumPy or SciPy follows that function's options.

"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import ArrayLike
from scipy import stats


def _apply(function: Callable[..., Any], samples: tuple[ArrayLike, ...], **kwargs: Any) -> dict[str, Any]:
    if not samples:
        raise ValueError("`samples` must contain at least one sample.")

    return {f"arg{index}": function(sample, **kwargs) for index, sample in enumerate(samples)}


def kurtosis(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate kurtosis for each sample.

    Args:
        *samples: One or more array-like samples.
        **kwargs: Options forwarded to ``scipy.stats.kurtosis``.

    Returns:
        Dictionary of SciPy scalars or arrays keyed by input order (``arg0``, ``arg1``, ...).

    Raises:
        ValueError: No samples are supplied.

    Notes:
        SciPy uses ``axis=0``, ``fisher=True`` (excess kurtosis), and ``bias=True`` unless overridden.
        Constant samples have undefined (NaN) kurtosis.

    Examples:
        >>> from statys import measures
        >>> round(float(measures.kurtosis([1, 2, 3, 4])["arg0"]), 2)
        -1.36

    """

    return _apply(stats.kurtosis, samples, **kwargs)


def max(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the maximum for each sample.

    Args:
        *samples: One or more array-like samples.
        **kwargs: Options forwarded to ``numpy.max``.

    Returns:
        Dictionary of NumPy results keyed by input order (``arg0``, ``arg1``, ...).

    Raises:
        ValueError: No samples are supplied or NumPy cannot perform the reduction.

    Notes:
        NumPy reduces each sample over all axes unless ``axis`` is supplied.
        ``out`` and ``keepdims`` retain NumPy behavior, and result shapes and dtypes follow the inputs and options.

    Examples:
        >>> from statys import measures
        >>> int(measures.max([1, 4, 2])["arg0"])
        4

    """

    return _apply(np.max, samples, **kwargs)


def mean(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the arithmetic mean for each sample.

    Args:
        *samples: One or more array-like samples.
        **kwargs: Options forwarded to ``numpy.mean``.

    Returns:
        Dictionary of NumPy scalars or arrays keyed by input order (``arg0``, ``arg1``, ...).

    Raises:
        ValueError: No samples are supplied.

    Notes:
        NumPy reduces each sample over all axes unless ``axis`` is supplied.
        ``dtype``, ``out``, and ``keepdims`` are forwarded unchanged. Statys does not convert results to Python scalars.

    Examples:
        >>> from statys import measures
        >>> measures.mean([[1, 3], [5, 7]], axis=0)["arg0"].tolist()
        [3.0, 5.0]

    """

    return _apply(np.mean, samples, **kwargs)


def median(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the median for each sample.

    Args:
        *samples: One or more array-like samples.
        **kwargs: Options forwarded to ``numpy.median``.

    Returns:
        Dictionary of NumPy scalars or arrays keyed by input order (``arg0``, ``arg1``, ...).

    Raises:
        ValueError: No samples are supplied.

    Notes:
        The default ``axis=None`` reduces each sample over all axes. ``overwrite_input=True`` permits input mutation.

    Examples:
        >>> from statys import measures
        >>> float(measures.median([1, 2, 7, 8])["arg0"])
        4.5

    """

    return _apply(np.median, samples, **kwargs)


def min(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the minimum for each sample.

    Args:
        *samples: One or more array-like samples.
        **kwargs: Options forwarded to ``numpy.min``.

    Returns:
        Dictionary of NumPy results keyed by input order (``arg0``, ``arg1``, ...).

    Raises:
        ValueError: No samples are supplied or NumPy cannot perform the reduction.

    Notes:
        NumPy reduces each sample over all axes unless ``axis`` is supplied.
        ``out`` and ``keepdims`` retain NumPy behavior, and result shapes and dtypes follow the inputs and options.

    Examples:
        >>> from statys import measures
        >>> int(measures.min([1, 4, 2])["arg0"])
        1

    """

    return _apply(np.min, samples, **kwargs)


def rank(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Assign increasing ranks to the values in each sample.

    Args:
        *samples: One or more array-like samples.
        **kwargs: Options forwarded to ``scipy.stats.rankdata``.

    Returns:
        Dictionary of rank arrays keyed by input order (``arg0``, ``arg1``, ...).

    Raises:
        ValueError: No samples are supplied.

    Notes:
        The default ``axis=None`` flattens each sample, and ``method="average"`` gives ties their average rank.
        The smallest value has rank one. Use ``axis=1`` to rank rows independently.

    Examples:
        >>> from statys import measures
        >>> measures.rank([3, 1, 1])["arg0"].tolist()
        [3.0, 1.5, 1.5]

    """

    return _apply(stats.rankdata, samples, **kwargs)


def skewness(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate the Fisher-Pearson skewness coefficient for each sample.

    Args:
        *samples: One or more array-like samples.
        **kwargs: Options forwarded to ``scipy.stats.skew``.

    Returns:
        Dictionary of SciPy scalars or arrays keyed by input order (``arg0``, ``arg1``, ...).

    Raises:
        ValueError: No samples are supplied.

    Notes:
        SciPy uses ``axis=0`` and ``bias=True`` unless overridden. ``bias=False`` requests bias correction.
        Constant samples have undefined (NaN) skewness.

    Examples:
        >>> from statys import measures
        >>> float(measures.skewness([1, 2, 3])["arg0"])
        0.0

    """

    return _apply(stats.skew, samples, **kwargs)


def std(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate standard deviation for each sample.

    Args:
        *samples: One or more array-like samples.
        **kwargs: Options forwarded to ``numpy.std``.

    Returns:
        Dictionary of NumPy scalars or arrays keyed by input order (``arg0``, ``arg1``, ...).

    Raises:
        ValueError: No samples are supplied.

    Notes:
        NumPy uses ``axis=None`` and ``ddof=0`` for population standard deviation unless overridden.
        Use ``ddof=1`` for the square root of the unbiased sample variance.

    Examples:
        >>> from statys import measures
        >>> float(measures.std([1, 2, 3], ddof=1)["arg0"])
        1.0

    """

    return _apply(np.std, samples, **kwargs)


def var(*samples: ArrayLike, **kwargs: Any) -> dict[str, Any]:
    """Calculate variance for each sample.

    Args:
        *samples: One or more array-like samples.
        **kwargs: Options forwarded to ``numpy.var``.

    Returns:
        Dictionary of NumPy scalars or arrays keyed by input order (``arg0``, ``arg1``, ...).

    Raises:
        ValueError: No samples are supplied.

    Notes:
        NumPy uses ``axis=None`` and ``ddof=0`` for population variance unless overridden.
        Use ``ddof=1`` for the unbiased sample variance.

    Examples:
        >>> from statys import measures
        >>> float(measures.var([1, 2, 3], ddof=1)["arg0"])
        1.0

    """

    return _apply(np.var, samples, **kwargs)
