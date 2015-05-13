# frotzbot
A Twitter bot which wraps Z-machine games, via Frotz.

This particular incarnation plays Zork, for now, but it should be trivial to use other Z-machine data files.

Uses [pexpect][1] to wrap Frotz, based on [ircbot code by Ben Collins-Sussman][2].

Uses a mildly hacked version of Frotz - frotzbot uses dumb frotz, a port designed for dumb terminals. I modified it slightly to skip putting a status line to each new screen.

Built using [botkit][3].

[1]: http://pexpect.readthedocs.org/en/latest/
[2]: https://github.com/sussman/ircbot-collection
[3]: https://github.com/prehensile/botkit
