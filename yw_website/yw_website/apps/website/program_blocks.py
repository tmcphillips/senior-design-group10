class ProgramBlocks:

    def __init__(self):
        self.name = None
        self.programblock_id = None
        self.id = None
        self.in_program_block_id = None
        self.direct_descendents = []
        self.data_objs = []
    
    def __str__(self):
        return "%s: id: %d, programblock_id: %d, in program block: %d" % (self.name, self.id, self.programblock_id, self.in_program_block_id)
