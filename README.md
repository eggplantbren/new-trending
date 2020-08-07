# New Trending

Algorithms for Lex to try with the new SDK.

(c) 2020 Brendon J. Brewer. LICENSE: MIT


## Variable Decay
This is _not_ equivalent to the versions currently running, but it is
based on similar ideas.

Speed test on the example data:

```
In [6]: %timeit variable_decay.trending_score(801000, data)                     
3.92 µs ± 120 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```
