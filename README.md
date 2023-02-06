# Thoughts and Ideas
- bloom filter but set 0s too, use as sine waves to combine (0th=sine, 1st=sine\*2^1, 2nd=sine\*2^2… ith=sine*2^i) for evolving tone. Alternatively, use traditional filter for only growing noise sine wave
- instead of messing w/ hex, how about convert to base7 and then that becomes the notes?
  - then you could use base16 or something else... chords...?
  - base10 int to arbitrary base helper func
    ```python
    def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]
    ```
- need to encourage runs more (maybe not.. listen to A266069)
- repetition / global structure needs to be created & enforced
  - along with some basic harmonic rules, i.e. end on the tonic? but also this is technically a "never done" composition
  - maybe somehow the numbers themselves also inform structure.. like order # 324 adds to the composition and also creates the sequence of segments 3, 2, and 4. Or 3 % <# of parts>, 2 % <# of parts>, 4 % <# of parts> or something... or just use 
- need some way maybe to occassionally change the BEATS_PER_LINE? Or some other way to vary order (magnitude) of note sizes. i.e from 64 to 32 for faster part ,or 128 for slower sections. This also can come from large and small numbers, which via resolution will lead to fast/slow sections
- ✅ ~~need to enforce time signature / measures better. even with splitting or truncating phrases or something.~~ 
  - ~~However, the added rhythmic complexity of allowing to cross measure boundaries is nice and don't totally want to lose that~~
  - ~~maybe splitting notes and doubling over phrases is better, and then let midi resolution merge~~
  - ~~or, alternatively, just force chords to stick to measures which could give better coherence~~
- instead of doing all chords for 1 measure, lets say if the distance to closest chord is > some cutoff X,
break the measure into two chords. This could be recursive, and X would scale the pace of chords (max 1 meaasure still)
- Maybe blend chords that are repeated instead of going inversions? Idk... Inversions are cool too
- *the motifs that emerge are incredible interesting.. so cool... what in the sequence/numbers makes this happen??*