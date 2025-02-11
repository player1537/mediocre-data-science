"""

"""

from __future__ import annotations
from .._auto import auto
from ._with_exit_stack import with_exit_stack


@with_exit_stack
def df2sql(
    df: auto.pd.DataFrame,
    name: str,
    conn: auto.sqlite3.Connection,
    *,   enter,
    batch: int = 10_000,
    verbose: bool = True,
    index: bool = True,
    if_exists: str = 'replace',
    schema: str | None = None,
    tmp_tbl_name: str = (
        '4Y0F3DV4D0ZVJF1X2VPE6CXRAJ'
    ),
):
    count = len(df)

    it = (
        (beg, min(count, beg + batch))
        for beg in range(0, len(df), batch)
    )

    if verbose:
        pbar = enter( auto.tqdm.auto.tqdm(
            total=len(df),
            unit='row',
            unit_scale=True,
        ) )
    
    if schema is not None:
        the_tbl_name = tmp_tbl_name
    else:
        the_tbl_name = name

    for i, (beg, end) in enumerate(it):
        if verbose:
            pbar.update(end - beg)

        df.iloc[beg:end].to_sql(
            the_tbl_name,
            conn,
            if_exists=(
                if_exists
            ) if i == 0 else (
                'append'
            ),
            index=index,
        )

    conn.commit()
    
    if schema is not None:
        conn.execute(auto.self.lib.SQLQuery(r'''
            CREATE TABLE
                {{ schema |tosqlref }}.{{ name |tosqlref }}
            
            AS
            
            SELECT
                *
            FROM {{ tmp_tbl_name |tosqlref }}
        ''', **locals()))
        
        conn.execute(auto.self.lib.SQLQuery(r'''
            DROP TABLE {{ tmp_tbl_name |tosqlref }}
        ''', **locals()))
        
        conn.commit()
