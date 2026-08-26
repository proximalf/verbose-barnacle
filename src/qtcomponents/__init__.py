from . import log, serial
from .file import FileDialog
from .plot import MatplotlibWidget

try:
    # if Qt isn't installed this will fail
    from .image import image_to_pixmap 
except ImportError or ModuleNotFoundError:

    def image_to_pixmap(*args, **kwargs):
        raise RuntimeError("image_to_pixmap requires pennyio - pip install qtcomponents[image]")