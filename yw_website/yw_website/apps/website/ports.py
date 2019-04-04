class Ports:

    def __init__(self):
        self.id = None
        self.name = None
        self.is_inport = None
        self.is_outport = None
        self.data_id = None
        self.on_program_block_id = None
        self.run_id = None
    
    def __str__(self):
        s = "{}: id: {}, is_inport: {}, is_outport: {}, on_program_block_id: {}"
        return s.format(self.name, self.id, self.is_inport, self.is_outport, self.on_program_block_id)
