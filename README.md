# Genetic algorithm experiment

This is a little genetic programming experiment. It doesn't do much: it attempts to approximate a number with a binary "DNA" string.

The DNA is just a random string of bits. This random string of bits is a program used to approximate the number.

Specifically, we start with a value 0.

We give each nibble a meaning.

| Nibble | Meaning                                              |
|--------|------------------------------------------------------|
| 0 - 9  | Add nibble to value                                  |
| a      | Divide value by 2                                    |
| b      | Multiply value by 2                                  |
| c      | Decrement value by 1                                 |
| d      | Increment value by 1                                 |
| e      | Reduce value by .1                                   |
| f      | Increase value by .1                                 |

However any set of operations could be given to the nibbles.

What matters is that every block of 4 bits has some meaning, even if that meaning is a NoOp;
any binary string is a valid program.

Note that in the above, a nibble 0001 has the same meaning as 1101;
both will add 1 to the intermediate value. This was strictly accidental.

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

Currently we have a single input and always apply the same operations,
so this isn't very useful.
It would be more useful to evolve the program to approximate a function.
To accomplish this, given an input value x (0, 1, 2, 3...) it might generate
an output value y. The set of operators may be more complex to allow things
such as sin/cos, setting polynomial parameters, or even implement feedback
loops / recursion where a value X is calculated based on the value (x-n).
The fitness may need to be calculated over the entire function.
Perhaps we want to evolve a circle, where input = angle and output = x, y.
Perhaps we want to make our instruction set Turing complete.

It's up to you!
