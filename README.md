# mini-timer

## Version Summary

### V0
- `init` and `start` were the only working commands.
- Other commands returned a placeholder message.
- Data storage was minimal.

### V1
- `start` and `stop` now work as a real timer flow.
- Completed sessions are written to a persistent log file.
- `log` and `stats` provide session history and summary output.
- The SPEC was clarified with a single-active-session rule and an exact timestamp format.

## V1 Tasks
1. Implement a real `stop` command that closes the active timer and saves the result.
2. Add a persistent session log so completed timers can be listed later.
3. Add a `stats` command to show total sessions, total duration, and average duration.

## Notes
- Project data is stored in `.minitimer/`.
- The CLI entry point is `solution_v1.py`.
