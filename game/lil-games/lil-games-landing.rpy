screen lil_games_landing():
    tag menu
    add "BGs/nightskysepia.png"

    vbox:
        spacing 40

        vbox:
            textbutton "Who's Line" action ShowMenu("whos_line_selection")
            text "Given a line from Lessons in Love, can you determine who said it?" color "#848986"
        vbox:
            textbutton "Coming Eventually"
            text "Battle wizards and climb the ranks in this rock-paper-scissors-like game." color "#848986"

    textbutton "Main Menu" action ShowMenu("main_menu") xalign 0.0 yalign 1.0

