from numbers2chords import get_bits

class BloomFilter:

    def __init__(self, n) -> None:
        self.length = n
        self.__bit_array = [0]*self.length

    def reset(self) -> None:
       self.__bit_array = [0]*self.length
        
    def add_bits(self, bits: list) -> None:
      for i, b in enumerate(bits):
          self.__bit_array[i % self.length] |= b

    def get_bits(self, n) -> list:
        return get_bits(n)

    def add_number(self, n: int) -> None:
        b = self.get_bits(n)
        self.add_bits(b)
    
    def test(self, n) -> bool:
        bits = self.get_bits(n)
        exists = True
        for i, b in enumerate(bits):
            if b:
              if not self.__bit_array[i % self.length]:
                exists = False
        return exists
    
    def __str__(self) -> str:
       percent_filled = (sum(self.__bit_array)*1.0)/ (self.length*1.0)
       return str(f"BloomFilter{{length={self.length}, percent filled = {percent_filled*100.0}%}}")