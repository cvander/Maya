# Schedule Data Format

Staff schedules are stored as markdown tables in this directory.

- `current.md` -- The active weekly schedule. One table with columns: Day, Shift, Start, End, Staff, Role.
- `staff.md` -- Staff roster with availability, max hours, and certification status.

Schedule skills read these files via `io.read_allowed_path()`. Do not move them outside `docs/schedule/` without updating skill configurations.
