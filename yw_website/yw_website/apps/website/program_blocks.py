class ProgramBlocks:

    def __init__(self):
        self.name = None
        self.program_block_id = None
        self.id = None
        self.in_program_block_id = None
        self.direct_descendents = []
        self.data_objs = []
        self.in_ports = []
        self.out_ports = []
    
    def __str__(self):
        s =  "{}: id: {}, programblock_id: {}, in program block: {}" 
        return s.format(self.name, self.id, self.program_block_id, self.in_program_block_id)

