#!/usr/bin/env python3
"""
agent-collab board — a tiny multi-agent collaboration board.

Same protocol, two backends, one CLI:
  - local  (default) : append-only JSONL under ./.agent-board/. Zero infrastructure.
  - convex           : your own Convex deployment (see backends/convex/). Real-time, multi-machine.

Select the backend with --backend or the AGENT_BOARD_BACKEND env var.
Local board location: AGENT_BOARD_DIR (default ./.agent-board).

Commands:
  post     append a turn          board.py post --from a --to b --content "..."
  inbox    list unread for agent  board.py inbox --agent a
  read     print + mark read      board.py read --agent a [--conversation slug]
  wait     block until unread     board.py wait --agent a [--poll 7] [--max 1800]
  decide   record a decision      board.py decide --title "..." --decision "..." --by a
  decisions  list recent          board.py decisions [--limit 20]

Stdlib only. Python 3.8+.
"""
import argparse
import json
import os
import sys
import time
import uuid

# ---------------------------------------------------------------- shared helpers

def _now() -> float:
    return time.time()

def _new_id() -> str:
    return uuid.uuid4().hex

def _emit(obj) -> None:
    """Print a result as JSON to stdout (the machine-readable contract)."""
    print(json.dumps(obj, ensure_ascii=False, indent=2))

# ---------------------------------------------------------------- local backend

class LocalBoard:
    """Append-only JSONL file board. Faithful local mirror of the Convex semantics."""

    def __init__(self, board_dir: str):
        self.dir = board_dir
        os.makedirs(self.dir, exist_ok=True)
        self.messages_path = os.path.join(self.dir, "messages.jsonl")
        self.decisions_path = os.path.join(self.dir, "decisions.jsonl")

    def _read_all(self, path):
        if not os.path.exists(path):
            return []
        rows = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows

    def _append(self, path, row):
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    def _rewrite(self, path, rows):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp, path)

    def _participants_for(self, conversation_id):
        """Participants are defined by the FIRST post in a conversation and inherited after."""
        if not conversation_id:
            return None
        for m in self._read_all(self.messages_path):
            if m.get("conversationId") == conversation_id and m.get("participants"):
                return m["participants"]
        return None

    def post(self, from_agent, to_agent, content, msg_type, conversation_id, participants):
        # Inherit participants from the first post of the conversation if not supplied.
        if conversation_id and not participants:
            participants = self._participants_for(conversation_id)
        row = {
            "id": _new_id(),
            "ts": _now(),
            "fromAgent": from_agent,
            "content": content,
            "type": msg_type,
            "readBy": [],
        }
        if to_agent and to_agent != "-":
            row["toAgent"] = to_agent
        if conversation_id and conversation_id != "-":
            row["conversationId"] = conversation_id
        if participants:
            row["participants"] = participants
        self._append(self.messages_path, row)
        return {"id": row["id"], "status": "posted"}

    def _is_for(self, msg, agent):
        if msg.get("fromAgent") == agent:
            return False  # you never receive your own turn
        to = msg.get("toAgent")
        if to is not None:
            return to == agent  # directed
        # broadcast: global (no conversation) reaches everyone; scoped reaches participants
        conv = msg.get("conversationId")
        if not conv:
            return True
        parts = self._participants_for(conv) or msg.get("participants") or []
        return agent in parts

    def inbox(self, agent):
        return [m for m in self._read_all(self.messages_path)
                if self._is_for(m, agent) and agent not in m.get("readBy", [])]

    def read(self, agent, conversation_id):
        rows = self._read_all(self.messages_path)
        if conversation_id:
            thread = [m for m in rows if m.get("conversationId") == conversation_id]
        else:
            thread = [m for m in rows if self._is_for(m, agent) or m.get("fromAgent") == agent]
        # mark read
        changed = False
        for m in rows:
            if m in thread and agent not in m.get("readBy", []) and m.get("fromAgent") != agent:
                m.setdefault("readBy", []).append(agent)
                changed = True
        if changed:
            self._rewrite(self.messages_path, rows)
        return thread

    def decide(self, title, decision, decided_by, approved_by, impact_areas, context):
        row = {
            "id": _new_id(),
            "ts": _now(),
            "title": title,
            "decision": decision,
            "decidedBy": decided_by,
            "impactAreas": impact_areas,
        }
        if approved_by and approved_by != "-":
            row["approvedBy"] = approved_by
        if context:
            row["context"] = context
        self._append(self.decisions_path, row)
        return {"id": row["id"], "status": "recorded"}

    def decisions(self, limit):
        rows = self._read_all(self.decisions_path)
        rows.sort(key=lambda r: r.get("ts", 0), reverse=True)
        return rows[:limit]

# ---------------------------------------------------------------- convex backend

class ConvexBoard:
    """Runs the same primitives against YOUR OWN Convex deployment via `npx convex run`.

    Setup (see backends/convex/README.md):
      - deploy backends/convex/* to your Convex project
      - set CONVEX_PROJECT_DIR to that project (or run board.py from inside it)
    """

    def __init__(self):
        self.project_dir = os.environ.get("CONVEX_PROJECT_DIR", os.getcwd())

    def _run(self, fn, payload):
        import subprocess
        proc = subprocess.run(
            ["npx", "convex", "run", fn, json.dumps(payload)],
            cwd=self.project_dir, capture_output=True, text=True,
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stderr)
            raise SystemExit(f"convex run {fn} failed (rc={proc.returncode})")
        out = proc.stdout.strip()
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            return {"raw": out}

    def post(self, from_agent, to_agent, content, msg_type, conversation_id, participants):
        p = {"fromAgent": from_agent, "content": content, "type": msg_type}
        if to_agent and to_agent != "-":
            p["toAgent"] = to_agent
        if conversation_id and conversation_id != "-":
            p["conversationId"] = conversation_id
        if participants:
            p["participants"] = participants
        return self._run("messages:post", p)

    def inbox(self, agent):
        return self._run("messages:getUnread", {"agentId": agent})

    def read(self, agent, conversation_id):
        # Convex side exposes list + markRead; mirror inbox here for simplicity.
        return self._run("messages:getUnread", {"agentId": agent})

    def decide(self, title, decision, decided_by, approved_by, impact_areas, context):
        p = {"title": title, "decision": decision, "decidedBy": decided_by, "impactAreas": impact_areas}
        if approved_by and approved_by != "-":
            p["approvedBy"] = approved_by
        if context:
            p["context"] = context
        return self._run("decisions:record", p)

    def decisions(self, limit):
        return self._run("decisions:list", {"limit": limit})

# ---------------------------------------------------------------- backend select

def get_board(backend):
    backend = backend or os.environ.get("AGENT_BOARD_BACKEND", "local")
    if backend == "convex":
        return ConvexBoard()
    return LocalBoard(os.environ.get("AGENT_BOARD_DIR", os.path.join(os.getcwd(), ".agent-board")))

# ---------------------------------------------------------------- CLI

def _csv(s):
    return [x.strip() for x in s.split(",") if x.strip()] if s else []

def main():
    ap = argparse.ArgumentParser(description="agent-collab board")
    ap.add_argument("--backend", choices=["local", "convex"], default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("post")
    p.add_argument("--from", dest="from_agent", required=True)
    p.add_argument("--to", dest="to_agent", default="-", help="recipient id, or '-' for broadcast")
    p.add_argument("--content", required=True)
    p.add_argument("--type", default="message",
                   help="message|question|review|decision|status_update")
    p.add_argument("--conversation", dest="conversation", default=None, help="thread slug")
    p.add_argument("--participants", default=None, help="csv, required on first post of a conversation")

    p = sub.add_parser("inbox")
    p.add_argument("--agent", required=True)

    p = sub.add_parser("read")
    p.add_argument("--agent", required=True)
    p.add_argument("--conversation", dest="conversation", default=None)

    p = sub.add_parser("wait")
    p.add_argument("--agent", required=True)
    p.add_argument("--poll", type=int, default=7)
    p.add_argument("--max", type=int, default=1800)

    p = sub.add_parser("decide")
    p.add_argument("--title", required=True)
    p.add_argument("--decision", required=True)
    p.add_argument("--by", dest="decided_by", required=True)
    p.add_argument("--approved-by", dest="approved_by", default="-")
    p.add_argument("--impact", default="", help="csv tags")
    p.add_argument("--context", default="")

    p = sub.add_parser("decisions")
    p.add_argument("--limit", type=int, default=20)

    args = ap.parse_args()
    board = get_board(args.backend)

    if args.cmd == "post":
        _emit(board.post(args.from_agent, args.to_agent, args.content, args.type,
                         args.conversation, _csv(args.participants)))
    elif args.cmd == "inbox":
        _emit(board.inbox(args.agent))
    elif args.cmd == "read":
        _emit(board.read(args.agent, args.conversation))
    elif args.cmd == "wait":
        elapsed = 0
        while elapsed < args.max:
            unread = board.inbox(args.agent)
            if unread:
                _emit(unread)
                return
            time.sleep(args.poll)
            elapsed += args.poll
        sys.stderr.write(f"TIMEOUT: no unread for {args.agent} after {args.max}s\n")
        raise SystemExit(1)
    elif args.cmd == "decide":
        _emit(board.decide(args.title, args.decision, args.decided_by,
                          args.approved_by, _csv(args.impact), args.context))
    elif args.cmd == "decisions":
        _emit(board.decisions(args.limit))

if __name__ == "__main__":
    main()
