#!/usr/bin/env python3
"""Word Game server with SQLite history tracking."""

import os
import sys
import json
import sqlite3
import mimetypes
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "word_game.db"
)

PORT = 8000

# --------------------------------------------------------------
def get_db():
    """Get a SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

# --------------------------------------------------------------
def init_db():
    """Create database tables if they don't exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS attempts (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            game_type TEXT NOT NULL,
            game_file TEXT NOT NULL,
            item_id   TEXT NOT NULL,
            correct   INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS item_status (
            game_type     TEXT NOT NULL,
            game_file     TEXT NOT NULL,
            item_id       TEXT NOT NULL,
            status        TEXT NOT NULL
                          DEFAULT 'unknown',
            last_3        TEXT DEFAULT '[]',
            total_correct INTEGER DEFAULT 0,
            total_wrong   INTEGER DEFAULT 0,
            last_seen     TEXT,
            PRIMARY KEY (
                game_type, game_file, item_id
            )
        );

        CREATE INDEX IF NOT EXISTS
            idx_attempts_lookup
        ON attempts(
            game_type, game_file, item_id
        );

        CREATE INDEX IF NOT EXISTS
            idx_status_lookup
        ON item_status(
            game_type, game_file, status
        );
    """)
    conn.commit()
    conn.close()

# --------------------------------------------------------------
def record_attempt(game_type, game_file,
                   item_id, correct):
    """Record an answer attempt and update status."""
    conn = get_db()
    now = datetime.now().isoformat()

    conn.execute(
        "INSERT INTO attempts "
        "(game_type, game_file, item_id, "
        "correct, timestamp) "
        "VALUES (?, ?, ?, ?, ?)",
        (game_type, game_file, item_id,
         1 if correct else 0, now)
    )

    row = conn.execute(
        "SELECT * FROM item_status "
        "WHERE game_type=? AND game_file=? "
        "AND item_id=?",
        (game_type, game_file, item_id)
    ).fetchone()

    if row is None:
        last_3 = [1 if correct else 0]
        tc = 1 if correct else 0
        tw = 0 if correct else 1
        status = compute_status(last_3)
        conn.execute(
            "INSERT INTO item_status "
            "(game_type, game_file, item_id, "
            "status, last_3, total_correct, "
            "total_wrong, last_seen) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (game_type, game_file, item_id,
             status, json.dumps(last_3),
             tc, tw, now)
        )
    else:
        last_3 = json.loads(row["last_3"])
        last_3.append(1 if correct else 0)
        if len(last_3) > 3:
            last_3 = last_3[-3:]
        tc = row["total_correct"] + (
            1 if correct else 0)
        tw = row["total_wrong"] + (
            0 if correct else 1)
        status = compute_status(last_3)
        conn.execute(
            "UPDATE item_status "
            "SET status=?, last_3=?, "
            "total_correct=?, total_wrong=?, "
            "last_seen=? "
            "WHERE game_type=? AND game_file=? "
            "AND item_id=?",
            (status, json.dumps(last_3),
             tc, tw, now,
             game_type, game_file, item_id)
        )

    conn.commit()
    conn.close()
    return status

# --------------------------------------------------------------
def compute_status(last_3):
    """Compute item status from last 3 results."""
    if len(last_3) >= 3 and all(
        r == 1 for r in last_3[-3:]
    ):
        return "solid"
    if len(last_3) > 0:
        return "learning"
    return "unknown"

# --------------------------------------------------------------
def get_history(game_type, game_file):
    """Get all item statuses for a game."""
    conn = get_db()
    rows = conn.execute(
        "SELECT item_id, status, last_3, "
        "total_correct, total_wrong, last_seen "
        "FROM item_status "
        "WHERE game_type=? AND game_file=?",
        (game_type, game_file)
    ).fetchall()
    conn.close()
    result = {}
    for r in rows:
        result[r["item_id"]] = {
            "status": r["status"],
            "last_3": json.loads(r["last_3"]),
            "total_correct": r["total_correct"],
            "total_wrong": r["total_wrong"],
            "last_seen": r["last_seen"],
        }
    return result

# --------------------------------------------------------------
def get_smart_selection(game_type, game_file,
                        all_items, count=4):
    """Select next items using smart algorithm."""
    history = get_history(game_type, game_file)

    unknown = []
    learning = []
    solid = []

    for item_id in all_items:
        sid = str(item_id)
        if sid not in history:
            unknown.append(sid)
        else:
            st = history[sid]["status"]
            if st == "solid":
                solid.append(sid)
            else:
                learning.append(sid)

    import random
    selected = []

    if learning:
        pick = min(1, len(learning))
        selected.extend(
            random.sample(learning, pick)
        )

    remaining = count - len(selected)
    if unknown and remaining > 0:
        pick = min(remaining, len(unknown))
        selected.extend(
            random.sample(unknown, pick)
        )

    remaining = count - len(selected)
    if learning and remaining > 0:
        avail = [
            w for w in learning
            if w not in selected
        ]
        pick = min(remaining, len(avail))
        selected.extend(
            random.sample(avail, pick)
        )

    remaining = count - len(selected)
    if solid and remaining > 0:
        pick = min(remaining, len(solid))
        selected.extend(
            random.sample(solid, pick)
        )

    return selected

# --------------------------------------------------------------
def get_stats(game_type, game_file):
    """Get summary stats for a game."""
    conn = get_db()
    rows = conn.execute(
        "SELECT status, COUNT(*) as cnt "
        "FROM item_status "
        "WHERE game_type=? AND game_file=? "
        "GROUP BY status",
        (game_type, game_file)
    ).fetchall()
    conn.close()
    stats = {
        "unknown": 0,
        "learning": 0,
        "solid": 0
    }
    for r in rows:
        stats[r["status"]] = r["cnt"]
    return stats

# --------------------------------------------------------------
def reset_history(game_type, game_file):
    """Reset all history for a specific game."""
    conn = get_db()
    conn.execute(
        "DELETE FROM attempts "
        "WHERE game_type=? AND game_file=?",
        (game_type, game_file)
    )
    conn.execute(
        "DELETE FROM item_status "
        "WHERE game_type=? AND game_file=?",
        (game_type, game_file)
    )
    conn.commit()
    conn.close()

# --------------------------------------------------------------
class GameHandler(SimpleHTTPRequestHandler):
    """HTTP handler with API endpoints."""

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/api/history":
            self.handle_get_history(params)
        elif path == "/api/history/next-batch":
            self.handle_next_batch(params)
        elif path == "/api/history/stats":
            self.handle_stats(params)
        else:
            super().do_GET()

    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/history":
            self.handle_record_attempt()
        elif path == "/api/history/reset":
            self.handle_reset()
        else:
            self.send_error(404, "Not Found")

    def handle_get_history(self, params):
        """Return item statuses for a game."""
        gt = params.get("game_type", ["word"])[0]
        gf = params.get("game_file", [""])[0]
        if not gf:
            self.send_json(
                {"error": "game_file required"},
                400
            )
            return
        data = get_history(gt, gf)
        self.send_json(data)

    def handle_next_batch(self, params):
        """Return smart selection of items."""
        gt = params.get("game_type", ["word"])[0]
        gf = params.get("game_file", [""])[0]
        count = int(
            params.get("count", ["4"])[0]
        )
        items_raw = params.get("all_items", [""])[0]
        if not gf or not items_raw:
            self.send_json(
                {"error": "game_file and "
                 "all_items required"},
                400
            )
            return
        all_items = json.loads(items_raw)
        selected = get_smart_selection(
            gt, gf, all_items, count
        )
        history = get_history(gt, gf)
        result = {
            "selected": selected,
            "history": {
                k: history[k]
                for k in selected
                if k in history
            }
        }
        self.send_json(result)

    def handle_stats(self, params):
        """Return summary stats for a game."""
        gt = params.get("game_type", ["word"])[0]
        gf = params.get("game_file", [""])[0]
        if not gf:
            self.send_json(
                {"error": "game_file required"},
                400
            )
            return
        stats = get_stats(gt, gf)
        self.send_json(stats)

    def handle_record_attempt(self):
        """Record an answer attempt."""
        body = self.read_body()
        if body is None:
            return
        required = [
            "game_type", "game_file",
            "item_id", "correct"
        ]
        for key in required:
            if key not in body:
                self.send_json(
                    {"error": f"{key} required"},
                    400
                )
                return
        new_status = record_attempt(
            body["game_type"],
            body["game_file"],
            str(body["item_id"]),
            body["correct"]
        )
        self.send_json({
            "status": "ok",
            "new_status": new_status
        })

    def handle_reset(self):
        """Reset history for a game."""
        body = self.read_body()
        if body is None:
            return
        gt = body.get("game_type", "word")
        gf = body.get("game_file", "")
        if not gf:
            self.send_json(
                {"error": "game_file required"},
                400
            )
            return
        reset_history(gt, gf)
        self.send_json({"status": "ok"})

    def read_body(self):
        """Read and parse JSON request body."""
        try:
            length = int(
                self.headers.get(
                    "Content-Length", 0
                )
            )
            raw = self.rfile.read(length)
            return json.loads(raw)
        except Exception as e:
            self.send_json(
                {"error": f"Invalid JSON: {e}"},
                400
            )
            return None

    def send_json(self, data, code=200):
        """Send a JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header(
            "Content-Type", "application/json"
        )
        self.send_header(
            "Content-Length", str(len(body))
        )
        self.send_header(
            "Access-Control-Allow-Origin", "*"
        )
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        """Custom log format."""
        msg = format % args
        sys.stderr.write(
            f"[{datetime.now():%H:%M:%S}] "
            f"{msg}\n"
        )

# --------------------------------------------------------------
def main():
    """Main function to start the server."""
    init_db()
    print(f"Database: {DB_PATH}")
    print(f"Server:   http://localhost:{PORT}")
    print("Press Ctrl+C to stop\n")

    server = HTTPServer(
        ("", PORT), GameHandler
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()

# --------------------------------------------------------------
if __name__ == "__main__":
    main()
