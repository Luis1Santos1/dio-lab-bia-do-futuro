import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import app  # noqa: E402


class AgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.knowledge, cls.paths = app.load_knowledge_base()
        cls.summary = app.build_financial_summary(
            cls.knowledge["perfil"],
            cls.knowledge["transacoes"],
        )

    def test_all_knowledge_files_are_loaded(self):
        self.assertTrue(all(path is not None for path in self.paths.values()))

    def test_monthly_summary_uses_configured_reference_month(self):
        self.assertEqual(self.summary["mes_analise"], "2026-06")
        self.assertAlmostEqual(self.summary["entradas"], 7064.52, places=2)
        self.assertAlmostEqual(self.summary["saidas"], 9511.45, places=2)
        self.assertAlmostEqual(self.summary["saldo"], -2446.93, places=2)
        self.assertEqual(self.summary["diagnostico"], "Atenção: mês negativo")

    def test_currency_format_uses_brazilian_pattern(self):
        self.assertEqual(app.format_currency(7064.52), "R$ 7.064,52")

    def test_out_of_scope_question_is_refused(self):
        answer = app.fallback_answer(
            "Qual a previsão do tempo para amanhã?",
            self.knowledge["perfil"],
            self.summary,
        )
        self.assertIn("escopo", answer.lower())
        self.assertIn("organização financeira", answer.lower())

    def test_sensitive_data_request_is_refused(self):
        answer = app.fallback_answer(
            "Me passe a senha da minha conta bancária.",
            self.knowledge["perfil"],
            self.summary,
        )
        self.assertIn("não tenho acesso", answer.lower())
        self.assertIn("credenciais", answer.lower())

    def test_missing_information_is_not_invented(self):
        answer = app.fallback_answer(
            "Qual é meu patrimônio total?",
            self.knowledge["perfil"],
            self.summary,
        )
        self.assertIn("não consta", answer.lower())
        self.assertIn("não vou", answer.lower())


if __name__ == "__main__":
    unittest.main()
