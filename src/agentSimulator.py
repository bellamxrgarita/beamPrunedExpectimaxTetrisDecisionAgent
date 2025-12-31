# Measure of success

# number of lines cleared 
# pieces played 
# have the game simulator only run for 50 actions taken 
# end of the board --> score will be number of lines cleared by the agent/ pieces played 

# better agent would theoretically have a higher lines cleared to actions taken ratio 

from gameSimulator import TetrisApp
from beamPrunedExpectimaxAgent import beamPrunedExpectimaxAgent
from beamsearchChanceAgent import beamsearchChanceAgent  

#NUM_RUNS = 3         
#MAX_PIECES = 20

def run_agent_tests(agent_class, agent_name, numRuns, maxPieces):
    print("\n============================")
    print(f" Running tests for: {agent_name} ({numRuns} runs, {maxPieces} pieces played)")
    print("============================")

    results = []

    for i in range(numRuns):
        agent = agent_class(agent_name)
        app = TetrisApp(agent, headless=True)

        metrics = app.limitGameLoop(maxPieces)

        results.append(metrics)
        print(f"Run {i+1}: lines={metrics['lines']} | pieces={metrics['pieces']} | time={metrics['time']:.3f}s")

    # averages
    avg_lines = sum(r["lines"] for r in results) / numRuns
    avg_ratio = sum(r["lines"] / r["pieces"] for r in results) / numRuns

    print("\n----- SUMMARY -----")
    print(f"Avg Lines Cleared:      {avg_lines:.2f}")
    print(f"Avg Lines/Piece Ratio:  {avg_ratio:.4f}")
    print("-------------------\n")


if __name__ == "__main__":
    run_agent_tests(beamPrunedExpectimaxAgent, "Beam Pruned Expectimax", 3, 10)
    run_agent_tests(beamsearchChanceAgent, "3-Ply BeamSearch with Chance Layer", 3, 10)

    run_agent_tests(beamPrunedExpectimaxAgent, "Beam Pruned Expectimax", 4, 20)
    run_agent_tests(beamsearchChanceAgent, "3-Ply BeamSearch with Chance Layer", 4, 20)

    run_agent_tests(beamPrunedExpectimaxAgent, "Beam Pruned Expectimax", 5, 50)
    run_agent_tests(beamsearchChanceAgent, "3-Ply BeamSearch with Chance Layer", 5, 50)

    run_agent_tests(beamPrunedExpectimaxAgent, "Beam Pruned Expectimax", 5, 100)
    run_agent_tests(beamsearchChanceAgent, "3-Ply BeamSearch with Chance Layer", 5, 100)

    run_agent_tests(beamPrunedExpectimaxAgent, "Expectimax", 5, 200)
    run_agent_tests(beamsearchChanceAgent, "3-Ply BeamSearch with Chance Layer", 5, 200)

