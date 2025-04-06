#region Game Screens

screen lil_games_whos_line_game_start_screen():
    tag menu
    add "BGs/nightskysepia.png"
    add whos_line.drag_group
    textbutton "Main Menu" action ShowMenu("main_menu") xalign 0.0 yalign 1.0


screen lil_games_whos_line_game_end_screen():
    tag results_table
    add "BGs/nightskysepia.png"

    frame:
        style_prefix "results"
        xfill True
        yfill True
        padding (20, 20)

        vbox:
            spacing 20
            xfill True

            text "Results" size 40 xalign 0.5

            viewport:
                draggable True
                mousewheel True
                scrollbars "vertical"
                xfill True

                # TODO: Surely there is a better way than looping multiple times
                hbox:
                    spacing 20
                    vbox:
                        text "Line #" size 26
                        for result in whos_line.results:
                            text str(result.line_index + 1) size 26

                    vbox:
                        text "Your Answer" size 26
                        for result in whos_line.results:
                            text result.player_answer size 26
                    vbox:
                        text "Correct Answer" size 26
                        for result in whos_line.results:
                            text result.correct_answer size 26
                    vbox:
                        text "Answer Text" size 26
                        for result in whos_line.results:
                            $ line = whos_line.selected_content["lines"][result.line_index]
                            text line["text"][:75] + ("..." if len(line["text"]) > 75 else "") size 26
                    vbox:
                        text "Replay" size 26
                        for result in whos_line.results:
                            $ line = whos_line.selected_content["lines"][result.line_index]
                            text line["replay-label"] size 26
                    
               
                    # for result in whos_line.results:
                    #     $ line = whos_line.selected_content["lines"][result.line_index]
                    #     $ bg_color = "#90fbb288" if result.line_index % 2 == 0 else "#ffffff86"

                    #     # Wrap the row in a frame with the background color
                    #     frame:
                    #         background Solid(bg_color)
                    #         xfill True
                    #         ysize 50  # Adjust the height of each row, as needed

                    #         grid 5 len(whos_line.results):
                    #             spacing 20
                    #             text str(result.line_index + 1)
                    #             text result.player_answer
                    #             text result.correct_answer
                    #             text line["text"][:100] + ("..." if len(line["text"]) > 100 else "") size 24
                    #             text line["replay-label"]

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
        def __init__(self, correct_answer, player_answer, line_index):
            self.correct_answer = correct_answer
            self.player_answer = player_answer
            self.line_index = line_index
        @property
        def is_correct(self):
            return self.correct_answer == self.player_answer

    def initialize_game():
        global result
        global current_line_index
        result = []
        current_line_index = 0
        initialize_drag_group()
        random.shuffle(selected_content["lines"])
        drag_group.add(create_drag_line(selected_content["lines"][current_line_index]))

    def initialize_drag_group():
        global drag_group
        drag_group = store.DragGroup()
        for i, name in enumerate(get_distinct_names(selected_content)):
            drag_group.add(create_drag_destination(name, i))

    def create_drag_destination(name, iterator):
        return store.Drag(d = store.Image(f"{name.lower()}thumb1.png"), xysize=(250, 250), drag_name = f"{name}_destination", xpos = destination_x_offset + (destination_spacing * iterator), draggable = False)

    def create_drag_line(line):
        return store.Drag(d = store.Text(line["text"], color="#E0E0E0",xsize=500), drag_name = f"{line['name']}_{current_line_index}", drag_raise = True, dragged = on_drag_complete, droppable = False, xalign = 0.5, yalign = 0.5)

    def on_drag_complete(dragged_items, destination):
        if destination is None:
            return
        
        dragged_line = dragged_items[0]
        dragged_line.snap(destination.x, destination.y, 0.5)

        correct_answer = selected_content["lines"][current_line_index]["name"]
        player_answer = dragged_line.drag_name
        results.append(LineResult(correct_answer, player_answer, current_line_index))

        drag_group.remove(dragged_line)
        set_next_line()

    def set_next_line():
        global current_line_index
        current_line_index += 1
        
        if (current_line_index >= len(selected_content["lines"])):
            end_of_game()
        else:
            drag_group.add(create_drag_line(selected_content["lines"][current_line_index]))

    def end_of_game():
        renpy.jump("lil_games_whos_line_end")
        
    destination_x_offset = 200
    destination_spacing = 450
#endregion Python