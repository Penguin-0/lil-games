#### Game Screen #####
screen whos_line_game_screen():
  add "BGs/nightskysepia.png"
  add drag_group

  textbutton "Main Menu" action ShowMenu("main_menu") xalign 0.0 yalign 1.0

### Game Label ###
label whos_line_game_start:
  call screen whos_line_game_screen()
  return  

### Python ###
init python:
  # Classes #
  class Line:
    def __init__(self, text, replay, destination, isComplete, isCorrect):
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
    line = Lines[dragged_name]
    line.isCorrect = dropped_on.drag_name == line.destination
    line.isComplete = True
    drag_group.add(ayane_line2) #TODO: Dynamically add
    drag_group.remove(dragged_items[0])

# Game Setup #
define Lines = {
    "ayane1": Line("I feel like it was just yesterday you were poking my arms and calling them squishy. Now, I could probably beat you to death blindfolded!", "firsttimedojo", "ayane_destination", False, False),
    "ayane2": Line("TODO", "none", "ayane_destination", False, False)
}

define ayane_line1 = Drag(d = Text(Lines["ayane1"].text, color="#E0E0E0"), xysize=(400, 400), drag_name = "ayane1", drag_raise = True, dragged = OnDragComplete, droppable = False)
define ayane_line2 = Drag(d = Text(Lines["ayane2"].text, color="#E0E0E0"), xysize=(400, 400), drag_name = "ayane2", drag_raise = True, dragged = OnDragComplete, droppable = False)

define x_offset = 300
define spacing = 300 
define ayane_destination = Drag(d = Image("ayanethumb1.png"), xysize=(250, 250), drag_name = "ayane_destination", xpos = x_offset, draggable = False)
define sana_destination = Drag(d = Image("sanathumb1.png"), xysize=(250, 250), drag_name = "sana_destination", xpos = x_offset + spacing, draggable = False)
define ami_destination = Drag(d = Image("amithumb1.png"), xysize=(250, 250), drag_name = "ami_destination", xpos = x_offset + (spacing * 2), draggable = False)
define maya_destination = Drag(d = Image("mayathumb1.png"), xysize=(250, 250), drag_name = "maya_destination", xpos = x_offset + (spacing * 3), draggable = False)

define drag_group = DragGroup(ayane_destination, sana_destination, ami_destination, maya_destination, ayane_line1)