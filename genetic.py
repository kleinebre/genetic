#!/usr/bin/env python3
from random import random as rnd

target = float(int(1000*rnd()))/10
target = 952
print("We want to approximate "+str(target))

POPULATION_SIZE = 30
growthrate = 1
MAX_GENERATIONS = 1000
BINLEN = 64

def random_bit():
    # generates a random bit.
    return str(int(rnd()*2))

def generate_dna(mylen):
    # generates a length of random bits.
    x = ''

    for i in range(0,mylen):
        x += random_bit()

    return x

def representedval(binstr, printop=False):
    # Translates a string of random bits into
    # the output that that string represents.
    # Each random string is treated as a valid
    # "program", and this function is the clever
    # bit that runs that program and returns the
    # "but what does it mean?" final output of
    # that program.
    #
    # In this case, any binary string is a program
    # that represents a floating point value.

    my_ops = []
    orig_str = binstr
    while True:
        if binstr == "":
            break
        nibble = binstr[0:4]
        binstr = binstr[4:]
        nibval = (8*int(nibble[0])) + \
                 (4*int(nibble[1])) + \
                 (2*int(nibble[2])) + \
                 int(nibble[3])

        #print "nibval = " + str(nibval)
        if (nibval < 10):
            #print "append " + str(nibval)
            my_ops.append(str(nibval))
            continue

        if (nibval == 10):
            my_ops.append(">>")
            continue

        if (nibval == 11):
            my_ops.append("<<")
            continue

        if (nibval == 12):
            my_ops.append("--")
            continue

        if (nibval == 13):
            my_ops.append("++")
            continue

        if (nibval == 14):
            my_ops.append(".")
            continue

        if (nibval == 15):
            my_ops.append(",")
            continue
    val = 0
    strplus = ""
    opstr = ""
    for op in my_ops:
        opstr += op
        if op in ('0','1','2','3','4','5','6','7','8','9'):
            strplus += op
            continue
        if (strplus != ""):
            val += int(strplus)
            strplus = ""
        if op == ">>":
            val /= 2
            continue
        if op == "<<":
            val *= 2
            continue
        if op == "++":
            val += 1
            continue
        if op == "--":
            val -= 1
            continue
        if op == ".":
            val -= .1
            continue
        if op == ",":
            val += .1
            continue

    if printop:
        print(opstr + " result = " + str(val))

    return float(val)

# We generate an initial population which is random.

population = []
for i in range(0,POPULATION_SIZE):
    dna = generate_dna(BINLEN)
    population.append(dna)

# For each of the individuals, we generate the output
# of the given "dna".

generation = 0
best_fitness_score = 1000000000
while True:
    generation += 1
    if generation > MAX_GENERATIONS:
        break

    # We've got DNA, but what does it represent???
    repval = []
    for dna in population:
        repval.append(representedval(dna))

    # Calculate (un)fitness
    fitness = []
    for i in range(0,POPULATION_SIZE):
        rep_fitness = abs(target - repval[i])
        fitness.append(rep_fitness)

    # Sort by fitness / selection
    # lowest number first normally means least fit individual first but
    # I actually like it when the fittest individuals are at the top
    # of the list (more efficient!) so in this case
    # lower scores represent higher fitness.

    dna_by_fitness =  [x for (y,x) in sorted(zip(fitness,population))]
    dna_fitness_score =  [y for (y,x) in sorted(zip(fitness,population))]

    # Evaluate fitness

    fitness = dna_fitness_score[0]

    if fitness < best_fitness_score:
        # we have beaten the fitness record.
        best_fitness_score = fitness
        print("Found a fitter candidate at generation %s with score %s" \
                % (generation, best_fitness_score))
        print(representedval(dna_by_fitness[0],printop=True))
        if best_fitness_score < .0001:
            exit(0)

    # Selection - let's kill off the worst half of the population

    half_pop=int(POPULATION_SIZE/2)
    dna_by_fitness = dna_by_fitness[:half_pop]
    dna_fitness_score = dna_fitness_score[:half_pop]
    population = dna_by_fitness
    curr_pop = half_pop
    POPULATION_SIZE = int(POPULATION_SIZE * growthrate)
    if (POPULATION_SIZE & 2) == 1:
        POPULATION_SIZE +=1

    while True:
        # Mating - choose and mate a pair of candidates
        # until the population has grown back to its original size

        while True:
            candidate_1 = int(half_pop*rnd())
       	    candidate_2 = int(half_pop*rnd())
            if candidate_1 != candidate_2:
                break

        #print "Mating candidate %s and %s" % (candidate_1, candidate_2)
        #print "Fitness scores before %s and %s" % (fitness[candidate_1], fitness[candidate_2])

        # Mate the candidates
        words = BINLEN / 4
        cutoff = int(rnd()*words)*4
        dna_c1 = dna_by_fitness[candidate_1]
        dna_c2 = dna_by_fitness[candidate_2]
        #print "Old DNA c1 :" + dna_c1
        #print "Old DNA c2 :" + dna_c2

        new_dna_disp = dna_c1[0:cutoff] + " - " +dna_c2[cutoff:]
        new_dna = dna_c1[0:cutoff] + dna_c2[cutoff:]
        #print "New DNA c3 :" + new_dna_disp+" => %s" % representedval(new_dna)

        # Mutation
        # (ignore for now)
        for mut in range(0,5):
            # comparing with generation number makes mutations
            # increasingly likely over multiple generations.
            # The purpose of this is to allow stabilised evolutions
            # to escape local minimum pits.
            if int(rnd()*1000) < generation:
                #print "Mutate dna..."
                #print "BEFORE mut: "+new_dna
                x=int(rnd()*BINLEN)
                #print "mutpos = %s" %x

                new_dna=new_dna[:x]+str(1-int(new_dna[x]))+new_dna[x+1:]
                #print " AFTER mut: "+new_dna

        population.append(new_dna)

        curr_pop += 1
        if curr_pop == POPULATION_SIZE:
            break
