import typing

class Throw:
    def __init__(self, score: typing.Union[int, str], modif=1, valid: bool = True):
        self.modifier = modif
        self.out = False
        self.foul = False
        self.valid = valid

        if isinstance(score, int):
            self.score = score
        else:
            if score == 'o':
                self.score = 0
                self.out = True
            elif score == 'f':
                self.score = 0
                self.foul = True

    def __eq__(self, other):
        if isinstance(other, Throw):
            return self.score == other.score and self.modifier == other.modifier and self.out == other.out and \
                   self.foul == other.foul
        return False