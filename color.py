

class Colors:
    black = (0, 0, 0)
    white = (255, 255, 255)
    yellow = (255, 255, 0)
    gray=(128,128,128)
    red=(255,0,0)

    @classmethod
    def get_block_colors(cls):
        return [cls.black, cls.white, cls.yellow]