"""
Add to: test/util/mass_update/test_send_mass_update_data.py

Targets the branches shown as uncovered (red margin) on the coverage report:
  1. if is_all_fees_mass_update(workbook): ... build_cre_data_for_all_fees
     + skipped_new_fees loop -> report_document_log
  2. elif entity_type == FEES and mu_version == MASS_UPDATE_VERSION_3:
     -> create_cre_data_for_mass_update_fees_to_send_to_cosmos

Imports/patch paths follow the repo's real convention (no "src." prefix,
top-level packages: constants, util.mass_update, services, entities, api).
`build_cre_data_for_all_fees` is actually defined in `services.fee_cre_builder`
(confirmed signature: (user, task, diffs) -> (cre_data_by_product, mapping,
skipped) — see test/services/test_fee_cre_builder.py) but it's patched where
it's *used*, i.e. in util.mass_update.send_mass_update_data, assuming a
`from services.fee_cre_builder import build_cre_data_for_all_fees` at the top
of that file. Adjust if the import is done differently there (e.g. importing
the module and calling `fee_cre_builder.build_cre_data_for_all_fees(...)`).
"""

import unittest
from unittest.mock import patch, MagicMock

from util.mass_update.send_mass_update_data import send_mass_update_data


class SendMassUpdateDataAllFeesTest(unittest.TestCase):

    # ------------------------------------------------------------------
    # is_all_fees_mass_update branch — happy path, no skipped fees
    # ------------------------------------------------------------------

    @patch("util.mass_update.send_mass_update_data.build_cre_data_for_all_fees")
    @patch("util.mass_update.send_mass_update_data.process_all_fees_mass_update")
    @patch("util.mass_update.send_mass_update_data.is_all_fees_mass_update")
    @patch("util.mass_update.send_mass_update_data.cos_read_file")
    @patch("util.mass_update.send_mass_update_data.openpyxl.load_workbook")
    def test_all_fees_mass_update_no_skipped(
        self, mock_load_wb, mock_cos_read, mock_is_all_fees, mock_process, mock_build_cre
    ):
        mock_is_all_fees.return_value = True
        mock_process.return_value = {"some": "diffs"}
        mock_build_cre.return_value = ({"P1": []}, {}, [])  # empty skipped_new_fees

        user, task = MagicMock(), MagicMock()

        send_mass_update_data(user, task)

        mock_process.assert_called_once()
        mock_build_cre.assert_called_once_with(user, task, {"some": "diffs"})

    # ------------------------------------------------------------------
    # is_all_fees_mass_update branch — with skipped fees (missing
    # fee_id/fee_value_id) -> verifies the report_document_log call
    # ------------------------------------------------------------------

    @patch("util.mass_update.send_mass_update_data.report_document_log")
    @patch("util.mass_update.send_mass_update_data.build_cre_data_for_all_fees")
    @patch("util.mass_update.send_mass_update_data.process_all_fees_mass_update")
    @patch("util.mass_update.send_mass_update_data.is_all_fees_mass_update")
    @patch("util.mass_update.send_mass_update_data.cos_read_file")
    @patch("util.mass_update.send_mass_update_data.openpyxl.load_workbook")
    def test_all_fees_mass_update_with_skipped_fees(
        self, mock_load_wb, mock_cos_read, mock_is_all_fees,
        mock_process, mock_build_cre, mock_report_log
    ):
        mock_is_all_fees.return_value = True
        mock_process.return_value = {"some": "diffs"}
        skipped = [{"sha_cd": "SHA1", "field": "Rate"}]
        mock_build_cre.return_value = ({"P1": []}, {}, skipped)

        user, task = MagicMock(), MagicMock()

        send_mass_update_data(user, task)

        # the SKIPPED message must be logged at least once for this fee
        logged_calls = [
            call.args[1] for call in mock_report_log.call_args_list
            if "SKIPPED" in str(call.args[1])
        ]
        self.assertTrue(logged_calls)
        self.assertIn("SHA1", logged_calls[0])
        self.assertIn("Rate", logged_calls[0])

    # ------------------------------------------------------------------
    # Existing ADL branch: entity_type == FEES, mu_version == VERSION_3
    # ------------------------------------------------------------------

    @patch("util.mass_update.send_mass_update_data.create_cre_data_for_mass_update_fees_to_send_to_cosmos")
    @patch("util.mass_update.send_mass_update_data.get_mu_version")
    @patch("util.mass_update.send_mass_update_data.is_all_fees_mass_update")
    @patch("util.mass_update.send_mass_update_data.cos_read_file")
    @patch("util.mass_update.send_mass_update_data.openpyxl.load_workbook")
    def test_adl_fees_mass_update_version_3(
        self, mock_load_wb, mock_cos_read, mock_is_all_fees,
        mock_get_mu_version, mock_create_cre
    ):
        mock_is_all_fees.return_value = False
        mock_get_mu_version.return_value = "MASS_UPDATE_VERSION_3"
        mock_create_cre.return_value = ({"P1": []}, {})

        user, task = MagicMock(), MagicMock()
        task.mass_update_template.entity_type = "FEES"

        send_mass_update_data(user, task)

        mock_create_cre.assert_called_once()


if __name__ == "__main__":
    unittest.main()
