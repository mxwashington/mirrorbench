"""Stub tests for the MirrorBench notebooks. No network, no paid calls.

Run from the repo root: python -m unittest discover -s tests -v
"""
import builtins
import hashlib
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import requests

NB_DIR = Path(__file__).resolve().parent.parent / "notebooks"
NOTEBOOKS = ["mirrorbench_v0_2_2.ipynb", "mirrorbench_followups_v0_2_2.ipynb"]
REQUIREMENTS = NB_DIR / "requirements.txt"


def code_cells(nb):
    cells = json.loads((NB_DIR / nb).read_text())["cells"]
    return ["".join(c["source"]) for c in cells if c["cell_type"] == "code"]


def install_cell(nb):
    return next(src for src in code_cells(nb) if "import requests" in src)


def run_install_cell(nb, cwd, calls):
    """Run the install cell as if requests were not installed. Appends each argv passed to subprocess.run to calls."""
    real_import = builtins.__import__

    def fake_import(name, *a, **k):
        if name == "requests" and not calls:
            raise ImportError("requests not installed (stub)")
        return real_import(name, *a, **k)

    old = os.getcwd()
    os.chdir(cwd)
    try:
        with mock.patch("builtins.__import__", fake_import), \
             mock.patch.object(subprocess, "run", lambda argv, **k: calls.append(list(argv))):
            exec(install_cell(nb), {})  # noqa: S102  runs the notebook's own cell under stubs
    finally:
        os.chdir(old)


def pinned_digest(nb):
    found = re.findall(r'^\s*REQUIREMENTS_SHA256 = "([0-9a-f]*)"', install_cell(nb), flags=re.MULTILINE)
    return found[0] if len(found) == 1 else None


class PinnedInstall(unittest.TestCase):
    def test_requirements_pin_every_package_with_a_hash(self):
        self.assertTrue(REQUIREMENTS.exists(), f"{REQUIREMENTS} is missing")
        reqs = re.split(r"\n(?=\S)", re.sub(r"(?m)^\s*#.*\n?", "", REQUIREMENTS.read_text()).strip())
        names = set()
        for r in reqs:
            self.assertRegex(r, r"^[A-Za-z0-9_.-]+==[^\s;]+", f"not pinned with ==: {r.splitlines()[0]}")
            self.assertRegex(r, r"--hash=sha256:[0-9a-f]{64}", f"no sha256 hash: {r.splitlines()[0]}")
            names.add(r.split("==")[0].lower())
        self.assertIn("requests", names)

    def test_pinned_digest_matches_the_lock(self):
        real = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()
        for nb in NOTEBOOKS:
            with self.subTest(nb=nb):
                self.assertEqual(pinned_digest(nb), real, "update REQUIREMENTS_SHA256 in the install cell to the lock's SHA-256")

    def assert_installs_reviewed_lock(self, cwd):
        for nb in NOTEBOOKS:
            with self.subTest(nb=nb, cwd=str(cwd)):
                calls = []
                run_install_cell(nb, cwd, calls)
                self.assertEqual(len(calls), 1)
                pip_args = calls[0][calls[0].index("install") + 1:]
                self.assertIn("--require-hashes", pip_args)
                lock = pip_args[pip_args.index("-r") + 1]
                self.assertTrue(os.path.isabs(lock), f"lock path is not absolute: {lock}")
                self.assertEqual(Path(lock), REQUIREMENTS)
                self.assertEqual([a for a in pip_args if not a.startswith("-")], [lock],
                                 f"pip is asked to install something other than the lock: {pip_args}")

    def test_repo_root_cwd_selects_the_reviewed_lock(self):
        self.assert_installs_reviewed_lock(NB_DIR.parent)

    def test_notebooks_cwd_selects_the_reviewed_lock(self):
        self.assert_installs_reviewed_lock(NB_DIR)

    def assert_refuses(self, setup):
        for nb in NOTEBOOKS:
            with self.subTest(nb=nb), tempfile.TemporaryDirectory() as d:
                setup(Path(d))
                calls = []
                with self.assertRaises(RuntimeError):
                    run_install_cell(nb, d, calls)
                self.assertEqual(calls, [], "pip was called")

    def test_decoy_hashed_requirements_is_refused(self):
        decoy = "requests==2.0.0 \\\n    --hash=sha256:" + "0" * 64 + "\n"
        self.assert_refuses(lambda d: (d / "requirements.txt").write_text(decoy))

    def test_modified_lock_is_refused(self):
        def setup(d):
            (d / "notebooks").mkdir()
            (d / "notebooks" / "requirements.txt").write_bytes(REQUIREMENTS.read_bytes() + b"\n")
            (d / "requirements.txt").write_bytes(REQUIREMENTS.read_bytes().replace(b"requests==", b"requests>=", 1))
        self.assert_refuses(setup)

    def test_absent_lock_is_refused(self):
        self.assert_refuses(lambda d: None)


class FakeResponse:
    def __init__(self, data, status=200):
        self.status_code, self._data, self.text = status, data, json.dumps(data)

    def raise_for_status(self):
        pass

    def json(self):
        return self._data


class SpendGuards(unittest.TestCase):
    """The spend guard cells (config, catalog preflight, ledger) still refuse before any POST."""

    def load(self, nb, extra_price=None):
        """Run every code cell up to the ledger cell with a stub catalog. Returns (namespace, posted bodies)."""
        cells = code_cells(nb)
        upto = next(i for i, s in enumerate(cells) if "def ledger_reserve" in s)
        posted, ns = [], {}

        def fake_get(url, **k):
            slugs = {s for v in ns.values() if isinstance(v, (list, tuple))
                     for s in v if isinstance(s, str) and re.fullmatch(r"[\w.-]+/[\w.:-]+", s)}
            pricing = {"prompt": "0.000001", "completion": "0.000002", **(extra_price or {})}
            return FakeResponse({"data": [{"id": s, "name": s, "pricing": dict(pricing), "context_length": 200000,
                                           "supported_parameters": ["reasoning", "max_tokens"]} for s in sorted(slugs)]})

        def fake_post(url, json=None, **k):
            posted.append(json)
            return FakeResponse({"model": json["model"], "choices": [{"message": {"content": "x" * 80}, "finish_reason": "stop"}],
                                 "usage": {"prompt_tokens": 10, "completion_tokens": 20, "cost": 0.0001}})

        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        old = os.getcwd()
        os.chdir(d.name)
        self.addCleanup(os.chdir, old)
        for p in (mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "stub-not-a-key"}),
                  mock.patch.object(requests, "get", fake_get), mock.patch.object(requests, "post", fake_post)):
            p.start()
            self.addCleanup(p.stop)
        for src in cells[:upto + 1]:
            exec(src, ns)  # noqa: S102  runs the notebook's own cells under stubs
        return ns, posted

    def model(self, ns):
        return ns["JUDGES"][0]

    def test_call_within_budget_is_sent_and_settled(self):
        for nb in NOTEBOOKS:
            with self.subTest(nb=nb):
                ns, posted = self.load(nb)
                res = ns["call"](self.model(ns), "hello")
                self.assertEqual(len(posted), 1)
                self.assertNotIn("error", res)
                self.assertEqual(posted[0]["usage"], {"include": True})
                self.assertIn("max_price", posted[0]["provider"])

    def test_call_over_budget_is_refused_before_post(self):
        for nb in NOTEBOOKS:
            with self.subTest(nb=nb):
                ns, posted = self.load(nb)
                ns["RUN_BUDGET_USD"] = 0.0
                with self.assertRaises(ns["BudgetExceeded"]):
                    ns["call"](self.model(ns), "hello")
                self.assertEqual(posted, [])

    def test_cache_control_body_is_refused(self):
        for nb in NOTEBOOKS:
            with self.subTest(nb=nb):
                ns, _ = self.load(nb)
                m = self.model(ns)
                body = {"model": m, "max_tokens": 10, "usage": {"include": True},
                        "provider": {"max_price": ns["max_price_body"](m)},
                        "messages": [{"role": "user", "content": "hi"}], "cache_control": {"type": "ephemeral"}}
                with self.assertRaises(RuntimeError):
                    ns["check_spend_body"](m, body)

    def test_preflight_refuses_a_request_fee(self):
        for nb in NOTEBOOKS:
            with self.subTest(nb=nb), self.assertRaisesRegex(RuntimeError, "request"):
                self.load(nb, extra_price={"request": "0.01"})


if __name__ == "__main__":
    unittest.main()
