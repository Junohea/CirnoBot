# CirnoBot
A bot for tehtube/CyTube

# Requirements:
<li>Python 3.5
<li>Registered CyTube account. Few functionality does not work properly without being a moderator.

# Usage:
<li>Edit <code>conf.cfg</code>
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
<li><code>!db [title]|[series num]</code> - Add videos from Google Spreadsheets to the end of playlist. (Example: !db Toradora |1,2) Requires <a href='https://console.developers.google.com/project'>OAuth2<a>
<li><code>!random [username]</code> - Fetches a quote from the user given, otherwise fetches a random quote.
<li><code>!stat [username]</code> - Quantity of chat messages by username.
<li><code>!hit [username]</code> - Hit username.

Require rank:
<li><code>!poll [title]</code> - Open an obscured poll to rate a title.
<li><code>!alert [username]</code> - Print list of AFK users.
<li><code>!schedule [username]</code> - Add shedule to the end of playlist. Requires Requires <a href='https://console.developers.google.com/project'>OAuth2<a>

