import os
import time
from datetime import date

from corebot.db import MongoCore
from corebot.requests_jarbas import Requester


class CoreWorker:
    @staticmethod
    def working():
        return True

    def start_worker(self):
        mongo = MongoCore()
        requester = Requester()

        sleep_time = os.getenv("SLEEP_TIME", 86400)
        while self.working():

            # Ir no banco e pegar a data de execução
            dt = mongo.get_last_execution()

            # Verificar a data de execução para montar a querystring
            if dt < date.today():

                # Executar o Jarbas
                result = requester.find_suspicions_by_date(dt)

            # Montar os resultados

            # Enviar as mensagens

            # Update banco de dados

            time.sleep(sleep_time)


if __name__ == "__main__":
    CoreWorker().start_worker()
