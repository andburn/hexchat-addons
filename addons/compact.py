__module_name__ = "Compact"
__module_author__ = "andburn"
__module_version__ = "0.1"
__module_description__ = "Compact layout to maximize horizontal space"


import re
import datetime
import hexchat


NICK_LEN = 10
prev_dates = {}


def get_previous(channel):
	global prev_dates
	if channel not in prev_dates:
		prev_dates[channel] = datetime.datetime(1970, 1, 1)
	return prev_dates[channel]


def set_previous(channel, date):
	global prev_dates
	prev_dates[channel] = date


def print_date_if_new(channel, time):
	server_time = datetime.datetime.fromtimestamp(time)
	prev_day = get_previous(channel)
	if server_time.date() > prev_day.date():
		set_previous(channel, server_time)
		print(server_time.strftime("\n\002%A, %d %b %Y"))


def handle_message(word, word_eol, userdata, attributes):
	if attributes.time:
		channel = hexchat.get_info("channel")
		print_date_if_new(channel, attributes.time)

	return hexchat.EAT_NONE


def handle_notice(word, word_eol, userdata, attributes):
	pass


hexchat.hook_server_attrs("PRIVMSG", handle_message)
hexchat.hook_server_attrs("NOTICE", handle_notice)

print(__module_name__, 'version', __module_version__, 'loaded.')
