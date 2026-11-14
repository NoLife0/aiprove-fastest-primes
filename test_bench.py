#!/usr/bin/env python3
"""Correctness + benchmark for ./primes (fastest-primes entry).
Correctness: public cases.json, edge cases, known pi(x) values up to 5e6.
Benchmark: repeated runs at N=5,000,000 (the max), reporting every timing.
"""
import json, subprocess, sys, time

BIN = ["./primes"]
RUNS = sys.argv[1:] and int(sys.argv[1]) or 9

def pi(n):
    t0 = time.perf_counter()
    out = subprocess.run(BIN, input=f"{n}\n", capture_output=True, text=True, check=True).stdout.strip()
    return int(out), time.perf_counter() - t0

ok = True
def check(n, want):
    global ok
    got, dt = pi(n)
    status = "OK " if got == want else "FAIL"
    if got != want: ok = False
    print(f"{status} pi({n}) = {got} (want {want})  [{dt*1000:.2f} ms]")

# public samples
for c in json.load(open("cases.json")):
    check(c["n"], c["count"])
# edges
for n, want in [(1, 0), (2, 1), (3, 2), (4, 2), (5, 3), (6, 3), (7, 4), (97, 25), (541, 100)]:
    check(n, want)
# known pi(x) at larger checkpoints
for n, want in [(10**4, 1229), (10**5, 9592), (10**6, 78498), (2*10**6, 148933),
                (3*10**6, 216816), (4*10**6, 283146), (5*10**6, 348513)]:
    check(n, want)

print("\nbenchmark: N=5000000, repeated runs (process start + sieve + print)")
times = []
for k in range(RUNS):
    got, dt = pi(5_000_000)
    assert got == 348513, got
    times.append(dt)
    print(f"  run {k+1}: {dt*1000:.3f} ms")
times.sort()
print(f"min={times[0]*1000:.3f} ms  median={times[len(times)//2]*1000:.3f} ms  max={times[-1]*1000:.3f} ms")
print("CORRECTNESS:", "ALL OK" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)
