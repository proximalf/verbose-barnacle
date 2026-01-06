try:
    from ._execute import main
except:

    def main():
        print("This util is missing! \nOptional install - `pip install qtcomponents[cli]`")
        pass
