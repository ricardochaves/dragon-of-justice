

class SimpleHtmlMessenger:

    def start_message(self):
        msg = (
            "Bem vindo ao Controle Público, aqui você pode verificar as atividades suspeitas "
            "dos seus candidatos, para saber como funciona a detecção de uma informação suspeita "
            "acesse em www.serenata.ai. \nAgora me diga qual o deputado você quer "
            "seguir. Funciona da seguinte forma, digite o seguinte: \n \n/nome fulano \n \nTodos "
            "os deputádos que tem fulano no nome ou sobrenome irão aparecer na lista. \nPara saber "
            "mais sobre o bot digite /ajuda."
        )
        return [msg]

    def help_message(self):
        msg = (
            "Commandos disponíveis:\n\n/nome fulano\n/lista\n\nUtilizando esses dois comandos você "
            "já será capaz de utilizar o bot. Esses comando vão mostras as outras opções que você tem"
        )
        return [msg]

    def user_user_following(self, itens):

        text = "<strong>%s</strong>.\n -- Para ver o históricos: /historico_%s\n -- Para parar de seguir" \
            " /deixardeseguir_%s"

        msg = 'Você está seguindo os seguintes políticos: \n%s' % self._build_list_name_string(text, itens)

        return [msg]

    def follow_congressperson(self, name, congressperson_id):
        msg = (
            "Agora você está seguindo %s. Para parar de seguir use /deixardeseguir_%s.\n\nPara ver a lista "
            "de todos os deputados seguidos user /lista" % (name, congressperson_id)
        )
        return [msg]

    def unfollow_congressperson(self, name):
        msg = "Você deixou de seguir %s" % name
        return [msg]

    def names_list(self, name, itens):

        text = "<strong>%s</strong>.\n -- Para seguir use /seguir_%s\n -- Para fiscalizar use /historico_%s"

        msg = "A pesquisa pelo nome <strong>%s</strong> gerou os seguintes resultados: \n %s" % (
            name, self._build_list_name_string(text, itens))

        return [msg]

    def history_message(self, itens, applicant_id, next_offset):
        msg = self.build_msg_suspicions(itens)

        if len(itens) == 7:
            msg.append("Para ver mais click em /proximos_%s_%s" % (applicant_id, next_offset))

        return msg

    def create_item_message(self, data):

        item = ("<strong>Ano:</strong> %s\n"
                "<strong>Quota:</strong> %s\n"
                "<strong>Grupo Quota:</strong> %s\n"
                "<strong>Fornecedor:</strong> %s\n"
                "<strong>CNPJ Fornecedo:</strong> %s\n"
                "<strong>Data:</strong> %s\n"
                "<strong>Documento Id:</strong> %s\n"
                "<strong>Valor:</strong> %s\n"
                "<strong>MOTIVO:</strong> %s\n"
                "<a href='%s'>MAIS INFORMAÇÕES DO JARBAS CLIQUE AQUI</a>\n"
                "<strong>Link Nota Fiscal:</strong> %s\n" % (
                    data['year'],
                    data['subquota_description'],
                    data['subquota_group_description'],
                    data['supplier'],
                    data['cnpj_cpf'],
                    data['issue_date'],
                    data['document_id'],
                    data['document_value'],
                    self.build_suspicions(data['suspicions']),
                    'https://jarbas.serenata.ai/layers/#/documentId/%s' % data['document_id'],
                    data['receipt']['url'] if data['receipt']['url'] else 'Não cadastrado'
                )
                )

        return item

    def build_msg_suspicions(self, lista):
        itens = [self.create_item_message(x) for x in lista]

        if len(lista) > 0:
            core_texto = 'Abaixo dessa mensagem você vai receber uma mensagem para cada ocorrencia do %s' % lista[
                0]["congressperson_name"]
        else:
            core_texto = 'Não foi encontrada nenhuma ocorrencia para o político'

        msg = [core_texto] + itens

        return msg

    def build_suspicions(self, data):
        suspicions_dict = {
            "irregular_companies_classifier": "CNPJ irregular",
            "meal_price_outlier": "Preço de refeição muito incomum",
            "election_expenses_classifier": data,
            "meal_price_outlier_classifier": "Valor suspeito de refeição",
            "over_monthly_subquota_limit": "Extrapolou o limite da (sub)quota",
            "traveled_speeds_classifier": "Viagens muito rápidas"
        }

        return suspicions_dict.get(list(data)[0], data)

    @staticmethod
    def _build_list_name_string(msg, names_list):
        return '\n\n'.join([msg % (x[0], x[1], x[1]) for x in names_list])
