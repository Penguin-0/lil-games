#region Game Screens

screen lil_games_whos_line_game_start_screen():
    tag menu
    add "BGs/nightskysepia.png"
    add whos_line.drag_group
    textbutton "Main Menu" action ShowMenu("main_menu") xalign 0.0 yalign 1.0


screen lil_games_whos_line_game_end_screen():
    tag menu
    add "BGs/nightskysepia.png"

    textbutton "Main Menu" action ShowMenu("main_menu") xalign 0.0 yalign 1.0

#endregion Game Screens

#region Game Labels

label lil_games_whos_line_initialize():
    $ whos_line.initialize_game()
    show screen lil_games_whos_line_game_start_screen

    "Drag the text to the character who said it."

    call screen lil_games_whos_line_game_start_screen
  
label lil_games_whos_line_end:
    hide screen lil_games_whos_line_game_start_screen
    show screen lil_games_whos_line_game_end_screen

    "The end."

    call screen lil_games_whos_line_game_end_screen
#endregion Game Labels

#region Python
default whos_line.drag_group = DragGroup()
default whos_line.results = []
default whos_line.current_line_index = 0

init python in whos_line:
    import random
    import store

    def initialize_drag_group_empty():
        return store.DragGroup()

    class LineResult:
        def __init__(self, is_correct):
            self.is_correct = is_correct

    def initialize_game():
        global result
        global current_line_index
        result = []
        current_line_index = 0
        random.shuffle(selected_content["lines"])
        initialize_drag_group()
        drag_group.add(create_drag_line(selected_content["lines"][current_line_index]))

    def initialize_drag_group():
        global drag_group
        drag_group = store.DragGroup()
        for i, name in enumerate(get_distinct_names(selected_content)):
            drag_group.add(create_drag_destination(name, i))

    def create_drag_destination(name, iterator):
        return store.Drag(d = store.Image(f"{name.lower()}thumb1.png"), xysize=(250, 250), drag_name = f"{name}_destination", xpos = destination_x_offset + (destination_spacing * iterator), draggable = False)

    def create_drag_line(line):
        return store.Drag(d = store.Text(line["text"], color="#E0E0E0",xsize=500), drag_name = line["name"], drag_raise = True, dragged = on_drag_complete, droppable = False, xalign = 0.5, yalign = 0.5)

    def on_drag_complete(dragged_items, destination):
        if destination is None:
            return
        
        dragged_line = dragged_items[0]
        dragged_line.snap(destination.x, destination.y, 0.5)

        is_correct = current_line.name == selected_content["lines"][current_line_index]["name"]
        results.append(LineResult(is_correct))

        drag_group.remove(dragged_line)
        set_next_line()

    def set_next_line():
        global current_line_index
        if len(current_line_index >= len(selected_content["lines"])):
            end_of_game()
        else:
            current_line_index += 1
            drag_group.add(create_drag_line(selected_content["lines"][current_line_index]))

    def end_of_game():
        renpy.jump("whos_line_game_end")
        
    destination_x_offset = 200
    destination_spacing = 450
#endregion Python