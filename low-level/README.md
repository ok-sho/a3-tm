# π Turing Machine

This folder contains the turing machine transition states as well as the Laconic code to build said turing machine. The TM is a 2 state machine (a and b) and calculates the first 30 digits of PI.

---

## Attribution & Credit

**All credit for the Laconic language and Turing machine compiler goes to Adam Yedidia:**

- **Repository:** https://github.com/adamyedidia/parsimony
- **What he created:** The entire Laconic language and the compiler that converts Laconic code to Turing machines

**My contribution:** I wrote `pi30.lca` (the Laconic source code) and compiled it using his tools to produce `pi30.tm2`.

To reproduce this work, you must clone Yedidia's repository and follow his tutorial. The files in this repository (`pi30.lca` and `pi30.tm2`) are the output of using his language and compiler, not new tools I built.

---

## Laconic File: `pi30.lca`

My implementation of the Rabinowitz-Wagon spigot algorithm for calculating digits of PI. I chose this algorithm due to its simple arithmetic as well as sequential generation of the digits.

The code may look odd to a person unfamiliar with Laconic (such as myself), but most of the peculiarity comes from the limited amount of operations in the language. These peculiarities are:

1. **Giant function signatures** — From my testing, all Laconic variables must be defined globally and then passed as parameters. This makes functions like pi_spigot seem ridiculous as it has 16 input parameters.

2. **Repeated if statements** — As far as I'm aware there are no "else" or "else if" statements in Laconic so all logic had to be coded with if statements. (Silly stuff like `if (a) {foo()} if (not a) {bar()}`).

3. **O(N) array assignments** — From reading the documentation I could not find a way to write to an array index, this meant that if I wanted to change a value inside an array I needed to rebuild the entire array by appending each element one by one and putting the element I want in the correct spot.

---

## Turing Machine: `pi30.tm2`

The resulting turing machine consists of 5773 states and would take days or even months to halt. The author specified that the compiler is optimized to minimize the number of states rather than the speed of execution. This combined with my inefficient implementation of the Rabinowitz-Wagon spigot means that this TM is created purely out of curiosity and for brownie points.

The rest of the code in this repository does not rely on this TM in any way (but does make use of the aforementioned algorithm).