# CirnoBot
A bot for CyTube.

<a href="https://github.com/tehnotcpu/CirnoBot/wiki/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D1%8F-%D0%BD%D0%B0-%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%BC">Документация на русском</a>

# Requirements:
<li>Python 3.5
<li>Registered CyTube account. Few functionality does not work properly without being a moderator.

# Usage:
<li><code>python3 setup.py install</code>
<li>Edit <code>conf.cfg in CirnoBot directory</code>
<li>Run with <code>python3 cyclient.py</code>

# Commands
Most commands mainly in Russian  ¯\\_(ツ)_/¯
<li><code>!pick [choices]</code> - Chooses a random item from the choices given.
<li><code>!roll [range]</code> - Chooses a random number from the range given(optional).
<li><code>!ask [question]</code> - Answers the question using a simple magic.
<li><code>!who [query]</code> - Chooses a user randomly.
<li><code>!uptime</code> - Sends the uptime of Cirno
<li><code>!quote</code> - Random quote from forismatic.com
<li><code>!q</code> - Random quote from database (if you added list of quotes into a table in database)
<li><code>!pic</code> - Random picture from database (if you added list of pictures into a table in database)
<li><code>!booru [query]</code> - Sends a picture from safebooru.org. If no args given - shows random result (Example: !booru Cirno)
<li><code>!4chan [board]</code> - Sends a random picture from 4chan board (Example: !4chan g)
<li><code>!2ch [board]</code> - Sends a random picture from 2ch.hk board (Example: !2ch t)
<li><code>!weather [city]</code> - Looks up current conditions. Requires <a href='http://openweathermap.org/'>OpenWeatherMap<a> API
<li><code>!rate</code> - Sends current rate exchange.
<li><code>!translate</code> - Translates the given string to Russian. Requires <a href='https://tech.yandex.ru/translate/'>Yandex Translate<a> API
<li><code>!add [url(list of url)]</code> - Add videos to the end of playlist.
<li><code>!random [username]</code> - Fetches a quote from the user given, otherwise fetches a random quote.
<li><code>!stat [username]</code> - Quantity of chat messages by username.
<li><code>!hit [username]</code> - Hit username.
<li><code>!search [query]</code> - Sends results from the Google Web Search.
<li><code>!mal [title]</code> - Sends information about anime title from MAL.

Require rank:
<li><code>!alert</code> - Print list of AFK users.
<li><code>!deny [user]</code> - Adds a user to bot blacklist.
<li><code>!allow [user]</code> - Remove a user from bot blacklist.

