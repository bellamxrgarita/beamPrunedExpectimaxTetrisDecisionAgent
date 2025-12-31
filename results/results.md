# Results
To test our agents and compare their performances, we used agentSimulator.py to simulate several rounds with a specified number of played pieces. We ran both expectimax and beamSearch against the tests which simulate different combinations of inputs(10 pieces, 20 pieces, 50 pieces, 100 pieces, 200 pieces played). For the tests that only played 10 and 20 pieces, the results were comparable, with the average lines/pieces ratio of beamSearch being slightly higher than expectimax. However, as the number of pieces played increases in the other test cases, so does the difference in performance between the two agents. Beam search consistently did better than expectimax in both the number of lines cleared, and the ratio of lines cleared to pieces placed. These results show that while expectimax is faster and works in smaller game plays, beamSearch is more effective at maximizing the number of lines cleared to avoid game failure. The results of the tests we ran are shown below:

### TEST: (3 runs, 10 pieces played) — Expectimax

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 1             | 2.074s       |
| 2   | 3             | 3.369s       |
| 3   | 3             | 6.188s       |

**Average Lines Cleared:** 2.33  
**Average Lines/Piece Ratio:** 0.2333
### TEST: (3 runs, 10 pieces played) — BeamSearch

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 2             | 15.879s      |
| 2   | 3             | 16.983s      |
| 3   | 3             | 15.389s      |

**Average Lines Cleared:** 2.67  
**Average Lines/Piece Ratio:** 0.2667

### TEST: (4 runs, 20 pieces played) — Expectimax

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 6             | 8.529s       |
| 2   | 5             | 6.926s       |
| 3   | 5             | 11.606s      |
| 4   | 7             | 9.173s       |

**Average Lines Cleared:** 5.75  
**Average Lines/Piece Ratio:** 0.2875

### TEST: (4 runs, 20 pieces played) — BeamSearch

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 7             | 30.653s      |
| 2   | 7             | 32.363s      |
| 3   | 6             | 26.532s      |
| 4   | 7             | 34.070s      |

**Average Lines Cleared:** 6.75  
**Average Lines/Piece Ratio:** 0.3375

### TEST: (5 runs, 50 pieces played) — Expectimax

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 15            | 17.042s      |
| 2   | 18            | 26.918s      |
| 3   | 12            | 16.517s      |
| 4   | 16            | 18.248s      |
| 5   | 16            | 21.539s      |

**Average Lines Cleared:** 15.40  
**Average Lines/Piece Ratio:** 0.3080

### TEST: (5 runs, 50 pieces played) — BeamSearch

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 19            | 89.262s      |
| 2   | 18            | 79.878s      |
| 3   | 19            | 80.263s      |
| 4   | 19            | 87.186s      |
| 5   | 18            | 78.373s      |

**Average Lines Cleared:** 18.60  
**Average Lines/Piece Ratio:** 0.3720

### TEST: (5 runs, 100 pieces played) — Expectimax

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 38            | 38.217s      |
| 2   | 32            | 38.737s      |
| 3   | 38            | 38.443s      |
| 4   | 35            | 40.001s      |
| 5   | 36            | 39.363s      |

**Average Lines Cleared:** 35.80  
**Average Lines/Piece Ratio:** 0.3580

### TEST: (5 runs, 100 pieces played) — BeamSearch

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 38            | 165.305s     |
| 2   | 39            | 167.194s     |
| 3   | 39            | 163.662s     |
| 4   | 38            | 168.336s     |
| 5   | 37            | 174.214s     |

**Average Lines Cleared:** 38.20  
**Average Lines/Piece Ratio:** 0.3820

### TEST: (5 runs, 200 pieces played) — Expectimax

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 75            | 78.007s      |
| 2   | 79            | 83.699s      |
| 3   | 77            | 74.043s      |
| 4   | 69            | 71.655s      |
| 5   | 75            | 86.224s      |

**Average Lines Cleared:** 75.00  
**Average Lines/Piece Ratio:** 0.3750

### TEST: (5 runs, 200 pieces played) — BeamSearch

| Run | Lines Cleared | Time Elapsed |
|-----|---------------|--------------|
| 1   | 78            | 324.707s     |
| 2   | 79            | 333.128s     |
| 3   | 79            | 325.346s     |
| 4   | 79            | 327.668s     |
| 5   | 78            | 328.826s     |

**Average Lines Cleared:** 78.60  
**Average Lines/Piece Ratio:** 0.3930

