# lil-games: a collection of Lessons in Love minigames

## Minigames
| Name | Description |
|------------|-----------------------------------------------------|
| Who's Line | Given a line from Lessons in Love, can you determine who said it?|

## Usage
1. From the Main Menu screen, click the button in the top left to launch the minigame.
   ![image](https://github.com/user-attachments/assets/c8f5024b-1895-4300-85d3-f1f1957d20cb)

## Installation
1. Download the Source Code for the [latest release](https://github.com/Penguin-0/lil-games/releases).
2. Unzip and drag the game folder into your Lessons in Love folder.

## Removal
1. Navigate to your Lessons in Love game folder.
2. Delete any files starting with lil-games.
3. In screens.rpy remove the following lines.
   ```
   # LiL Games
   if main_menu:
      textbutton "Who's Line" action Jump("whos_line_game_start") xalign 0.98 yalign 0.02 background Solid("#000000B3")
   ```
