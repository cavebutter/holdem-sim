# holdem_sim

Get probablilites, odds, and win expectations for holdem hands

## Installation

```bash
$ pip install holdem_sim
```

## Usage

### Holdem Percentage Odds and Ratios Calculator

Command line application (for now).  There are two flows:
* Single Player Monte Carlo Simulation
* Multiplayer Win Expectancy



#### Single Player Monte Carlo Simulation
Tell the application your hole cards and board as flop, turn, and river.  The application will run 100,000 
simulations of that hand and return the percentage and odds of improving to any poker hand.
#### Usage
`python holdem.py -c Rs Rs -f Rs Rs Rs -t Rs Rs -r Rs` where `Rs` stands for Rank and suit of a card.  

Card ranks must be 2-9, T, J, K, Q, A.  Ranks are case sensitive.
Suits are c, d, h, s.  Suits are case sensitive.

`-c` is the flag for your hole cards and to indicate Single Player mode.  These must be separated by a space.

`-f` or `--flop` is the optional flag for flop.  Three cards separated by a space.

`-t` or `--turn` is the optional flag for turn.  One card.

`-r` or `--river` is the optional flag for river.  One card.

#### Sample Output
![image](single_player.png)

#### Multiplayer Win Expectancy
Tell the application your hole cards and board (as flop, turn, and river) and total number of players in the hand.

`-m` is the flag to indicate multiplayer mode.  The hero's hole cards (2) are required arguments.

`-p`  or `--players` is the flag to indicate the total number of players in the hand. This is a required argument, maximum of 6 players.

`--two` through `--six` are optional flags to indicate the hands of players other than the hero.  2 cards each.

Returns win expectancy for the hero.
## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`holdem_sim` was created by Jay Cohen. It is licensed under the terms of the MIT license.

## Credits

`holdem_sim` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
