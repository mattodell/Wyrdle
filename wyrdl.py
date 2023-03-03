import pathlib
import random
from string import ascii_letters
from rich.console import Console
from rich.theme import Theme

console = Console(width=40, theme=Theme({"warning": "red on yellow"}))

NUM_LETTER = 5
NUM_GUESSES = 6
WORDS_PATH = pathlib.Path(__file__).parent / "wordlist.txt"

def main():
    
    #Pre-Procees
    word = get_random_word(WORDS_PATH.read_text(encoding="utf-8").split("\n"))
    guesses = ["_" * NUM_LETTER] * NUM_GUESSES
    
    #Process (loop)
    for idx in range(NUM_GUESSES):
        refresh_page(headLine=f"Guess {idx + 1}")
        show_guesses(guesses, word)
        
        guesses[idx] = guess_word(previous_guesses=guesses[:idx])
        if guesses[idx] == word:
            break
    
    #Post-Process
    game_over(guesses, word, guessed_correctly=guesses[idx] == word)
    
def get_random_word(word_list):
    """Get a random 5 letter word from a list of strings

    Args:
        word_list (list): list of words

    Returns:
        string: random word for guessing
        
    >>> get_random_word(["snake", "worm", "it'll"])
    'SNAKE'
    """

    if words := [
        word.upper() 
        for word in word_list
        if len(word) == NUM_LETTER and all(letter in ascii_letters for letter in word)
    ]:
        return random.choice(words)
    else:
        console.print("No words of length 5 in word list", style="warning")
        raise SystemExit()

    return random.choice(words)

def guess_word(previous_guesses):
    guess = console.input("\nGuess word: ").upper()
    
    if guess in previous_guesses:
        console.print(f"You've already guessed {guess}.", style="warning")
        return guess_word(previous_guesses)
    
    if len(guess) != NUM_LETTER:
        console.print(f"You're guess must be {NUM_LETTER} letters", style="warning")
        return guess_word(previous_guesses)
    
    if any((invalid := letter) not in ascii_letters for letter in guess):
        console.print(f"Invalid letter: '{invalid}'. Please use English letters", style="warning")
        return guess_word(previous_guesses)
    
    return guess
    
def show_guess(guess, word):
    """Show the users guess on the terninal and classify all letters

    Args:
        guess (string): the guess
        word (string): the secret word
        
    >>> show_guess("CRANE", "SNAKE")
    Correct letters: A, E
    Misplaced letters: N
    Wrong letters: C, R
    """
    
    correct_letters = {
        letter for letter, correct in zip(guess, word) if letter == correct
    }
    misplaced_letters = set(guess) & set(word) - correct_letters
    wrong_letters = set(guess) - set(word)
    
    print("Correct letters:", ", ".join(sorted(correct_letters)))
    print("Misplaced letters:", ", ".join(sorted(misplaced_letters)))
    print("Wrong letters:", ", ".join(sorted(wrong_letters)))
    
def show_guesses(guesses, word):
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f"[{style}]{letter}[/]")
        console.print("".join(styled_guess), justify="center")
            
    
def game_over(guesses, word, guessed_correctly):
     refresh_page(headLine="Game Over")
     show_guesses(guesses, word)
     if guessed_correctly:
        console.print(f"\n[bold white on green]Correct, the word is {word}[/]")
     else:
        console.print(f"\n[bold white on red]Sorry, the word was {word}[/]")
     
def refresh_page(headLine):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headLine} :leafy_green:[/]\n")

if __name__ == "__main__":
    main()