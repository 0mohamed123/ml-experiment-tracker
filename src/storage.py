import sqlite3
import json
import os
from datetime import datetime


class Storage:
    def __init__(self, db_path='experiments.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    params TEXT,
                    metrics TEXT,
                    tags TEXT,
                    notes TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')

    def save(self, experiment):
        with sqlite3.connect(self.db_path) as conn:
            now = datetime.now().isoformat()
            if experiment.get('id'):
                conn.execute('''
                    UPDATE experiments
                    SET metrics=?, updated_at=?
                    WHERE id=?
                ''', (json.dumps(experiment['metrics']),
                      now, experiment['id']))
            else:
                cursor = conn.execute('''
                    INSERT INTO experiments
                    (name, params, metrics, tags, notes, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    experiment['name'],
                    json.dumps(experiment.get('params', {})),
                    json.dumps(experiment.get('metrics', {})),
                    json.dumps(experiment.get('tags', [])),
                    experiment.get('notes', ''),
                    now, now
                ))
                return cursor.lastrowid
        return experiment.get('id')

    def load(self, exp_id):
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                'SELECT * FROM experiments WHERE id=?', (exp_id,)).fetchone()
            if row:
                return self._row_to_dict(row)
        return None

    def list_all(self):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                'SELECT * FROM experiments ORDER BY created_at DESC').fetchall()
            return [self._row_to_dict(r) for r in rows]

    def delete(self, exp_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM experiments WHERE id=?', (exp_id,))

    def _row_to_dict(self, row):
        return {
            'id': row[0], 'name': row[1],
            'params': json.loads(row[2] or '{}'),
            'metrics': json.loads(row[3] or '{}'),
            'tags': json.loads(row[4] or '[]'),
            'notes': row[5],
            'created_at': row[6], 'updated_at': row[7]
        }