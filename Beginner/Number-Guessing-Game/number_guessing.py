import random
import time


high_scores = {}

def welcome_message():
    print("🎉 Welcome to the Number Guessing Game! 🎉")
    print("Rules of the Game:")
    print("1. I'm thinking of a number between 1 and 100.")
    print("2. You will select a difficulty level which determines how many chances you have:")
    print("   - Easy: 10 chances")
    print("   - Medium: 5 chances")
    print("   - Hard: 3 chances")
    print("3. After each guess, I'll tell you if your guess is too high or too low.")
    print("4. If you're stuck, I'll provide hints to help you out!")
    print("5. The game keeps track of your best scores for each difficulty level.")
    print("6. You can play multiple rounds until you decide to quit.")


def difficulty_level():
    print("\nPlease select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")

    while True:
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            return 10
        elif choice == '2':
            return 5
        elif choice == '3':
            return 3
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")


def give_hint(secret_number, guess):
    if abs(secret_number - guess) <= 10:
        return "You're close! Try again."
    else:
        return "You're far off! Keep trying"


def guessing_game(chances):
    secret_number = random.randint(1, 100)
    attempts = 0
    start_time = time.time()

    while attempts < chances:
        try:
            guess = int(input(f"\nAttempt {attempts + 1}/{chances}. Enter your guess: "))
            attempts += 1
            
            if guess < secret_number:
                print("🔽 Too low! Try again.")
            elif guess > secret_number:
                print("🔼 Too high! Try again.")
            else:
                endtime = time.time()
                elapsed_time = endtime - start_time
                print(f"✅ Congratulations! You've guessed the number {secret_number} in {attempts} attempts and {elapsed_time:.2f} seconds.")

                if chances not in high_scores or attempts < high_scores[chances]:
                    high_scores[chances] = attempts

                print(f"🏆 New high score for this difficulty: {attempts} attempts!")
                break

            hint = give_hint(secret_number, guess)
            print(hint)

        except ValueError:
            print("❌ Please enter a valid integer.")

    if attempts == chances and guess != secret_number:
        print(f"Sorry! You've used all your chances. The correct number was {secret_number}.")


def main():
    welcome_message()

    while True:
        chances = difficulty_level()
        guessing_game(chances)

        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            break


if __name__ == "__main__":
    main()