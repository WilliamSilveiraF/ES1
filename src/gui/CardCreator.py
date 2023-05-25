from gui.ShapeCreator import ShapeCreator

class CardCreator(ShapeCreator):
    def __init__(self, frame, card_width, card_attributes):
        super().__init__(frame)
        self.card_width = card_width
        self.card_attributes = card_attributes

    def create_card(self, x1, y1, x2, y2, radius):
        self.create_rounded_rect(x1, y1, x2, y2, radius=radius, fill=self.card_attributes[1], outline=self.card_attributes[2])
