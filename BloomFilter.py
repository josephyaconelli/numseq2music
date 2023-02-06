

class BloomFilter:

    def __init__(self, n) -> None:
        self.__bit_array = [0]*n
        
    def add_bits(self, bits) -> None:
        bytes("hel")