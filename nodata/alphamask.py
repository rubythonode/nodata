import numpy as np
import skimage.measure as measure
import scipy.ndimage.measurements as sci_meas
from skimage.segmentation import slic
from scipy.ndimage.morphology import binary_fill_holes


def _diff_nodata(image, ndv):
    return np.sum([np.abs(im.astype(float) - n) for im, n in zip(image, ndv)], axis=0)


def _hacky_make_image(labeled_img, u_labels, measures, m_key, dtype=np.int16):
    out = np.zeros(labeled_img.shape, dtype=dtype).ravel()
    if m_key is None:
        measures = [{"key": m} for m in measures]
        m_key = "key"

    def value_grab(a, b):
        out[b] = measures[a[0] - 1][m_key]
        return None

    sci_meas.labeled_comprehension(labeled_img, labeled_img, u_labels, value_grab, float, 0, pass_positions=True)

    return out.reshape(labeled_img.shape)


def simple_mask(data, ndv):
    '''SIMPLE THRESHOLDING APPROACH'''
    depth, rows, cols = data.shape

    alpha = (np.invert(np.all(np.dstack(data) == ndv, axis=2)).astype(data.dtype) * np.iinfo(data.dtype).max)

    return alpha


def slic_mask(arr, nodata, n_clusters=50, threshold=5, debug=False):
    """
    Uses @dnomadb algorithm, roughly:
        - cluster image using SLIC (k-means)
        - pull out contiguous regions and find aggregate stats
        - select regions that are likely nodata
        - fill inclusions
    """
    assert arr.shape[0] == len(nodata)
    near_nodata = _diff_nodata(arr, nodata)
    clusters = slic(near_nodata, n_clusters)
    labeled = measure.label(clusters) + 1
    measures = measure.regionprops(labeled, intensity_image=near_nodata, cache=True)
    mean_intensity = _hacky_make_image(labeled, np.unique(labeled), measures, 'mean_intensity')
    mask = binary_fill_holes(np.invert(binary_fill_holes(mean_intensity >= threshold)))
    if debug:
        d = dict([(m.label, m.mean_intensity) for m in measures])
        return mask.astype('uint8'), labeled.astype('uint32'), mean_intensity.astype('uint32'), d
    else:
        return mask.astype('uint8')