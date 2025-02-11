"""

"""

from __future__ import annotations
from .._auto import auto
from ._with_exit_stack import with_exit_stack


def summary(
    arg,
    *args,
    **kwargs,
) -> str:
    is_pandas = isinstance(arg, auto.pd.DataFrame)
    if is_pandas:
        return summary_pandas_DataFrame(arg, *args, **kwargs)

    is_sqlite3 = any([
        isinstance(arg, auto.sqlite3.Connection),
        all([
            hasattr(arg, 'execute'),
            hasattr(arg, 'commit'),
        ]),
    ])
    if is_sqlite3:
        return summary_sqlite3_Connection(arg, *args, **kwargs)

    assert False, type(arg)


def summary_pandas_DataFrame(
    df,
    /,
) -> str:
    if len(df) > 3:
        df = df.sample(3, random_state=1337)

    df = df.T

    with auto.warnings.catch_warnings():
        auto.warnings.simplefilter('ignore', FutureWarning)

        df = df.applymap(str)
        df = df.applymap(lambda s: auto.textwrap.shorten(s, 72//2))

    return df.to_markdown()


@with_exit_stack
def summary_sqlite3_Connection(
    conn,
    /,
    name: str | None = None,
    *,   enter,
) -> str:
    the_name = name

    enter( auto.contextlib.redirect_stdout(
        (io := auto.io.StringIO()),
    ) )

    df = auto.pd.read_sql(auto.self.lib.SQLQuery(r'''
        PRAGMA database_list
    '''), conn)

    df.set_index([
        'seq',
    ], inplace=True)
    df.sort_index(inplace=True)

    first = True
    for _seq, row in df.iterrows():
        schema_name = row['name']

        df = auto.pd.read_sql(auto.self.lib.SQLQuery(r'''
            SELECT *
            FROM {{ schema_name |tosqlref }}.sqlite_master
        ''', schema_name=schema_name), conn)

        df.set_index([
            'type',
            'name',
        ], inplace=True)

        df.sort_values([
            'rootpage',
        ], inplace=True)

        for (type, name), row in df.iterrows():
            if the_name is not None and name != the_name:
                continue

            if type == 'table':
                table_name = row['tbl_name']

                if table_name.startswith('sqlite_'):
                    continue
                if table_name.startswith('sqlean_'):
                    continue

                count ,= conn.execute(auto.self.lib.SQLQuery(r'''
                    SELECT
                        MAX(ROWID)
                    FROM {{ schema_name |tosqlref }}.{{ table_name |tosqlref }}
                    LIMIT 1
                ''', schema_name=schema_name, table_name=table_name)).fetchone()

                assert count is not None, (schema_name, table_name)

                rowids = auto.random.Random(1337).sample(range(1, count + 1), min(count, 3))

                df = auto.pd.read_sql(auto.self.lib.SQLQuery(r'''
                    SELECT
                        *
                        , ROWID AS rowid
                    FROM {{ schema_name |tosqlref }}.{{ table_name |tosqlref }}
                    WHERE ROWID IN (
                        {%- set sep = joiner(", ") %}
                        {%- for rowid in rowids %}
                        {{ sep() }}{{ rowid |tosqlint }}
                        {%- endfor %}
                    )
                ''', schema_name=schema_name, table_name=table_name, rowids=rowids), conn)

                df.set_index([
                    'rowid',
                ], inplace=True)
                df.sort_index(inplace=True)

                text = summary(df)

                ref = auto.self.lib.SQLQuery(r'''
                    {{ schema_name |tosqlref }}.{{ table_name |tosqlref }} ({{ count }})
                ''', schema_name=schema_name, table_name=table_name, count=count)
                ref = ref.strip()

                text = auto.re.sub(r'''
                    \|\s+\|
                ''', f'| {ref} |', text, count=1, flags=auto.re.VERBOSE)

                if not first:
                    print()
                    print('---')
                    print()
                else:
                    first = False

                print(text)

            elif type == 'index':
                print(row['sql'])
                if not first:
                    print()
                    print('---')
                    print()
                else:
                    first = False
                print()

    return io.getvalue()