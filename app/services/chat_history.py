import json
from pathlib import Path
from threading import Lock
from typing import List, Dict

_HISTORY_FILE = Path(__file__).resolve().parents[2] / "chat_history.json"
_lock = Lock()


class ChatHistory:
    def __init__(self, file_path: Path = _HISTORY_FILE):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _load(self) -> List[Dict[str, str]]:
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save(self, history: List[Dict[str, str]]) -> None:
        self.file_path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_message(self, role: str, text: str) -> None:
        history = self._load()
        history.append({"role": role, "text": text})
        self._save(history)

    def get_history(self) -> List[Dict[str, str]]:
        return self._load()

    def clear(self) -> None:
        self._save([])


chat_history = ChatHistory()
