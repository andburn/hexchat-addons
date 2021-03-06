__module_name__ = "Compact"
__module_author__ = "andburn"
__module_version__ = "0.1"
__module_description__ = "Compact layout to maximize horizontal space"


import re
import time
import datetime
import hexchat


NICK_LEN = 12
tardis_channels = ("#hearthsim", "#HearthSim/Hearthstone-Deck-Tracker")
prev_dates = {}


def get_previous(channel):
	global prev_dates
	if channel not in prev_dates:
		prev_dates[channel] = datetime.datetime(1970, 1, 1)
	return prev_dates[channel]


def set_previous(channel, date):
	global prev_dates
	prev_dates[channel] = date


def truncate(str, length=NICK_LEN):
	if len(str) > length:
		return str[:length - 1] + "~"
	return str


def print_date_if_new(channel, time):
	server_time = datetime.datetime.fromtimestamp(time)
	prev_day = get_previous(channel)
	if server_time.date() > prev_day.date():
		set_previous(channel, server_time)
		print(server_time.strftime("\n\002%A, %d %b %Y\n"))


def handle_message(word, word_eol, userdata, attributes):
	# print date time if new day
	message_time = attributes.time
	if not message_time:
		message_time = time.time()

	channel = hexchat.get_info("channel")
	print_date_if_new(channel, message_time)

	# only handle channels with tardis bot messages
	if word[2] not in tardis_channels:
		return hexchat.EAT_NONE

	# check for hearthsim mirror bot messages
	match = re.search(r':\[(discord|gitter|irc)\]\s+<(.*?)>\s*(.*)', word_eol[3])
	if match:
		# rearrange the message
		nick = truncate(match.group(2), 10) + "|" + match.group(1)[:1].upper()
		message = match.group(3)
	else:
		# otherwise chop nick and use message as given
		message = word_eol[3][1:]
		match = re.search(r':(.+?)!', word[0])
		if match:
			nick = truncate(match.group(1))
		else:
			nick = word[0][:NICK_LEN]

	hexchat.emit_print("Channel Message", nick, message, time=attributes.time)
	return hexchat.EAT_ALL


hexchat.hook_server_attrs("PRIVMSG", handle_message)

print(__module_name__, 'version', __module_version__, 'loaded.')