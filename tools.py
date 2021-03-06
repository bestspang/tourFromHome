import pathlib
import sqlite3
import pandas as pd

DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("wind-data.db").resolve()


def get_wind_data(start, end):
    """
    Query wind data rows between two ranges

    :params start: start row id
    :params end: end row id
    :returns: pandas dataframe object
    """
    # df = pd.read_sql(sql = db.session.query(NodeModel).with_entities(NodeModel.temp,
    #                                     NodeModel.timestamp).statement,
    #                                     con = db.session.bind)
    con = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT Speed, SpeedError, Direction FROM Wind WHERE rowid > "{start}" AND rowid <= "{end}";'
    df = pd.read_sql_query(statement, con)
    return df
