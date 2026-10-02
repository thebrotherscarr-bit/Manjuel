"""THE ROUTES: a model reached somewhere other than the rack.

2026-10-02, WHAT'S LEFT B18 and the first half of H8. The operator's word: "backed by ollama as a
first route then secondarily through additional API as added", and, asked whether RULE 4 should
give way for it: "let's do what I said then, set up a second set for parity, why not? I'm not
scared of it." RULE 4 is amended on that word (CLAUDE.md), narrowly, and this module is the whole
of the amendment's reach in code. It is the only module that knows a hosted model exists, as
runtime.py is the only one that knows the rack does.

A MODEL NAMED WITH NO ROUTE IS OLLAMA'S, AS IT HAS ALWAYS BEEN. A model named `route://model` is
reached through the route of that name: one `us/route_<name>.us` record saying where it goes
(`base_url`), how it speaks (`adapter`), and that it LEAVES THE MACHINE (`remote`). `us.py` checks
the record against this module and parity.md against the records.

WHAT HOLDS IT SHUT, AND WHERE EACH THING IS HELD:

  OFF UNTIL THE OPERATOR TURNS IT ON. A route is on only while its key is in the environment, which
    is where `.env` puts it (RULE 7). The key is read at the call, held in one local variable, sent
    in one header, and never printed, logged, stored, returned or raised: every message this module
    makes is scrubbed of it first. A hand never places a key.
  ONLY WHAT HIS OWN FILE PUT THERE LEAVES. The one caller is `parity.run`, and the text is a
    parity case's objective and feed. `refusal` stops anything the law gate would refuse as an
    objective, the client tag, and the VALUE of any secret in the environment, and says which rule,
    never what matched. A test holds that no other module calls `chat`.
  A KEY NEVER CROSSES IN THE CLEAR OR WHERE IT WAS NOT SENT. A route on another machine must be
    https; a redirect is never followed, because it would carry the key to wherever it points.
  BOUNDED (ESTATE LAW 7). One call, no retries, a time limit, a cap on what is sent and on what is
    read back.
  THE OPERATOR AUTHORISES THE SPEND (RULE 6). Nothing here asks; `/parity` does, and says first
    what will leave.

WHAT THIS DOES NOT DO. No seat sits on a route: a seat naming one finds no such model on the rack
and nothing is sent, and `us.py` reports it (WHAT'S LEFT H8 is that wiring). It does not embed, it
does not stream, and it keeps no price table: a price table is a second thing to keep true (the
atlas ruling of 2026-09-09 refusing a cost bridge stands for atlas).

THE ADAPTER IS ANTHROPIC'S MESSAGES FORM, `POST {base_url}/v1/messages`. Ollama 0.35 on this
machine answers the same form on loopback, which is how it was proved against a real server with
no cloud and no key; the hosted route differs from that run in its host, its TLS and its key.
"""

from __future__ import annotations

import json
import os
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

SEP = "://"

# The speakers this build has. A record naming another is a DRIFT in us.py, and `chat` refuses it.
ADAPTERS = ("anthropic",)
ANTHROPIC_VERSION = "2023-06-01"

MAX_SEND_CHARS = 24_000          # a parity case is a few hundred; this is a ceiling, not a target
MAX_REPLY_BYTES = 2_000_000
CALL_TIMEOUT = 180.0             # seconds, one call, no retry

_LOOPBACK = ("127.0.0.1", "localhost", "::1")
_GROUND = Path(__file__).resolve().parent.parent

# A variable whose NAME says it holds a secret. Its VALUE, if it is long enough to mean something,
# may not appear in a text that leaves.
_SECRET_NAME_RE = re.compile(r"(?i)(KEY|TOKEN|SECRET|PASSWORD|PASSWD|BEARER|SERVICE|CREDENTIAL)")
_MIN_SECRET_LEN = 12


class RouteError(Exception):
    """Base. Every message a route raises is safe to print: it is scrubbed of the key."""


class RouteOff(RouteError):
    """The route's key is not in the environment, so nothing was sent."""


class RouteRefused(RouteError):
    """The text, or the route, is one this module will not send on. Nothing was sent."""


class RouteFailed(RouteError):
    """The call was made and did not come back whole. `remote` says whether it went to another machine."""

    def __init__(self, message: str, remote: bool = True):
        super().__init__(message)
        self.remote = remote


@dataclass(frozen=True)
class Route:
    name: str
    adapter: str
    base_url: str
    remote: bool

    @property
    def key_env(self) -> str:
        return key_env(self.name)


@dataclass(frozen=True)
class Reply:
    text: str
    tokens_in: int | None        # as the provider counted them
    tokens_out: int | None
    stop: str
    route: str
    model: str
    sent_chars: int              # what was sent, in characters
    remote: bool                 # True when it LEFT THE MACHINE; False for a route on this machine


# ---------------------------------------------------------------------
# names
# ---------------------------------------------------------------------


def key_env(name: str) -> str:
    """The variable a route's key lives in. ONE function, read by the loader, by us.py and by the
    strokes, so the name cannot be spelled three ways."""
    return "MANJUEL_ROUTE_" + re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").upper() + "_KEY"


def split(model: str) -> tuple[str, str]:
    """("route", "model") for `route://model`; ("", model) for anything else, which is Ollama's."""
    m = (model or "").strip()
    if SEP in m:
        route, _, name = m.partition(SEP)
        return route.strip().lower(), name.strip()
    return "", m


def is_routed(model: str) -> bool:
    return bool(split(model)[0])


def is_loopback(url: str) -> bool:
    try:
        host = urllib.parse.urlsplit(url).hostname or ""
    except ValueError:
        return False
    return host.lower() in _LOOPBACK


def leaves(route: Route) -> bool:
    """Does a call on this route LEAVE THE MACHINE? Read off the ADDRESS, never off the record's own
    `remote` flag (us.py checks the two agree): a route on loopback stays here, and the reports say so."""
    return not is_loopback(route.base_url)


def host(route: Route) -> str:
    """Where a route's calls go, for a person to read (parity's disclosure says it)."""
    try:
        return urllib.parse.urlsplit(route.base_url).hostname or route.base_url
    except ValueError:
        return route.base_url


def load(ground=None) -> dict[str, Route]:
    """Every route the ground declares, by name: the `route` records of us/."""
    from . import us
    records, _broken = us.load(Path(ground) if ground is not None else _GROUND)
    out: dict[str, Route] = {}
    for r in records:
        if r.get("kind") != "route":
            continue
        name = str(r.get("id", "")).removeprefix("route_")
        out[name] = Route(name=name, adapter=str(r.get("adapter") or ""),
                          base_url=str(r.get("base_url") or "").rstrip("/"),
                          remote=bool(r.get("remote")))
    return out


def enabled(route: Route) -> bool:
    """On while its key is in the environment. The value is tested for presence and goes nowhere."""
    return bool(os.environ.get(route.key_env, "").strip())


# ---------------------------------------------------------------------
# what may leave
# ---------------------------------------------------------------------


def refusal(text: str, ground=None) -> str:
    """Why this text may not leave the machine, or "". It names the RULE and never what matched:
    a message that quoted the secret would carry it."""
    ground = Path(ground) if ground is not None else _GROUND
    if len(text) > MAX_SEND_CHARS:
        return f"it is {len(text)} characters, and a route carries at most {MAX_SEND_CHARS}"
    from . import lawgate
    from .vectors import CLIENT_TOKEN
    if CLIENT_TOKEN in text:
        return "it carries the client tag (SITTING LAW 2)"
    _checks, refusals = lawgate.check_objective(text, ground)
    if refusals:
        return f"the law gate would refuse it as an objective ({refusals[0][0]})"
    for name, value in os.environ.items():
        if len(value) >= _MIN_SECRET_LEN and _SECRET_NAME_RE.search(name) and value in text:
            return f"it carries the value of {name} (RULE 7: keys are silent)"
    return ""


def _scrub(text: str, key: str) -> str:
    return text.replace(key, "[key]") if key else text


# ---------------------------------------------------------------------
# the call
# ---------------------------------------------------------------------


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """A redirect is never followed: urllib would carry the key header to wherever it points."""

    def redirect_request(self, *a, **k):
        return None


def _opener(loopback: bool):
    handlers: list = [_NoRedirect()]
    if loopback:
        handlers.append(urllib.request.ProxyHandler({}))       # a loopback call goes nowhere near a proxy
    return urllib.request.build_opener(*handlers)


def _int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _http_error(name: str, exc: urllib.error.HTTPError, key: str) -> str:
    if 300 <= exc.code < 400:
        return (f"route {name!r} answered {exc.code}, a redirect. It is never followed: it would "
                f"carry the key to wherever it points.")
    detail = ""
    try:
        body = json.loads(exc.read(4096).decode("utf-8", "replace"))
        err = body.get("error") if isinstance(body, dict) else None
        if isinstance(err, dict):
            detail = f"{err.get('type', '')}: {err.get('message', '')}".strip(": ")
    except Exception:
        detail = ""
    return _scrub(f"route {name!r} answered {exc.code}" + (f" ({detail[:300]})" if detail else ""), key)


def chat(model: str, system: str, user: str, *, ground=None, max_tokens: int = 1024,
         timeout: float | None = None, route: Route | None = None) -> Reply:
    """One call to a routed model. `route` is for a caller that has the record in hand (the strokes,
    a proof against a loopback server); the ground's records are read when it is None."""
    name, bare = split(model)
    if not name or not bare:
        raise RouteError(f"{model!r} names no route; a routed model is route://model")
    ground = Path(ground) if ground is not None else _GROUND
    route = route or load(ground).get(name)
    if route is None:
        raise RouteError(f"there is no route named {name!r}: no us/route_{name}.us record")
    if route.adapter not in ADAPTERS:
        raise RouteError(f"route {name!r} speaks {route.adapter!r}; this build has "
                         f"{', '.join(ADAPTERS)} and nothing else")
    loop = is_loopback(route.base_url)
    leave = leaves(route)
    if not loop and not route.base_url.lower().startswith("https://"):
        raise RouteRefused(f"route {name!r} is another machine over plain http, so its key would "
                           f"cross in the clear. Nothing was sent.")
    key = os.environ.get(route.key_env, "").strip()
    if not key:
        raise RouteOff(f"route {name!r} is OFF: {route.key_env} is not set. Put it in .env yourself "
                       f"(RULE 7: it is never printed, and a hand never writes it) and restart.")
    sent = (system or "") + "\n" + (user or "")
    why = refusal(sent, ground)
    if why:
        raise RouteRefused(f"nothing was sent to {name!r}: {why}")

    payload: dict = {"model": bare, "max_tokens": int(max_tokens),
                     "messages": [{"role": "user", "content": user or ""}]}
    if system:
        payload["system"] = system
    req = urllib.request.Request(
        route.base_url + "/v1/messages", data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={"content-type": "application/json", "x-api-key": key,
                 "anthropic-version": ANTHROPIC_VERSION, "user-agent": "manjuel"})
    bound = float(timeout or CALL_TIMEOUT)
    try:
        with _opener(loop).open(req, timeout=bound) as resp:
            raw = resp.read(MAX_REPLY_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise RouteFailed(_http_error(name, exc, key), remote=leave) from None
    except (TimeoutError, socket.timeout):
        raise RouteFailed(f"route {name!r} gave no answer in {bound:.0f}s, and the call was dropped", remote=leave) from None
    except urllib.error.URLError as exc:
        if isinstance(exc.reason, (TimeoutError, socket.timeout)):
            raise RouteFailed(f"route {name!r} gave no answer in {bound:.0f}s, and the call was dropped", remote=leave) from None
        raise RouteFailed(_scrub(f"route {name!r} could not be reached: {exc.reason}", key), remote=leave) from None
    except Exception as exc:                  # never carry the request along in a chain
        raise RouteFailed(f"route {name!r}: {type(exc).__name__}", remote=leave) from None
    if len(raw) > MAX_REPLY_BYTES:
        raise RouteFailed(f"route {name!r} answered more than {MAX_REPLY_BYTES} bytes, and the answer was dropped", remote=leave)
    try:
        body = json.loads(raw.decode("utf-8"))
    except ValueError:
        raise RouteFailed(f"route {name!r} answered something that is not json", remote=leave) from None
    blocks = body.get("content") if isinstance(body, dict) else None
    if not isinstance(blocks, list):
        raise RouteFailed(f"route {name!r} answered without a content list", remote=leave)
    text = "".join(b.get("text", "") for b in blocks
                   if isinstance(b, dict) and b.get("type") == "text")
    usage = body.get("usage") if isinstance(body.get("usage"), dict) else {}
    return Reply(text=_scrub(text.strip(), key), tokens_in=_int(usage.get("input_tokens")),
                 tokens_out=_int(usage.get("output_tokens")), stop=str(body.get("stop_reason") or ""),
                 route=name, model=bare, sent_chars=len(sent), remote=leave)
