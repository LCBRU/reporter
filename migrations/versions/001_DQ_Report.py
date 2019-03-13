from sqlalchemy import MetaData, Table, Column, Integer, NVARCHAR, Index, ForeignKey


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    t = Table(
        "dq_report",
        meta,
        Column("id", Integer, primary_key=True),
        Column("name", NVARCHAR(500), nullable=False),
    )
    t.create()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    t = Table("dq_report", meta, autoload=True)
    t.drop()