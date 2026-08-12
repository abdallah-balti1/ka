"""
Add to: test/util/mass_update/test_get_mass_update_template.py
(or create this file if it doesn't exist yet in that folder).

Targets the two branches at 0% coverage in
util/mass_update/get_mass_update_template.py:
  - SPEC_ADL_FEES_TEMPLATE in task.name
  - GLOBAL_FEES_TEMPLATE in task.name

Each branch has two possible payload shapes (direct list / SIN+SUB dict),
hence 4 tests minimum to cover the whole inner if/else block.

Imports/patch paths follow the repo's real convention (no "src." prefix,
top-level packages: constants, util.mass_update, services, entities, api —
see test/api/mass_update_template/test_fees_template.py).
"""

import unittest
from unittest.mock import patch, MagicMock

from util.mass_update.get_mass_update_template import get_mass_update_template


class GetMassUpdateTemplateAllFeesTest(unittest.TestCase):

    # ------------------------------------------------------------------
    # SPEC_ADL_FEES_TEMPLATE branch
    # ------------------------------------------------------------------

    @patch("util.mass_update.get_mass_update_template.create_specific_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_adl_fees_data")
    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    def test_spec_adl_fees_template_payload_as_list(
        self, mock_session_mgr, mock_get_adl_fees_data, mock_create_wb
    ):
        mock_session_mgr.return_value.__enter__.return_value = None
        mock_get_adl_fees_data.return_value = [{"sha_cd": "F1"}]
        mock_create_wb.return_value = MagicMock()

        task = MagicMock()
        task.name = "SPEC_ADL_FEES_TEMPLATE"
        product_ids = [1, 2]

        result = get_mass_update_template(task, product_ids)

        mock_get_adl_fees_data.assert_called_once_with(product_ids)
        mock_create_wb.assert_called_once_with([{"sha_cd": "F1"}])
        self.assertEqual(result, mock_create_wb.return_value)

    @patch("util.mass_update.get_mass_update_template.create_specific_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_adl_fees_data")
    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    def test_spec_adl_fees_template_payload_as_dict(
        self, mock_session_mgr, mock_get_adl_fees_data, mock_create_wb
    ):
        mock_session_mgr.return_value.__enter__.return_value = None
        mock_get_adl_fees_data.return_value = {
            "SIN": [{"sha_cd": "F1"}],
            "SUB": [{"sha_cd": "F2"}],
        }
        mock_create_wb.return_value = MagicMock()

        task = MagicMock()
        task.name = "SPEC_ADL_FEES_TEMPLATE"

        get_mass_update_template(task, [1])

        called_with = mock_create_wb.call_args[0][0]
        self.assertEqual(len(called_with), 2)  # SUB + SIN concatenated

    @patch("util.mass_update.get_mass_update_template.create_specific_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_adl_fees_data")
    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    def test_spec_adl_fees_template_payload_none(
        self, mock_session_mgr, mock_get_adl_fees_data, mock_create_wb
    ):
        # covers the "or []" fallback when payload/list is empty or None
        mock_session_mgr.return_value.__enter__.return_value = None
        mock_get_adl_fees_data.return_value = None
        mock_create_wb.return_value = MagicMock()

        task = MagicMock()
        task.name = "SPEC_ADL_FEES_TEMPLATE"

        get_mass_update_template(task, [1])

        mock_create_wb.assert_called_once_with([])

    # ------------------------------------------------------------------
    # GLOBAL_FEES_TEMPLATE branch
    # ------------------------------------------------------------------

    @patch("util.mass_update.get_mass_update_template.create_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_fees_data")
    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    def test_global_fees_template_payload_as_list(
        self, mock_session_mgr, mock_get_fees_data, mock_create_wb
    ):
        mock_session_mgr.return_value.__enter__.return_value = None
        mock_get_fees_data.return_value = [{"sha_cd": "F1"}]
        mock_create_wb.return_value = MagicMock()

        task = MagicMock()
        task.name = "GLOBAL_FEES_TEMPLATE"

        result = get_mass_update_template(task, [1, 2])

        mock_get_fees_data.assert_called_once_with([1, 2])
        mock_create_wb.assert_called_once_with([{"sha_cd": "F1"}])
        self.assertEqual(result, mock_create_wb.return_value)

    @patch("util.mass_update.get_mass_update_template.create_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_fees_data")
    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    def test_global_fees_template_payload_as_dict(
        self, mock_session_mgr, mock_get_fees_data, mock_create_wb
    ):
        mock_session_mgr.return_value.__enter__.return_value = None
        mock_get_fees_data.return_value = {
            "SIN": [{"sha_cd": "F1"}],
            "SUB": [{"sha_cd": "F2"}],
            "unknown": [{"sha_cd": "F3"}],  # must be ignored (not SIN/SUB)
        }
        mock_create_wb.return_value = MagicMock()

        task = MagicMock()
        task.name = "GLOBAL_FEES_TEMPLATE"

        get_mass_update_template(task, [1])

        called_with = mock_create_wb.call_args[0][0]
        self.assertEqual(len(called_with), 2)  # "unknown" not included

    @patch("util.mass_update.get_mass_update_template.create_fees_template_workbook")
    @patch("util.mass_update.get_mass_update_template.get_fees_data")
    @patch("util.mass_update.get_mass_update_template.SessionCriticalActionManager")
    def test_global_fees_template_payload_none(
        self, mock_session_mgr, mock_get_fees_data, mock_create_wb
    ):
        mock_session_mgr.return_value.__enter__.return_value = None
        mock_get_fees_data.return_value = None
        mock_create_wb.return_value = MagicMock()

        task = MagicMock()
        task.name = "GLOBAL_FEES_TEMPLATE"

        get_mass_update_template(task, [1])

        mock_create_wb.assert_called_once_with([])


if __name__ == "__main__":
    unittest.main()
