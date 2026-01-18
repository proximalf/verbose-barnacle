from PySide6.QtWidgets import QWidget

from qtcomponents.view import ImageViewComponent

from .lib import test_image, test_widget


@test_widget
def main() -> QWidget:

    component = ImageViewComponent()

    component.set_image(test_image())

    return component.widget


if __name__ == "__main__":
    main()
