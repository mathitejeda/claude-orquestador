#!/usr/bin/env python3
"""Métricas del orquestador.

Modos:
  (sin argumentos)  Hook SubagentStop: lee el JSON del evento por stdin y, si el
                    subagente es de este plugin, agrega una línea a
                    ~/.claude/orquestador/eventos.jsonl.
  --id [ruta]       Imprime {"proyecto", "proyecto_id"} del repo en ruta (o el
                    directorio actual). Lo usan las skills para el historial.

Nunca guarda contenido del proyecto: solo nombre de carpeta, un id hasheado,
agente, modelo y contadores. La ruta completa va únicamente al índice local
config.json, que no sale de la máquina.

Como hook, nunca falla ni bloquea: ante cualquier error sale con 0.
"""
import datetime
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = os.path.expanduser("~/.claude/orquestador")
EVENTOS = os.path.join(BASE, "eventos.jsonl")
CONFIG = os.path.join(BASE, "config.json")
PREFIJO = "orquestador:"


def _git(ruta, *args):
    try:
        r = subprocess.run(["git", "-C", ruta, *args], capture_output=True,
                           text=True, timeout=3)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def _normalizar_remote(url):
    url = url.strip().lower()
    url = re.sub(r"^[a-z+]+://", "", url)      # https://, ssh://
    url = re.sub(r"^[^@/]+@", "", url)         # usuario[:token]@
    url = url.replace(":", "/", 1) if re.match(r"^[^/]+:[^/]", url) else url  # git@host:owner/repo
    url = re.sub(r"\.git$", "", url).rstrip("/")
    return url


def identificar(ruta):
    raiz = _git(ruta, "rev-parse", "--show-toplevel") or os.path.abspath(ruta)
    remote = _git(raiz, "remote", "get-url", "origin")
    if remote:
        pid = hashlib.sha256(_normalizar_remote(remote).encode()).hexdigest()[:10]
    else:
        pid = "local-" + hashlib.sha256(raiz.encode()).hexdigest()[:8]
    return {"proyecto": os.path.basename(raiz), "proyecto_id": pid, "_raiz": raiz}


def _modelo_y_contadores(transcript):
    modelos, turnos, herramientas, t_in, t_out = {}, 0, 0, 0, 0
    if not transcript or not os.path.exists(transcript):
        return None, 0, 0, 0, 0
    with open(transcript, encoding="utf-8") as f:
        for linea in f:
            try:
                d = json.loads(linea)
            except ValueError:
                continue
            if d.get("type") != "assistant":
                continue
            m = d.get("message") or {}
            if m.get("model"):
                modelos[m["model"]] = modelos.get(m["model"], 0) + 1
            turnos += 1
            for bloque in m.get("content") or []:
                if isinstance(bloque, dict) and bloque.get("type") == "tool_use":
                    herramientas += 1
            u = m.get("usage") or {}
            t_in += (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) \
                + (u.get("cache_read_input_tokens") or 0)
            t_out += u.get("output_tokens") or 0
    modelo = max(modelos, key=modelos.get) if modelos else None
    return modelo, turnos, herramientas, t_in, t_out


def _familia(modelo):
    for fam in ("haiku", "sonnet", "opus", "fable"):
        if modelo and fam in modelo:
            return fam
    return modelo or "desconocido"


def _actualizar_indice(info):
    os.makedirs(BASE, exist_ok=True)
    with open(CONFIG + ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            with open(CONFIG, encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, ValueError):
            cfg = {}
        proyectos = cfg.setdefault("proyectos", {})
        actual = proyectos.get(info["proyecto_id"], {})
        if actual.get("ruta") == info["_raiz"]:
            return
        proyectos[info["proyecto_id"]] = {"nombre": info["proyecto"], "ruta": info["_raiz"]}
        tmp = CONFIG + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        os.replace(tmp, CONFIG)


def hook():
    evento = json.load(sys.stdin)
    agente = evento.get("agent_type") or ""
    if not agente.startswith(PREFIJO):
        return
    info = identificar(evento.get("cwd") or os.getcwd())
    modelo, turnos, herramientas, t_in, t_out = _modelo_y_contadores(
        evento.get("agent_transcript_path"))
    linea = {
        "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "proyecto": info["proyecto"],
        "proyecto_id": info["proyecto_id"],
        "agente": agente[len(PREFIJO):],
        "modelo": modelo,
        "familia": _familia(modelo),
        "agent_id": evento.get("agent_id"),
        "turnos": turnos,
        "herramientas": herramientas,
        "tokens_in": t_in,
        "tokens_out": t_out,
    }
    os.makedirs(BASE, exist_ok=True)
    with open(EVENTOS, "a", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    _actualizar_indice(info)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--id":
        info = identificar(sys.argv[2] if len(sys.argv) > 2 else os.getcwd())
        print(json.dumps({k: v for k, v in info.items() if not k.startswith("_")}))
        return
    try:
        hook()
    except Exception:
        pass  # un hook de métricas nunca debe romper la sesión


if __name__ == "__main__":
    main()
