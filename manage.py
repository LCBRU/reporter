#!/usr/bin/env python

import os
from migrate.versioning.shell import main
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    main(repository="migrations", url=os.environ["SQL_DQLOG_URI"], debug="False")
