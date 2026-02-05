# Simple-Ant-CA
Minimal simulation of an ant searching and gathering resources. Technically not designed as a cellular automaton but follows all classical CA rules with one exception.

Consists of an ant which starts on a home cell then moves randomly, leaving a trail, until it overlaps with a resource cell.
It then removes the resource and switches to the full state where it prefers to move to a trail cell if it can.
When it overlaps a home cell the ant switches back to the empty state and restarts the cycle, clearing any remaining trails.

The trails don't store any invisible data (ie. they are not direction) and the ant can only sense the trails in its immediate neighborhood (4 cells).
The cell states (ground/home/resource), ant states (blank, standing/moving + empty/full), and trail states (blank, to home) are coded in separate layers for simplicity.
To convert this to a conventional CA, the state layers could be merged (with some combined states added) and the global trail clearing could be removed.
