identify_playstation2_games
==========

A module for identifying Sony Playstation 2 games with Python 2 &amp; 3

Warning: It only works on DVD ISO files, and not yet CD ISO files.


Example use:
-----
~~~python

from identify_playstation2_games import get_playstation2_game_info

info = get_playstation2_game_info("E:\Sony\Playstation2\Armored Core 3\Armored Core 3.iso")
print(info)

# outputs:
# ("SLUS-20435", u"Armored Core 3")
~~~


