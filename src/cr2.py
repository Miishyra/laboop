from abc import ABC,abstractmethod

class ValidationError(Exception): pass
class RateLimitExceededError(ValidationError): pass
class IPNotAllowedError(ValidationError): pass
class PayloadTooLargeError(ValidationError): pass

class RequestValidator(ABC):
    def __init__(self): self._n=None
    def set_next(self,n): self._n=n; return n
    def validate(self,r): self._check(r); self._n and self._n.validate(r)
    @abstractmethod
    def _check(self,r): pass

class AuthValidator(RequestValidator):
    def _check(self,r):
        if not r.get("token",""): raise ValidationError

class IPWhitelistValidator(RequestValidator):
    def __init__(self,ips): super().__init__(); self.ips=ips
    def _check(self,r):
        if r.get("source_ip") not in self.ips: raise IPNotAllowedError

class RateLimitValidator(RequestValidator):
    def __init__(self,m): super().__init__(); self.m=m; self.c={}
    def _check(self,r):
        u=r.get("user_id")
        if u:
            self.c[u]=self.c.get(u,0)+1
            if self.c[u]>self.m: raise RateLimitExceededError

class PayloadSizeValidator(RequestValidator):
    def __init__(self,s): super().__init__(); self.s=s
    def _check(self,r):
        if len(str(r.get("payload","")))>self.s: raise PayloadTooLargeError

def build_chain(*v):
    for i in range(len(v)-1): v[i].set_next(v[i+1])
    return v[0] if v else None

class Server:
    def __init__(self,h,ip,s,m):
        self._h=h.strip(); self._ip=ip
        self._s=s if s in["online","offline","maintenance"] else"offline"
        self._m=m; self._a=[]; self._v=None
    @property
    def hostname(self): return self._h
    @property
    def ip(self): return self._ip
    @property
    def status(self): return self._s
    @status.setter
    def status(self,v):
        if v in["online","offline","maintenance"]: self._s=v
    @property
    def max_connections(self): return self._m
    @property
    def active_sessions(self): return self._a.copy()
    def start(self):
        if self._s=="online": raise ServerAlreadyOnlineError
        self._s="online"
    def stop(self): self._s="offline"; self._a.clear()
    def set_validator(self,v): self._v=v
    def open_session(self,r):
        if self._s!="online": raise ServerOfflineError
        if self._v: self._v.validate(r)
        if not r.get("session_id"): raise ValidationError
        if len(self._a)>=self._m: raise SessionLimitError
        self._a.append(r["session_id"])
    def close_session(self,s):
        if s not in self._a: raise SessionNotFoundError
        self._a.remove(s)
    def __str__(self):
        return f"{self._h} [{self._ip}] — {self._s}, сессии: {len(self._a)}/{self._m}"

class ServerError(Exception): pass
class ServerOfflineError(ServerError): pass
class ServerAlreadyOnlineError(ServerError): pass
class SessionLimitError(ServerError): pass
class SessionNotFoundError(ServerError): pass


# ========== ЗАПУСК С ПРИНТАМИ ==========
srv = Server('server-01', '192.168.1.10', 'offline', 10)
srv.start()
print(srv.status)

chain = build_chain(
    AuthValidator(),
    IPWhitelistValidator(['192.168.1.5', '192.168.1.6']),
    RateLimitValidator(3),
    PayloadSizeValidator(1024),
)
srv.set_validator(chain)

req = {'token': 'abc123', 'user_id': 'u1', 'source_ip': '192.168.1.5', 'session_id': 's1', 'payload': 'hello'}
srv.open_session(req)
print("OK")

for i in range(4):
    try:
        srv.open_session({'token': 'abc123', 'user_id': 'u1', 'source_ip': '192.168.1.5', 'session_id': f's{i}', 'payload': 'hello'})
        print(f"OK {i}")
    except RateLimitExceededError:
        print('rate')