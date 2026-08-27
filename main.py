import sys


def main():
    if "--cli" in sys.argv:
        import src.app_cli as app
        app.run()
    else:
        import src.app as app
        app.run()


if __name__ == "__main__":
    main()