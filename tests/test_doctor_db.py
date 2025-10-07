import os
import sqlite3
import tempfile
import importlib.util

# We'll import functions from doctor_finder by manipulating module globals to point DB_PATH to a temp file
spec = importlib.util.spec_from_file_location('doctor_finder', os.path.join(os.path.dirname(__file__), '..', 'doctor_finder.py'))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def setup_temp_db():
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('CREATE TABLE Doctor (doctorID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, specialty TEXT)')
    conn.commit()
    conn.close()
    return path


def test_add_fetch_update_delete():
    path = setup_temp_db()
    try:
        # point module to use temp DB
        mod.DB_PATH = path

        # initially empty
        assert mod.fetch_doctors() == []

        # add
        mod.add_doctor('Dr A', 'Cardiology')
        rows = mod.fetch_doctors()
        assert len(rows) == 1
        did = rows[0][0]
        assert rows[0][1] == 'Dr A'

        # update
        mod.update_doctor(did, 'Dr A Updated', 'Neurology')
        rows2 = mod.fetch_doctors()
        assert rows2[0][1] == 'Dr A Updated'
        assert rows2[0][2] == 'Neurology'

        # duplicate check
        assert not mod.doctor_exists('Nonexistent')
        assert mod.doctor_exists('Dr A Updated')

        # delete
        mod.delete_doctor(did)
        assert mod.fetch_doctors() == []

    finally:
        os.remove(path)
