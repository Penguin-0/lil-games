screen whos_line_selection():
    tag menu
    add "BGs/nightskysepia.png"

    vbox:
        spacing 40

        for content in whos_line.content_list:
            python:
                names = whos_line.get_distinct_names(content)
                name_display = whos_line.get_name_display_text(names)
            vbox:
                textbutton content["displayText"] action Call("lil_games_whos_line_start", content)
                text name_display size 18 color "#888888"
                text "Created by: [content['createdBy']]" size 18 color "#888888"

    textbutton "Main Menu" action ShowMenu("main_menu") xalign 0.0 yalign 1.0

init python in whos_line:
    import json
    import glob

    def load_json_content():
        data_list = []
        json_files = glob.glob("game/lil-games/whos-line/*.json")

        for file_path in json_files:
            if "content-example.json" in file_path:
                continue

            if "content-1.json" in file_path:
                continue

            with open(file_path, "r") as f:
                data_list.append(json.load(f))

        return data_list

    def get_distinct_names(content):
        names = []

        for line in content["lines"]:
            name = line.get("name", "").capitalize()
            if name not in names and len(names) < 4:
                names.append(name)

        return names
    
    def get_name_display_text(names):
        if len(names) == 1:
            return f"Featuring: {names[0]}"

        return f"Featuring: {', '.join(names[:-1])}, and {names[-1]}"
        
    content_list = load_json_content()

