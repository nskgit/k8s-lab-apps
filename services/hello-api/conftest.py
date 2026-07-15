"""Anchors pytest's import path at the service root.

pytest inserts the directory containing the topmost conftest.py into
sys.path, which makes `from app...` imports work identically for bare
`pytest` and `python -m pytest`. CI lesson #1 (run #1 failure): bare
`pytest` does NOT add the CWD to sys.path, but `python -m pytest` does —
tests passed locally, failed in CI. This file removes that dependence.
"""
