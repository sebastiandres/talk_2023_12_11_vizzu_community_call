import pandas as pd
from ipyvizzu import Chart as Chart_old
from ipyvizzu import Data as Data_old
from ipyvizzu import Config, DisplayTarget
from ipyvizzustory import Story, Step
from ipyvizzustory import Slide as Slide_old


class Chart:

    def __init__(self):
        self.actions = []
        self.slide_number = 0

    def add_slide(self, slide):
        #from IPython import embed; embed()
        # Check if slide has all the required elements
        build_dict = slide.config.build()["config"]
        channels = build_dict["channels"]
        data = self.__get_data__()
        known_columns = []
        # Get the known columns
        for element in data['series']:
            known_columns.append(element['name'])
        # Check if all the required columns are known
        element_status = {}
        for _, element in channels.items():
            if type(element)==str:
                element_status[element] = element in known_columns
            elif type(element)==list:
                for subelement in element:
                    element_status[subelement] = subelement in known_columns
            else:
                raise Exception("Unknown type - could not process the element")
        # Check if all the elements are known
        verification = all(element_status.values())        
        if not verification:
            unknown_elements = [element for element in element_status if not element_status[element]]
            unknown_elements_str = ", ".join(unknown_elements)
            raise Exception(f"Column(s) {unknown_elements_str} not in the data columns")
        else:
            self.slide_number += 1
            print(f"Adding slide {self.slide_number}")
            self.actions.append({"content": slide, "action": "add_slide"})

    def set_data(self, data):
        print("Setting data")
        self.actions.append({"content": data, "action": "set_data"})
    
    def add_record(self, dict_of_values):
        # Should alert if not all the columns are met
        print("Adding record")
        self.actions.append({"content": dict_of_values, "action": "add_record"})

    def add_records(self, list_of_dict_of_values):
        for dict_of_values in list_of_dict_of_values:
            self.add_record(dict_of_values)

    ###########################################################################
    # Story chart methods
    ###########################################################################
    def interact(self, width="800px", height="600px"):
        story_chart = self.__create_story_chart(width, height)
        story_chart.play()

    def __get_data__(self):
        """Returns the data stored in the actions"""
        for action in self.actions:
            if action["action"]=="set_data":
                data = action["content"]
                return data

    def __create_story_chart(self, width="100%", height="100%"):
        """Creates the vizzu animation chart on spot using the stored actions"""
        data = self.__get_data__()
        story = Story(data=data)
        # Iterate over the actions and add them to the story
        for action in self.actions:
            if action["action"] == "add_slide":
                config = action["content"].config
                style = action["content"].style
                slide = Slide_old(Step(config), )
                story.add_slide(slide)
            elif action["action"] == "set_data":
                pass
                #data = action["content"]
            elif action["action"] == "add_record":
                pass
                #record = action["content"]
            elif action["action"] == "add_records":
                pass
                #records = action["content"]
            else:
                raise Exception("Unknown action type")
        # Return the obtained story
        return story

    ###########################################################################
    # Animation chart methods
    ###########################################################################
    def __create_animation_chart(self, width="800px", height="600px"):
        """Creates the vizzu animation chart on spot using the stored actions"""
        data = None
        chart = Chart_old(width=width, height=height, display=DisplayTarget.MANUAL)
        for action in self.actions:
            if action["action"] == "add_slide":
                config = action["content"].config
                style = action["content"].style
                chart.animate(data, config)
            elif action["action"] == "set_data":
                data = action["content"]
                chart.animate(data)
            elif action["action"] == "add_record":
                record = action["content"]
                data.add_record(record)
            elif action["action"] == "add_records":
                records = action["content"]
                data.add_records(records)
            else:
                raise Exception("Unknown action type")
        return chart

    def show(self, width="800px", height="600px"):
        animated_chart = self.__create_animation_chart(width, height)
        animated_chart.show()

    def to_html(self, filename="", width="100%", height="100%"):
        animated_chart = self.__create_animation_chart(width, height)
        chart_html = animated_chart._repr_html_()
        if filename != "":
            with open(filename, "w") as file:
                file.write(chart_html)
        else:
            return chart_html
    
    def to_gif(self, filename, width="100%", height="100%"):
        print("Not implemented")

    def to_mp4(self, filename, width="100%", height="100%"):
        print("Not implemented")