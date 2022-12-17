import os


class Paths:
    base: str = os.path.dirname(__file__)
    static: str = os.path.join(base, "static")
    media: str = os.path.join(static, "media")

    # * app specific
    posts: str = os.path.join(media, "posts")


paths = Paths()
