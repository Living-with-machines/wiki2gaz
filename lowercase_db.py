import sqlite3

mapper = "resources/wikidata/index_enwiki-latest.db"

with sqlite3.connect(mapper) as conn:
    c = conn.cursor()
    c.execute("ALTER TABLE mapping ADD COLUMN lower_wikipedia_title")
    c.execute("UPDATE or IGNORE mapping SET lower_wikipedia_title = lower(wikipedia_title)")
    c.execute("DROP INDEX IF EXISTS idx_wikipedia_title")
    c.execute("CREATE INDEX idx_wikipedia_title ON mapping(wikipedia_title);")
    c.execute("CREATE INDEX lower_idx_wikipedia_title ON mapping(lower_wikipedia_title);")
