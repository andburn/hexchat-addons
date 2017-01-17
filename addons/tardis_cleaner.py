import re
import hexchat


__module_name__ = "Tardis Cleaner"
__module_author__ = "andburn"
__module_version__ = "0.1"
__module_description__ = "Clean up TardisBot noise on #hearthsim"


def clean_tardis(word, word_eol, userdata):
	if len(word) > 2:
		nickname = str(word[0])
		message = str(word[1])

		match = re.search(r'\[(discord|gitter|irc)\]\s+<(.*?)>\s+(.*)', message)
		if match:
			nickname = match.group(2) + "|" + match.group(1)[0:1].upper()
			message = match.group(3)

		hexchat.emit_print(userdata, nickname, message)
		return hexchat.EAT_ALL

hexchat.hook_print("Channel Message", clean_tardis, "Channel Message")
hexchat.hook_print("Channel Msg Hilight", clean_tardis, "Channel Msg Hilight")

print(__module_name__, 'version', __module_version__, 'loaded.')
