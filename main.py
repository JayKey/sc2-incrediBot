import asyncio
from sc2 import maps
from sc2.data import Difficulty, Race, Result
from sc2.main import run_game
from sc2.player import Bot, Computer
from botLogic.bot import IncrediBot

def run_game_with_difficulty(difficulty):
    result = run_game(
        maps.get("AbyssalReefLE"),
        [
            Bot(Race.Protoss, IncrediBot()),
            Computer(Race.Zerg, difficulty)
        ],
        realtime=False,
    )
    return result

def main():
    difficulties = [Difficulty.Easy, Difficulty.Medium, Difficulty.Hard, Difficulty.Harder, Difficulty.VeryHard, Difficulty.CheatVision, Difficulty.CheatMoney, Difficulty.CheatInsane]
    win_loss_ratios = {difficulty: [0, 0] for difficulty in difficulties}
    current_difficulty = Difficulty.Easy

    while True:
        print(f"Starting game against {current_difficulty}...")
        result = run_game_with_difficulty(current_difficulty)
        print(result)

        if result == Result.Victory:
            win_loss_ratios[current_difficulty][0] += 1
        else:
            win_loss_ratios[current_difficulty][1] += 1

        print(f"Result against {current_difficulty}: {'Win' if result == Result.Victory else 'Loss'}")
        print("Current win/loss ratios:")
        for difficulty, (wins, losses) in win_loss_ratios.items():
            ratio = wins / (losses or 1)
            print(f"{difficulty}: {wins}/{losses} ({ratio:.2f})")

        # Check if the win/loss ratio is 4:1 or better to increase difficulty
        if win_loss_ratios[current_difficulty][0] / (win_loss_ratios[current_difficulty][1] or 1) >= 4:
            next_difficulty_index = difficulties.index(current_difficulty) + 1
            if next_difficulty_index < len(difficulties):
                current_difficulty = difficulties[next_difficulty_index]
                print(f"Win/loss ratio is 4:1 or better. Moving to {current_difficulty}.")
            else:
                print("Reached the highest difficulty. Stopping.")
                break

        # Check if the win/loss ratio is below 0.5 to decrease difficulty
        elif win_loss_ratios[current_difficulty][0] / (win_loss_ratios[current_difficulty][1] or 1) < 0.5:
            prev_difficulty_index = difficulties.index(current_difficulty) - 1
            if prev_difficulty_index >= 0:
                current_difficulty = difficulties[prev_difficulty_index]
                print(f"Win/loss ratio is below 0.5. Moving to {current_difficulty}.")
            else:
                print("Reached the lowest difficulty. Cannot decrease further.")

if __name__ == "__main__":
    main()
