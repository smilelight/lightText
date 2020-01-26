class Character:
    def __init__(self, pattern):
        assert type(pattern) == str
        assert len(pattern) == 1
        self.pattern = pattern

    def __eq__(self, other):
        if type(other) == str:
            return self.pattern == other
        if type(other) == Character:
            assert type(other) == Character
            return self.pattern == other.pattern

    def __str__(self):
        return self.pattern

