# fastest-primes — AIProve entry

**Entry:** `primes.c` (C11) + prebuilt `./primes` binary.
**Run command:** `./run.sh` — reads N on stdin, prints π(N) on stdout.
(`run.sh` uses the committed binary if present, else builds it with
`gcc -O3 -march=native -std=c11 -o primes primes.c` first. Equivalent direct
form: `gcc -O3 -march=native -std=c11 -o primes primes.c && echo 5000000 | ./primes`.)

**Metric: wall-clock latency on hidden N (1 ≤ N ≤ 5,000,000); wrong output is
disqualified before timing.**

## Implementation

Bit-packed odd-only sieve of Eratosthenes:

- Bit `i` ↔ odd number `2i+1`; a set bit means composite (bit 0 marks the
  number 1). At N = 5·10⁶ the sieve is 313 KB — cache-resident.
- Marking starts at `p²` with index step `p` (= number step `2p`), odd `p` only.
- Count = `1 + size − popcount(bits)` (the `+1` is the prime 2), using
  `__builtin_popcountll`; input is read with a single `fread` + `strtol`,
  output with one `fwrite` — no stdio formatting overhead in the hot path.
- A byte-array variant was built and benchmarked head-to-head; the bit-packed
  version won (medians 5.63 ms vs 6.33 ms over 15 runs each) and was kept.

## Correctness (see build-transcript.txt)

All verified locally against known π(x) values — **every check passed**:

- Public samples: π(10)=4, π(100)=25, π(1000)=168, π(100000)=9592,
  π(1000000)=78498.
- Edges: π(1)=0, π(2)=1, π(3)=2, π(4)=2, π(5)=3, π(97)=25, π(541)=100.
- Large: π(10⁴)=1229, π(2·10⁶)=148933, π(3·10⁶)=216816, π(4·10⁶)=283146,
  **π(5·10⁶)=348513**.

## Benchmarks (this shared VM, end-to-end incl. process start, N=5,000,000)

- Head-to-head round (15 runs each): bitset **median 5.63 ms**, min 5.47 ms;
  byte sieve median 6.33 ms.
- Final binary, 11-run round: **min 6.15 ms, median 7.40 ms**.
- Later rounds under heavy shared-CPU contention showed medians of
  11–12 ms with outliers to ~60 ms (the box is a 1.5-vCPU shared VM;
  the grader runs all entries back-to-back on one machine, so relative
  standing is what counts). Process-start floor alone measures ~1–2 ms,
  so the sieve itself is roughly 4–5 ms at N = 5·10⁶.

## Run the tests

```bash
python3 test_bench.py        # correctness suite + benchmark at N=5,000,000
echo 5000000 | ./run.sh      # 348513
```
