import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from reporter.environment import SQL_DQLOG_URI
from reporter.emailing import get_recipients

Base = declarative_base()
engine = create_engine(SQL_DQLOG_URI, echo=False)
Session = sessionmaker(bind=engine)


class DqReport(Base):
    __tablename__ = 'dq_report'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<DqReport(name='{}')>".format(self.name)


class DqReportRun(Base):
    __tablename__ = 'dq_report_run'

    id = Column(Integer, primary_key=True)
    recipients = Column(String)
    report = Column(String)
    error_count = Column(Integer)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    dq_report_id = Column(Integer, ForeignKey(DqReport.id))
    dq_report = relationship(DqReport)

    def __repr__(self):
        return "<DqReportRun(dq_report_id='{}', recipients='{}', datetime_run='{}')>".format(
            self.dq_report_id,
            self.recipients,
            self.datetime_run,
        )


def log_report_run(name, start_datetime, end_datetime, recipients, report, error_count):
    session = Session()
    try:
        dq_report = get_or_create_report(session, name)
        dq_run = DqReportRun(
            start_datetime = start_datetime,
            end_datetime = end_datetime,
            dq_report = dq_report,
            report=report,
            error_count = error_count,
            recipients = '; '.join(get_recipients(recipients)),
        )
        session.add(dq_run)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_or_create_report(session, name):
    dq_report = session.query(DqReport).filter_by(name=name).first()
    if dq_report:
        return dq_report
    else:
        dq_report = DqReport(name=name)
        session.add(dq_report)
        return dq_report
