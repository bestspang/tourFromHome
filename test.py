from models.node import NodeModel
import pandas as pd

print([node.json() for node in NodeModel.query.all()])
