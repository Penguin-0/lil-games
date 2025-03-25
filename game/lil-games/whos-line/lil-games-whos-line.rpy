#### Game Screens #####
screen whos_line_game_start_screen():
  tag menu
  add "BGs/nightskysepia.png"
  add drag_group
  textbutton "Main Menu" action ShowMenu("main_menu") xalign 0.0 yalign 1.0
  

screen whos_line_game_end_screen():
  tag menu
  add "BGs/nightskysepia.png"

  $ y_position = 0.05
  for line in Lines:
    $ background_color = "#00ff001a" if line.isCorrect else "#ff00002d"
    textbutton line.key + " Replay" action Replay(line.replay, {}, False) ypos y_position xpos 0.1 background Solid(background_color)
    $ y_position += 0.1

  textbutton "Main Menu" action ShowMenu("main_menu") xalign 0.0 yalign 1.0
  

### Game Labels ###
label lil_games_whos_line_start(selected_lines):
  show screen whos_line_game_start_screen()
  $ InitializeDragGroup()

  "Drag the text to the character who said it."

  call screen whos_line_game_start_screen
    

label whos_line_game_end:
  hide screen whos_line_game_start
  show screen whos_line_game_end_screen
  $ ayane_text_result = GetResultText("ayane")
  $ sana_text_result = GetResultText("sana")
  $ ami_text_result = GetResultText("ami")
  $ maya_text_result = GetResultText("maya")

  "The end."
  "[ayane_text_result]"
  "[sana_text_result]"
  "[ami_text_result]"
  "[maya_text_result]"
  "Just kidding Selebus would get mad and hunt me down if I touched their affection."

  call screen whos_line_game_end_screen

### Python ###
init python:
  import json

  # Classes #
  class Line(object):
    def __init__(self, key=None, text=None, replay=None, destination=None, isComplete=False, isCorrect=False):
      self.key = key
      self.text = text
      self.replay = replay
      self.destination = destination
      self.isComplete = isComplete
      self.isCorrect = isCorrect

  # Functions #
  def OnDragComplete(dragged_items, dropped_on):
    if dropped_on is None:
      return

    dragged_items[0].snap(dropped_on.x, dropped_on.y, 0.5)

    dragged_name = dragged_items[0].drag_name
    line = next(line for line in Lines if line.key == dragged_name)
    line.isCorrect = dropped_on.drag_name == line.destination
    line.isComplete = True
    drag_group.remove(dragged_items[0])
    GetNextDragLine()

  #TODO: Get line randomly
  def GetNextDragLine():
    line = next((line for line in Lines if not line.isComplete), None)
    if line is None:
      renpy.jump("whos_line_game_end")
    
    drag_group.add(CreateDragLine(line))


  def CreateDragLine(line):
    return Drag(d = Text(line.text, color="#E0E0E0",xsize=500), drag_name = line.key, drag_raise = True, dragged = OnDragComplete, droppable = False, xalign = 0.5, yalign = 0.5)

  def CreateDragDestination(name, iterator):
    return Drag(d = Image(f"{name}thumb1.png"), xysize=(250, 250), drag_name = f"{name}_destination", xpos = x_offset + (spacing * iterator), draggable = False)

  def GetResultText(name):
        character_lines = [line for line in Lines if line.key.startswith(name)]
        correct_count = len([line for line in character_lines if line.isCorrect])
        total_count = len([line for line in character_lines])

        if correct_count == total_count:
            return f"You got {correct_count}/{total_count} of {name}'s lines correct! Her affection has increased by 100 across all saves."
        elif correct_count == 1:
            return f"You got {correct_count}/{total_count} of {name}'s lines correct. Her affection has stayed the same."
        else:
            return f"You got {correct_count}/{total_count} of {name}'s lines correct... Her affection has decreased by 100 across all saves. She's crying!"

  def ReadJsonFiles():
    with open("game/lil-games/whos-line/content-1.json", "r") as f:
      data = json.load(f)

    lines = [Line(**item) for item in data]
    return lines

  def InitializeDragGroup():
    return DragGroup(ayane_destination, sana_destination, ami_destination, maya_destination, CreateDragLine(Lines[0]))

# Game Setup #
define Lines = ReadJsonFiles()
default drag_group = InitializeDragGroup()

define x_offset = 200
define spacing = 450 
define ayane_destination = CreateDragDestination("ayane", 0)
define sana_destination = CreateDragDestination("sana", 1)
define ami_destination = CreateDragDestination("ami", 2)
define maya_destination = CreateDragDestination("maya", 3)

# default drag_group = DragGroup(ayane_destination, sana_destination, ami_destination, maya_destination, CreateDragLine(Lines[0]))