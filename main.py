from typing import Tuple, Set

import pandas as pd

RESULTS_PATH = 'data/results.csv'

TOP_8 = ['Dave', 'Guy', 'Tom', 'Jack', 'Joel', 'Will Sanders', 'Will Perkin', 'Hamish']


def _derive_n_wins_n_losses(player: str) -> Tuple[int, int]:
    win_loss_series = df.apply(lambda row: _derive_win_loss_val(row, player), axis=1)

    win_loss_counts = win_loss_series.value_counts()
    n_wins = win_loss_counts[1]
    n_losses = win_loss_counts[-1]

    return n_wins, n_losses


def _derive_win_loss_val(row: pd.Series, player: str) -> int:
    if _player_did_not_play(row, player):
        return 0
    else:
        if _player_on_winning_team(row, player):
            return 1
        else:
            return -1


def _player_did_not_play(row: pd.Series, player: str) -> bool:
    return (player != row['team 1 player 1'] and 
            player != row['team 1 player 2'] and
            player != row['team 2 player 1'] and
            player != row['team 2 player 2'])


def _player_on_winning_team(row: pd.Series, player: str) -> bool:
    if row['winning team'] == 1:
        return (player == row['team 1 player 1'] or
                player == row['team 1 player 2'])
    else:
        return (player == row['team 2 player 1'] or
                player == row['team 2 player 2'])


def _derive_bageled_teams(row: pd.Series) -> Set[int]:
    bagelled_teams = set()

    for set_no in range(1, 4):
        if row[f'team 1 set {set_no}'] == 0 and row[f'team 2 set {set_no}'] == 6:
            bagelled_teams.add(1)
        if row[f'team 1 set {set_no}'] == 6 and row[f'team 2 set {set_no}'] == 0:
            bagelled_teams.add(2)

    return bagelled_teams


df = pd.read_csv(RESULTS_PATH)

n_games = len(df)
print(f'{n_games} games played.')

n_days_played = df['date'].nunique()
print(f'Played on {n_days_played} days.')

for player in TOP_8:
    n_wins, n_losses = _derive_n_wins_n_losses(player)
    print(f'{player}: {n_wins} wins, {n_losses} losses.')

df['bageled_teams'] = df.apply(lambda row: _derive_bageled_teams(row), axis=1)
