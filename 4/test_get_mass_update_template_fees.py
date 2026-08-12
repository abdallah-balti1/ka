"""
Tests des deux branches de retrieve_mass_update_template liées aux fees :
  - SPEC_ADL_FEES_TEMPLATE (ADL in/out, existant)
  - GLOBAL_FEES_TEMPLATE (All Fees, nouveau)

⚠️ Vérifie les points suivants contre le vrai fichier avant utilisation :
  - Le nom exact du module (`util.mass_update.get_mass_update_template`) et
    de la fonction (`retrieve_mass_update_template`)
  - Que SPEC_ADL_FEES_TEMPLATE / GLOBAL_FEES_TEMPLATE sont bien importés
    dans ce module (les tests les réimportent depuis là pour ne jamais
    coder une chaîne en dur qui pourrait diverger de la vraie constante)
  - La signature exacte de la fonction (ici supposée
    retrieve_mass_update_template(task, product_ids))

On mocke : le client HTTP (get_adl_fees_data / get_fees_data), les builders
Excel (create_specific_fees_template_workbook / create_fees_template_workbook)
et SessionCriticalActionManager (context manager, pas besoin de vraie DB pour
ces deux branches spécifiques).
"""

import unittest
from unittest.mock import MagicMock, patch

from util.mass_update.get_mass_update_template import (
    GLOBAL_FEES_TEMPLATE,
    SPEC_ADL_FEES_TEMPLATE,
    retrieve_mass_update_template,
)


def _fake_task(name: str):
    task = MagicMock()
    task.name = name
    task.id = "task_id_1"
    task.task_model.mass_update_template = MagicMock()  # truthy, passe le guard initial
    return task


class TestRetrieveMassUpdateTemplateSpecificFees(unittest.TestCase):
    """Branche SPEC_ADL_FEES_TEMPLATE — comportement EXISTANT, non modifié.
    Tests de non-régression : on vérifie qu'on ne l'a pas cassé en ajoutant
    la branche GLOBAL_FEES_TEMPLATE juste après."""

    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    @patch("util.mass_update.get_mass_update_template.create_specific_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_adl_fees_data")
    def test_dict_payload_concatenates_sub_and_sin(
        self, mock_get_adl_fees_data, mock_create_wb, _mock_session_mgr
    ):
        mock_get_adl_fees_data.return_value = {
            "SUB": [{"sha_cd": "sub_1"}],
            "SIN": [{"sha_cd": "sin_1"}],
        }
        sentinel_wb = MagicMock()
        mock_create_wb.return_value = sentinel_wb

        task = _fake_task(SPEC_ADL_FEES_TEMPLATE)
        result = retrieve_mass_update_template(task, ["prod_1"])

        mock_create_wb.assert_called_once_with(
            [{"sha_cd": "sub_1"}, {"sha_cd": "sin_1"}]
        )
        self.assertIs(result, sentinel_wb)

    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    @patch("util.mass_update.get_mass_update_template.create_specific_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_adl_fees_data")
    def test_list_payload_passed_through_directly(
        self, mock_get_adl_fees_data, mock_create_wb, _mock_session_mgr
    ):
        mock_get_adl_fees_data.return_value = [{"sha_cd": "direct_1"}]

        task = _fake_task(SPEC_ADL_FEES_TEMPLATE)
        retrieve_mass_update_template(task, ["prod_1"])

        mock_create_wb.assert_called_once_with([{"sha_cd": "direct_1"}])

    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    @patch("util.mass_update.get_mass_update_template.create_specific_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_adl_fees_data")
    def test_none_payload_becomes_empty_list(
        self, mock_get_adl_fees_data, mock_create_wb, _mock_session_mgr
    ):
        mock_get_adl_fees_data.return_value = None

        task = _fake_task(SPEC_ADL_FEES_TEMPLATE)
        retrieve_mass_update_template(task, ["prod_1"])

        mock_create_wb.assert_called_once_with([])

    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    @patch("util.mass_update.get_mass_update_template.create_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.create_specific_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_adl_fees_data")
    def test_does_not_call_global_fees_branch(
        self, mock_get_adl_fees_data, mock_create_specific_wb, mock_create_global_wb,
        _mock_session_mgr,
    ):
        """Garde-fou : une tâche ADL ne doit JAMAIS déclencher le chemin
        All Fees (pas d'appel à get_fees_data / create_fees_template_workbook)."""
        mock_get_adl_fees_data.return_value = []

        task = _fake_task(SPEC_ADL_FEES_TEMPLATE)
        retrieve_mass_update_template(task, ["prod_1"])

        mock_create_global_wb.assert_not_called()


class TestRetrieveMassUpdateTemplateGlobalFees(unittest.TestCase):
    """Branche GLOBAL_FEES_TEMPLATE — nouveau chemin All Fees."""

    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    @patch("util.mass_update.get_mass_update_template.create_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_fees_data")
    def test_dict_payload_concatenates_sub_and_sin(
        self, mock_get_fees_data, mock_create_wb, _mock_session_mgr
    ):
        mock_get_fees_data.return_value = {
            "SUB": [{"sha_cd": "sub_1"}],
            "SIN": [{"sha_cd": "sin_1"}],
            "unknown": [],
        }
        sentinel_wb = MagicMock()
        mock_create_wb.return_value = sentinel_wb

        task = _fake_task(GLOBAL_FEES_TEMPLATE)
        result = retrieve_mass_update_template(task, ["prod_1"])

        mock_create_wb.assert_called_once_with(
            [{"sha_cd": "sub_1"}, {"sha_cd": "sin_1"}]
        )
        self.assertIs(result, sentinel_wb)

    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    @patch("util.mass_update.get_mass_update_template.create_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_fees_data")
    def test_list_payload_passed_through_directly(
        self, mock_get_fees_data, mock_create_wb, _mock_session_mgr
    ):
        mock_get_fees_data.return_value = [{"sha_cd": "direct_1"}]

        task = _fake_task(GLOBAL_FEES_TEMPLATE)
        retrieve_mass_update_template(task, ["prod_1"])

        mock_create_wb.assert_called_once_with([{"sha_cd": "direct_1"}])

    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    @patch("util.mass_update.get_mass_update_template.create_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_fees_data")
    def test_none_payload_becomes_empty_list(
        self, mock_get_fees_data, mock_create_wb, _mock_session_mgr
    ):
        mock_get_fees_data.return_value = None

        task = _fake_task(GLOBAL_FEES_TEMPLATE)
        retrieve_mass_update_template(task, ["prod_1"])

        mock_create_wb.assert_called_once_with([])

    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    @patch("util.mass_update.get_mass_update_template.create_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_fees_data")
    def test_empty_dict_payload_becomes_empty_list(
        self, mock_get_fees_data, mock_create_wb, _mock_session_mgr
    ):
        mock_get_fees_data.return_value = {}

        task = _fake_task(GLOBAL_FEES_TEMPLATE)
        retrieve_mass_update_template(task, ["prod_1"])

        mock_create_wb.assert_called_once_with([])

    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    @patch("util.mass_update.get_mass_update_template.create_specific_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.create_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_fees_data")
    def test_does_not_call_specific_fees_branch(
        self, mock_get_fees_data, mock_create_global_wb, mock_create_specific_wb,
        _mock_session_mgr,
    ):
        """Garde-fou symétrique : une tâche All Fees ne doit jamais
        déclencher le chemin ADL."""
        mock_get_fees_data.return_value = []

        task = _fake_task(GLOBAL_FEES_TEMPLATE)
        retrieve_mass_update_template(task, ["prod_1"])

        mock_create_specific_wb.assert_not_called()

    def test_constants_do_not_collide(self):
        """Non-régression : SPEC_ADL_FEES_TEMPLATE ne doit jamais être un
        sous-ensemble de GLOBAL_FEES_TEMPLATE ou inversement, sinon le
        routage par 'in task.name' matcherait les deux branches."""
        self.assertNotIn(SPEC_ADL_FEES_TEMPLATE, GLOBAL_FEES_TEMPLATE)
        self.assertNotIn(GLOBAL_FEES_TEMPLATE, SPEC_ADL_FEES_TEMPLATE)


if __name__ == "__main__":
    unittest.main()
