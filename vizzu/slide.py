from ipyvizzu import Config

class Slide:

    def __init__(self, *args, **kwargs):
        if len(args)>0:
            raise Exception("All arguments must be named. Use 'name=value' syntax.")
        # Process the arguments
        if "graph_type" in kwargs:
            graph_type = kwargs["graph_type"]
            del kwargs["graph_type"]
            # Pass to the correct config class
            if graph_type=="pie":
                try:
                    config = Config.pie(kwargs)
                except:
                    raise Exception("Invalid arguments for pie graph")
            else:
                raise Exception("Unknown graph type")
        else:
            config = Config(kwargs)
        # Store the procesed arguments
        self.config = config
        self.style = {}

    def config():
        return self.config

    def style():
        return self.style

    def __repr__(self):
        return "Slide:\nconfig=\n"+repr(self.config)+"\nstyle=\n"+repr(self.style)