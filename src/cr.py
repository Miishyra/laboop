class ServerError(Exception):
    pass

class ServerOfflineError(ServerError):
    pass

class ServerAlreadyOnlineError(ServerError):
    pass

class SessionLimitError(ServerError):
    pass

class SessionNotFoundError(ServerError):
    pass


class Server:
    def __init__(self, hostname, ip, status, max_connections):
        self._hostname = hostname.strip()
        self._ip = ip
        self._status = status if status in ["online", "offline", "maintenance"] else "offline"
        self._max_connections = max_connections
        self._active_sessions = []

    @property
    def hostname(self):
        return self._hostname

    @property
    def ip(self):
        return self._ip

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value in ["online", "offline", "maintenance"]:
            self._status = value

    @property
    def max_connections(self):
        return self._max_connections

    @property
    def active_sessions(self):
        return self._active_sessions.copy()

    def start(self):
        if self._status == "online":
            raise ServerAlreadyOnlineError()
        self._status = "online"

    def stop(self):
        self._status = "offline"
        self._active_sessions.clear()

    def open_session(self, session_id):
        if self._status != "online":
            raise ServerOfflineError()
        if len(self._active_sessions) >= self._max_connections:
            raise SessionLimitError()
        self._active_sessions.append(session_id)

    def close_session(self, session_id):
        if session_id not in self._active_sessions:
            raise SessionNotFoundError()
        self._active_sessions.remove(session_id)

    def __str__(self):
        return f"{self._hostname} [{self._ip}] — {self._status}, сессии: {len(self._active_sessions)}/{self._max_connections}"


# ========== ЗАПУСК С ВЫВОДОМ ==========
svr = Server('server-01', '192.168.1.10', 'offline', 10)
svr.start()
print(svr.status)

svr.open_session('sess-001')
svr.open_session('sess-002')
print(len(svr.active_sessions))

svr.close_session('sess-001')
print(len(svr.active_sessions))

print(svr)