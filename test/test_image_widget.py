from PySide6.QtWidgets import QWidget

from .lib import test_widget, test_image

from qtcomponents.view import ImageViewComponent


@test_widget
def main() -> QWidget:

    component = ImageViewComponent()

    component.set_image(test_image())

    return component.widget


if __name__ == "__main__":
    main()
