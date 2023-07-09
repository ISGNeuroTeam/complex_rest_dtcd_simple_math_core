from typing import Dict


class Edge:
    sourcePort: str
    sourceNode: str
    targetPort: str
    targetNode: str

    def __init__(self, data: Dict):
        self.sourceNode = data['sourceNode']
        self.sourcePort = data['sourcePort']
        self.targetNode = data['targetNode']
        self.targetPort = data['targetPort']
