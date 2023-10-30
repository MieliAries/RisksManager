class ProcessDTO(object):

    def __init__(self, process_id, name, description):
        self.process_id = process_id
        self.name = name
        self.description = description


class RiskDTO(object):

    def __init__(self, risk_id, name, importance, description):
        self.risk_id = risk_id
        self.name = name
        self.importance = importance
        self.description = description
