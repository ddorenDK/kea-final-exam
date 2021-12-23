
class epd:

    def get_sum(self):
        return self.A1 

    def __init__(self, name, A1, A2, A3, A4, A5, B1, B2, B3, B4, B5, B6, B7, C1, C2, C3, C4, D):
        self.name = name
        #A stage
        self.A1 = A1 #Raw material supply
        self.A2 = A2 #Transport
        self.A3 = A3 #Manufacturing
        self.A4 = A4 #Transport
        self.A5 = A5 #Construction installation process

        #B stage | Use Stage
        self.B1 = B1 #
        self.B2 = B2 #
        self.B3 = B3 #
        self.B4 = B4 #
        self.B5 = B5 #
        self.B6 = B6 #
        self.B7 = B7 #

        #C stage
        self.C1 = C1 #Demolition/Deconstruction
        self.C2 = C2 #Transport
        self.C3 = C3 #Waste Processing
        self.C4 = C4 #Disposal

        #D stage | Benefits beyond the system boundary
        self.D = D 

        #PWD Sum 
        #TODO
        #Find a way to calculate this in a nicer manner / sanitize the input upon object creation
        self.sum = A1 + A2 + A3 + A4 + A5 + B1 + B2 + B3 + B4 + B5 + B6 + B7 + C1 + C2 + C3 + C4 + D

        #List of the manufacturers
        #TODO 
        #Find a way to extract and get manufacturers
        self.manufacturers = []





        