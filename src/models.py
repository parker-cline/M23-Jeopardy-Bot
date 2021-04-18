from __init__ import metadata, engine
from sqlalchemy import Table

clues = Table("clues", metadata, autoload_with=engine)
airdates = Table("airdates", metadata, autoload_with=engine)
documents = Table("documents", metadata, autoload_with=engine)
categories = Table("categories", metadata, autoload_with=engine)
classifications = Table("classifications", metadata, autoload_with=engine)