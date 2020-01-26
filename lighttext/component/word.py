class Word:
    def __init__(self, pattern):
        assert type(pattern) == str
        assert len(pattern) >= 1
        self.pattern = pattern

    def __eq__(self, other):
        if type(other) == str:
            return self.pattern == other
        if type(other) == Word:
            assert type(other) == Word
            return self.pattern == other.pattern

    def __str__(self):
        return self.pattern
