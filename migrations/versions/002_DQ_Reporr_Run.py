from sqlalchemy import MetaData, Table, Column, Text, Integer, DateTime, NVARCHAR, Index, ForeignKey


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    dq_report = Table("dq_report", meta, autoload=True)

    t = Table(
        "dq_report_run",
        meta,
        Column("id", Integer, primary_key=True),
        Column(
            "dq_report_id",
            Integer,
            ForeignKey(dq_report.c.id),
            index=True,
            nullable=False,
        ),
        Column("recipients", NVARCHAR(2000), nullable=False),
        Column("error_count", Integer),
        Column("report", Text, nullable=False),
        Column("start_datetime", DateTime, nullable=False),
        Column("end_datetime", DateTime, nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    t = Table("dq_report_run", meta, autoload=True)
    t.drop()