import unittest
from corebot.simple_messenger import SimpleHtmlMessenger


class TestSimpleHtmlMessenger(unittest.TestCase):

    def test_build_suspicions(self):
        """
            Test: Integration: SimpleHtmlMessenger: teste build_suspicions
        """
        messenger = SimpleHtmlMessenger()

        self.assertEquals(messenger.build_suspicions({"traveled_speeds_classifier": "teste"}), "Viagens muito rápidas")
        self.assertEquals(messenger.build_suspicions({"irregular_companies_classifier": "teste"}), "CNPJ irregular")
        self.assertEquals(messenger.build_suspicions(
            {"meal_price_outlier": "teste"}), "Preço de refeição muito incomum")
        self.assertEquals(messenger.build_suspicions({"election_expenses_classifier": "teste"}), {
                          "election_expenses_classifier": "teste"})
        self.assertEquals(messenger.build_suspicions(
            {"meal_price_outlier_classifier": "teste"}), "Valor suspeito de refeição")
        self.assertEquals(messenger.build_suspicions(
            {"over_monthly_subquota_limit": "teste"}), "Extrapolou o limite da (sub)quota")
