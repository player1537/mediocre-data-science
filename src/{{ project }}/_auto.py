"""

"""

from __future__ import annotations


class AutoImport:
    @property
    def importlib(auto):
        import importlib
        return importlib

    def __getattr__(auto, name: str):
        return auto.importlib.import_module(name)
    
    @property
    def self(auto):
        import {{ project }}
        return {{ project }}

    @property
    def numpy(auto):
        import numpy
        import numpy.lib.recfunctions
        return numpy

    @property
    def np(auto):
        return auto.numpy

    @property
    def pd(auto):
        return auto.pandas

    @property
    def sklearn(auto):
        import sklearn
        import sklearn.base
        import sklearn.calibration
        import sklearn.cluster
        import sklearn.compose
        import sklearn.covariance
        import sklearn.cross_decomposition
        import sklearn.datasets
        import sklearn.decomposition
        import sklearn.discriminant_analysis
        import sklearn.dummy
        import sklearn.dummy
        import sklearn.ensemble
        import sklearn.ensemble
        import sklearn.exceptions
        import sklearn.experimental
        import sklearn.feature_extraction
        import sklearn.feature_extraction.image
        import sklearn.feature_extraction.text
        import sklearn.gaussian_process
        import sklearn.impute
        import sklearn.inspection
        import sklearn.isotonic
        import sklearn.kernel_approximation
        import sklearn.kernel_ridge
        import sklearn.linear_model
        import sklearn.manifold
        import sklearn.metrics
        import sklearn.metrics.cluster
        import sklearn.mixture
        import sklearn.model_selection
        import sklearn.multiclass
        import sklearn.multioutput
        import sklearn.naive_bayes
        import sklearn.neighbors
        import sklearn.neural_network
        import sklearn.pipeline
        import sklearn.preprocessing
        import sklearn.random_projection
        import sklearn.semi_supervised
        import sklearn.svm
        import sklearn.tree
        import sklearn.utils
        return sklearn

    @property
    def scipy(auto):
        import scipy
        import scipy.cluster
        import scipy.constants
        import scipy.datasets
        import scipy.fft
        import scipy.fftpack
        import scipy.integrate
        import scipy.interpolate
        import scipy.io
        import scipy.linalg
        import scipy.misc
        import scipy.ndimage
        import scipy.odr
        import scipy.optimize
        import scipy.signal
        import scipy.sparse
        import scipy.spatial
        import scipy.special
        import scipy.stats
        return scipy

    @property
    def mpl(auto):
        return auto.matplotlib

    @property
    def plt(auto):
        return auto.matplotlib.pyplot
    
    @property
    def matplotlib(auto):
        import matplotlib
        import matplotlib.pyplot
        return matplotlib
    
    @property
    def PIL(auto):
        import PIL
        import PIL.BmpImagePlugin
        import PIL.ExifTags
        import PIL.GifImagePlugin
        import PIL.GimpGradientFile
        import PIL.GimpPaletteFile
        import PIL.Image
        import PIL.ImageChops
        import PIL.ImageColor
        import PIL.ImageFile
        import PIL.ImageMode
        import PIL.ImageOps
        import PIL.ImagePalette
        import PIL.ImageSequence
        import PIL.JpegImagePlugin
        import PIL.JpegPresets
        import PIL.PaletteFile
        import PIL.PngImagePlugin
        import PIL.PpmImagePlugin
        import PIL.TiffImagePlugin
        import PIL.TiffTags
        return PIL

    @property
    def tqdm(auto):
        import tqdm
        import tqdm.auto
        import tqdm.notebook
        return tqdm

    @property
    def tkinter(auto):
        import tkinter
        import tkinter.ttk
        import tkinter.scrolledtext
        import tkinter.dnd
        import tkinter.font
        import tkinter.tix
        import tkinter.colorchooser
        import tkinter.messagebox
        return tkinter

    @property
    def google(auto):
        import google
        import google.colab
        import google.colab.syntax
        import google.colab.userdata
        return google

    @property
    def fastapi(auto):
        import fastapi
        import fastapi.templating
        import fastapi.middleware.cors
        return fastapi


auto = AutoImport()
