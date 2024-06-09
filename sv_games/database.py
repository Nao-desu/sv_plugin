import sqlite3, os
import asyncio
from ..info import MOUDULE_PATH
from os.path import join

dbpath = join(MOUDULE_PATH,"data","sv_games.db")

#答对次数记录数据库
class GameRecord:
    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._create_table()

    def connect(self):
        return sqlite3.connect(self.path)
    
    def _create_table(self):
        with self.connect() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS game_record(uid TEXT NOT NULL, gid TEXT NOT NULL, record INT NOT NULL, PRIMARY KEY (uid, gid))"
            )

    def add_record(self, uid, gid):
        with self.connect() as conn:
            conn.execute("INSERT INTO game_record (uid, gid, record) VALUES (?, ?, 1) ON CONFLICT (uid, gid) DO UPDATE SET record = record + 1", (uid, gid))

    async def get_records_and_rankings(self, gid):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._get_records_and_rankings, gid)

    def _get_records_and_rankings(self, gid):
        with self.connect() as conn:
            query = "SELECT uid, record, RANK () OVER (ORDER BY record DESC) as ranking FROM game_record WHERE gid = ? ORDER BY record DESC"
            records = conn.execute(query, (gid,)).fetchall()
            return records

    async def get_total_records_and_rankings(self):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._get_total_records_and_rankings)

    def _get_total_records_and_rankings(self):
        with self.connect() as conn:
            query = "SELECT uid, SUM(record) as total_record, RANK () OVER (ORDER BY SUM(record) DESC) as ranking FROM game_record GROUP BY uid ORDER BY total_record DESC"
            records = conn.execute(query).fetchall()
            return records

db = GameRecord(dbpath)
