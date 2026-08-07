"""
Orchestration du traitement d'un mass update "All Fees" une fois
détecté par is_all_fees_mass_update(wb).

Appelé depuis send_mass_update_data_to_cosmos :

    if is_all_fees_mass_update(workbook):
        diffs = process_all_fees_mass_update(workbook)
        cre_data_by_product_id, mapping_entity_line_dict, skipped_new_fees = (
            build_cre_data_for_all_fees(user, task, diffs)
        )
"""

from typing import Dict, List

from client.smartgps import get_refetch_fees_data
from services.fee_diff_service import FeeDiffService
from util.mass_update.fees_upload import parse_fees_template_workbook


def process_all_fees_mass_update(wb) -> List[Dict]:
    """
    1. Parse le classeur uploadé (colonnes éditables + Cosmos ID + Product Cd)
    2. Rappelle cosmos_api (/refetch_fees_data) pour l'état FRAIS de ces sha_cd
    3. Calcule la diff entre le fichier et l'état frais

    Retourne la liste des diffs :
        [{"sha_cd", "prod_cd", "field", "old_value", "new_value",
          "fee_id", "fee_value_id"}, ...]

    Ne fait PAS l'émission des events ni la construction des CreData —
    c'est le rôle de build_cre_data_for_all_fees, appelé séparément par
    l'appelant (le job dans send_mass_update_data.py).
    """
    file_rows = parse_fees_template_workbook(wb)

    if not file_rows:
        return []

    sha_cd_list = [row["sha_cd"] for row in file_rows]
    fresh_data_by_sha_cd: Dict[str, Dict] = get_refetch_fees_data(sha_cd_list)

    diffs = FeeDiffService.build_diff(file_rows, fresh_data_by_sha_cd)

    return diffs
