import os
DATABASE = os.environ['DATABASE_NAME']

from db.api import DBConnection
from db.utils import get_df_from_batch
from db.tables import *

if DATABASE == 'redshift':
    from db.loaders.redshift_loader import transit_insert_to_redshift
if DATABASE == 'clickhouse':
    from db.loaders.clickhouse_loader import insert_to_clickhouse
if DATABASE == 'pg':
    from db.loaders.postgres_loader import insert_to_postgres
if DATABASE == 'bigquery':
    from db.loaders.bigquery_loader import insert_to_bigquery
    from bigquery_utils.create_table import create_tables_bigquery
if DATABASE == 'snowflake':
    from db.loaders.snowflake_loader import insert_to_snowflake


# create tables if don't exist
try:
    db = DBConnection(DATABASE)
    if DATABASE == 'pg':
        create_tables_postgres(db)
    if DATABASE == 'clickhouse':
        create_tables_clickhouse(db)
    if DATABASE == 'snowflake':
        create_tables_snowflake(db)
    if DATABASE == 'bigquery':
        create_tables_bigquery()
    if DATABASE == 'redshift':
        create_tables_redshift(db)
    db.engine.dispose()
    db = None
except Exception as e:
    print(repr(e))
    print("Please create the tables with scripts provided in "
          "'/sql/{DATABASE}_sessions.sql' and '/sql/{DATABASE}_events.sql'")


def insert_batch(db: DBConnection, batch, table, level='normal'):

    if len(batch) == 0:
        return
    df = get_df_from_batch(batch, level=level)

    if db.config == 'redshift':
        transit_insert_to_redshift(db=db, df=df, table=table)
        return

    if db.config == 'clickhouse':
        insert_to_clickhouse(db=db, df=df, table=table)

    if db.config == 'pg':
        insert_to_postgres(db=db, df=df, table=table)

    if db.config == 'bigquery':
        insert_to_bigquery(df=df, table=table)

    if db.config == 'snowflake':
        insert_to_snowflake(db=db, df=df, table=table)

