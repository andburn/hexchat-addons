import hexchat


__module_name__ = "Trim Nicks"
__module_author__ = "andburn"
__module_version__ = "0.1"
__module_description__ = "Trim nicknames to a defined length"


MAX_LEN = 12
NOTICE_LEN = 8


def trim_nicks(word, word_eol, userdata):
	# add three for color code
	max_len = MAX_LEN + 3
	if len(word) > 2:
		nickname = word[0]
		if len(nickname) > max_len:
			new_nick = nickname[0:max_len - 1] + "~"
			hexchat.emit_print(userdata, new_nick, word[1])
			return hexchat.EAT_ALL

	return hexchat.EAT_NONE


def trim_notice(word, word_eol, userdata):
	max_len = NOTICE_LEN
	if len(word) > 2:
		source = word[0]
		if len(source) > max_len:
			source = source[0:max_len - 1] + "~"
			hexchat.emit_print(userdata, source, word[1], word[2])
			return hexchat.EAT_ALL

	return hexchat.EAT_NONE


hexchat.hook_print("Channel Message", trim_nicks, "Channel Message")
hexchat.hook_print("Channel Msg Hilight", trim_nicks, "Channel Msg Hilight")
hexchat.hook_print("Channel Notice", trim_notice, "Channel Notice")
