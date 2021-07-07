from lokiconnector import LokiConnector
from script_cleaner import ScriptCleaner

global line_id_counter, scene_counter


def enter_info_into_db(episode: ScriptCleaner, loki: LokiConnector):
    print("Opening Connection \t.... ")

    try:
        print("ENTERING CHARACTERS\t....", end="   \t\t\t")

        # characters
        for char in episode.characters:
            loki.insert_char(char)

        print("..... INPUTTED CHARACTERS")
        print("ENTERING PLACES\t\t....", end="   \t\t\t")

        # places
        for place_id, place_name in episode.places.items():
            loki.insert_place(place_id, place_name)

        print("..... INPUTTED PLACES")
        print("ENTERING SCENES\t\t....", end="   \t\t\t")

        # scenes
        for scene_id in episode.structure["scenes"].keys():
            loki.insert_scenes(scene_id)

        print("..... INPUTTED SCENES")
        print("ENTERING SCENES + PLACES....", end="   \t\t\t")

        # scenes + places
        for scene_id, list_of_place_ids in episode.structure["scenes"].items():
            for place_id in list_of_place_ids:
                loki.insert_place_scene(scene_id, place_id)

        print("..... INPUTTED SCENES + PLACES")
        print("ENTERING EXPRESSIONS\t....", end="  \t\t\t")

        # expressions
        for char in episode.characters:
            char_id = loki.character_id(char)

            for scene_id, expression_list in episode.structure[char]["expressions"].items():
                for expression in expression_list:
                    loki.insert_line(line_id_counter, expression, "EXPRESSION", char_id, scene_id)
                    line_id_counter += 1

        print("..... INPUTTED EXPRESSIONS")
        print("ENTERING ACTIONS\t....", end="   \t\t\t")

        # actions
        for char in episode.characters:
            char_id = loki.character_id(char)
            for scene_id, action_list in episode.structure[char]["actions"].items():
                for action in action_list:
                    loki.insert_line(line_id_counter, action, "ACTION", char_id, scene_id)
                    line_id_counter += 1

        print("..... INPUTTED ACTIONS")
        print("ENTERING DIALOGUE\t....", end="   \t\t\t")

        # dialogue
        for char in episode.characters:
            char_id = loki.character_id(char)
            for scene_id, dialogue_list in episode.structure[char]["dialogue"].items():
                for dialogue in dialogue_list:
                    loki.insert_line(line_id_counter, dialogue, "DIALOGUE", char_id, scene_id)
                    line_id_counter += 1

        print("..... INPUTTED DIALOGUE")
        print("ENTERING SWITCHES\t....", end="   \t\t\t")

        for char in episode.characters:
            char_id = loki.character_id(char)
            for scene_id, switch_id_list in episode.structure[char]["switches"].items():
                for switch_pair in switch_id_list:
                    old_char_id = loki.character_id(switch_pair[0])
                    loki.insert_switch(scene_id, old_char_id, char_id)

        print("..... INPUTTED SWITCHES")
        print("\nEntered Everything ... Closing Connection")

    except Exception as e:
        print("exception encountered:", end=" ")
        print(e)
        print("\n..... Closing Connection")

if __name__ == "__main__":
    global scene_counter, line_id_counter
    scene_counter = 1


    ep1 = ScriptCleaner("https://transcripts.fandom.com/wiki/Glorious_Purpose")
    print("cleaned episode 1")
    ep2 = ScriptCleaner("https://transcripts.fandom.com/wiki/The_Variant")
    print("cleaned episode 2")
    ep3 = ScriptCleaner("https://transcripts.fandom.com/wiki/Lamentis")

    print("cleaned episode 3")
    ep4 = ScriptCleaner("https://transcripts.fandom.com/wiki/The_Nexus_Event")

    print("cleaned episode 4")


    line_id_counter = 1

    loki = LokiConnector()
    loki.exec_sql_file()

    print("\t\t\t\tStarted Episode 1\t\t")
    enter_info_into_db(ep1, loki)
    print("\t\t\t\tEnded Episode 1\t\t\t")

    print("\t\t\t\tStarted Episode 2\t\t")
    enter_info_into_db(ep2, loki)
    print("\t\t\t\tEnded Episode 2\t\t\t")

    print("\t\t\t\tStarted Episode 3\t\t")
    enter_info_into_db(ep3, loki)
    print("\t\t\t\tEnded Episode 3\t\t\t")

    print("\t\t\t\tStarted Episode 4\t\t")
    enter_info_into_db(ep4, loki)
    print("\t\t\t\tEnded Episode 4\t\t\t")

    loki.close()


