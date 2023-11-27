"""Function to make the data in an array smoother.

By Markus Reinert (IOW, 2023, https://orcid.org/0000-0002-3761-8029)
based on templates by Marvin Lorenz and Samira Zander (IOW, 2021).
"""

import numpy as np


def smooth_2D_array(data, pm_i, pm_j, *, overwrite=False):
    """Smooth `data` with a 2D running average of size (2*pm_i+1) × (2*pm_j+1).

    The dimensions of `data` are considered to be `(i, j)`.

    Points in `data` that are `NaN` before the smoothing will stay
    `NaN` and are ignored (masked) for the averaging.

    If `overwrite` is `False` (default), a new array with the smoothed
    values and the same size as `data` is returned.  If `overwrite` is
    `True`, the values in data are replaced with the smoothed values
    and nothing is returned.  Note that overwriting can be about
    10-times slower if `data` is an xarray DataArray.

    If `pm_i` and `pm_j` are both zero, `data` is returned unchanged.

    Example:
    To smooth the data by averaging every 3×3-square, use `pm_i = 1`
    and `pm_j = 1`, i.e., taking the mean over plus and minus (pm) one
    cell in each direction.
    """
    ni, nj = data.shape
    data_smoothed = np.empty_like(data) if not overwrite else data
    # Make the array larger by putting NaNs around it,
    # so that the averaging works also near boundaries
    data_extended = np.full((ni + 2 * pm_i, nj + 2 * pm_j), np.nan)
    data_extended[pm_i : ni + pm_i, pm_j : nj + pm_j] = data
    # Create a masked array, because averaging over a masked array
    # is much faster than using np.nanmean
    data_masked = np.ma.masked_where(np.isnan(data_extended), data_extended)
    for i in range(ni):
        for j in range(nj):
            if data_masked.mask[i + pm_i, j + pm_j]:
                data_smoothed[i, j] = np.nan
            else:
                data_smoothed[i, j] = np.ma.mean(
                    data_masked[i : i + 2 * pm_i + 1, j : j + 2 * pm_j + 1]
                )
    return data_smoothed if not overwrite else None
