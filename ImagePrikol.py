from PIL import Image


class ImageRedact:
    def __init__(self, name):
        self.name = name
        self.image = Image.open(self.name)
        self.image2 = Image.open(self.name)
        self.pixels = self.image.load()
        self.x, self.y = self.image.size
        self.surname = self.name.split('.')[0]
        self.type = self.name.split('.')[1]

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_name(self):
        return self.surname.split('/')[-1]

    def get_image(self):
        return self.image

    def get_type(self):
        return self.type

    def reset(self):
        self.image = self.image2
        self.x, self.y = self.image.size

    def negative(self):
        for row in range(self.x):
            for col in range(self.y):
                if len(self.pixels[row, col]) == 3:
                    r, g, b = self.pixels[row, col]
                    self.pixels[row, col] = 255 - r, 255 - g, 255 - b
                if len(self.pixels[row, col]) == 4:
                    r, g, b, a = self.pixels[row, col]
                    self.pixels[row, col] = 255 - r, 255 - g, 255 - b, a

    '''
    def tone(self, red_delta, green_delta, blue_delta):
        for row in range(self.x):
            for col in range(self.y):
                print(row, col)
                if len(self.pixels[row, col]) == 3:
                    r, g, b  = self.pixels[row, col]
                if len(self.pixels[row, col]) == 4:
                    r, g, b, a = self.pixels[row, col]
                r, g, b, = r + red_delta, g + green_delta, b + blue_delta
                if r > 255:
                    r = 255
                elif r < 0:
                    r = 0
                if g > 255:
                    g = 255
                elif g < 0:
                    g = 0
                if b > 255:
                    b = 255
                elif b < 0:
                    b = 0
                if len(self.pixels[row, col]) == 3:
                    self.pixels[row, col] = r, g, b
                if len(self.pixels[row, col]) == 4:
                    self.pixels[row, col] = r, g, b, a
    '''

    def reflectOX(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)

    def reflectOY(self):
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

    def prikol(self, delta):
        empt_im = Image.new('RGB', (self.x, self.y), (0, 0, 0))
        empt_pixels = empt_im.load()
        for row in range(self.x):
            for col in range(self.y):
                if row < delta:
                    r, g, b = self.pixels[row, col]
                    empt_pixels[row, col] = r, g, b
                else:
                    empt_pixels[row, col] = r, g, b
                    g, b = self.pixels[row, col][1:]
                    r = self.pixels[row - delta, col][0]
        self.image = empt_im

    def crop(self, x1, y1, x2, y2):
        if x1 < x2 and y1 < y2 and x1 >= 0 and y1 >= 0 and x2 <= self.x and y2 <= self.y:
            self.image = self.image.crop((x1, y1, x2, y2))
            self.x, self.y = x2 - x1, y2 - y1

    def update(self):
        self.image.save(self.name)
        self.pixels = self.image.load()

    def autosave(self):
        self.image2.save(f"{self.surname}1.{self.type}")