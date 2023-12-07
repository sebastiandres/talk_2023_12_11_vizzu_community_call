import ipyvizzu

# Extend the ipyvizzu data class without any changes
class Data(ipyvizzu.Data):
    def __init__(self):
        # Call the constructor of the parent class
        super().__init__()