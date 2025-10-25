# Genetic algorithm experiment

This is a little genetic programming experiment. It doesn't do much: it attempts to approximate a number with a binary "DNA" string.

The DNA is just a random string of bits. This random string of bits is a program used to approximate the number.

Specifically, we start with a value 0. If the nibble is anywhere in the range 0..9, the nibble is added to the value. Subsequent nibbles are given additional meanings:

10 -> Value is divided by 2 11 -> Value is multiplied by 2 12 -> Value is decremented by 1 13 -> Value is incremented by 1 14 -> Value is decremented by .1 15 -> Value is incremented by .1

However any set of operations could be given to the nibbles. What matters is that every block of 4 bits has some meaning, even if that meaning is a NoOp. Note that in the above, a nibble 0001 has the same meaning as 1101; both will add 1 to the intermediate value. This was strictly accidental.

Good. With the program represented as a random string, we can now run the program and calculate the output value.

We then sort the results and keep the top half set of programs that has rendered the result closest to the intended output.

Next, we "mate" programs. To do so:

- We start with two DNA strings
- Choose a random point in those strings
- Cut the strings at that point
- And combine parts of the two programs with each other.

Finally, to represent mutations, sometimes a program bit may be randomly flipped.

# Observations

- Longer programs will have longer calculations and as a result they are more likely to be fractionally incorrect, but they will also have more opportunity to get close to the target result.

- As we get closer to the desired result, the odds of getting a better result than "best so far" will decrease since we're getting ever closer to a "local minimum". To counter-act this, we can make mutations increasingly likely from one generation to the next, which will shake up things a bit and allow the program to adapt a novel approach.

# Next steps

Now imagine an audio wave form - since our current program only generates a single value, obviously it is not a very efficient way to approximate such a wave form. If we had "output current value" and loop instructions, however, we could generate output strings of arbitrary length. Also, if we know we're generating audio, we could include sine generators controllable with amplitude and phase params to help things along.
