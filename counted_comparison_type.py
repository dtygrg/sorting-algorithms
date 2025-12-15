from functools import total_ordering

@total_ordering
class CountedComparisons:
    comparisons = 0

    def __init__(self, value):
        self.value = value

    @classmethod
    def reset(cls):
        cls.comparisons = 0

    @classmethod
    def get_count(cls) -> int:
        return cls.comparisons

    def __lt__(self, other):
        CountedComparisons.comparisons += 1
        if isinstance(other, CountedComparisons):
            return self.value < other.value
        return self.value < other

    def __eq__(self, other):
        CountedComparisons.comparisons += 1
        if isinstance(other, CountedComparisons):
            return self.value == other.value
        return self.value == other
