from corebot.simple_messenger import SimpleHtmlMessenger
from corebot.db import MongoCore
from corebot.requests_jarbas import Requester
import logging

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class CoreBot:

    def __init__(self, messenger=None, db=None, requester=None):

        self.messenger = messenger if messenger else SimpleHtmlMessenger()
        self.db = db if db else MongoCore()
        self.requester = requester if requester else Requester()

    def execute_command(self, command, user_id):
        args = self._translate_command(command)
        return self._execute(user_id, args)

    def _translate_command(self, command):
        if command[:5] == "/nome":
            return [command[:5], " ".join(command.split(' ')[1:])]
        else:
            return [command.split("_")[0], command.split("_")[1:]]

    def _execute(self, user_id, command):
        command_list = {
            "/nome": self._command_name,
            "/ajuda": self._command_help,
            "/lista": self._command_list,
            "/seguir": self._command_follow,
            "/deixardeseguir": self._command_unfollow,
            "/start": self._command_start,
            "/historico": self._command_history,
            "/proximos": self._command_proximos}

        return command_list[command[0]](user_id, command)

    def _command_start(self, user_id, command):
        self.db.insert_user(user_id)
        return self.messenger.start_message()

    def _command_help(self, user_id, command):
        return self.messenger.help_message()

    def _command_list(self, user_id, command):
        itens = [[self.db.get_congressperson_name(x['id']), x['id']] for x in self.db.get_user_following(user_id)]
        return self.messenger.user_user_following(itens)

    def _command_follow(self, user_id, command):
        name = self.db.add_congressperson_to_follow(user_id, int(command[1][0]))
        return self.messenger.follow_congressperson(name, command[1][0])

    def _command_unfollow(self, user_id, command):
        name = self.db.remove_congressperson_to_follow(user_id, int(command[1][0]))
        return self.messenger.unfollow_congressperson(name)

    def _command_name(self, user_id, command):
        itens = self.requester.find_names(command[1])
        return self.messenger.names_list(command[1], itens)

    def _command_history(self, user_id, command):
        itens, next_offset = self.requester.find_suspicions(command[1][0])
        return self.messenger.history_message(itens, command[1][0], next_offset)

    def _command_proximos(self, user_id, command):
        itens, next_offset = self.requester.find_suspicions(command[1][0], command[1][1])
        return self.messenger.history_message(itens, command[1][0], next_offset)
