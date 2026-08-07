# -----------------------------------------------------------------------------
# À AJOUTER dans send_mass_update_data.py, DANS send_mass_update_data_to_cosmos,
# juste après le chargement du workbook (ligne ~99, après
# "mu_version = get_mu_version(workbook)") et AVANT le bloc existant
# "if mass_update_template.entity_type == FEES and mu_version == MASS_UPDATE_VERSION_3:"
#
# Imports à ajouter en haut du fichier :
#   from util.mass_update.fees_detection import is_all_fees_mass_update
#   from util.mass_update.process_all_fees_mass_update import process_all_fees_mass_update
#   from services.fee_cre_builder import build_cre_data_for_all_fees
#
# ⚠️ ORDRE IMPORTANT : ce nouveau bloc doit être vérifié EN PREMIER,
# avant le bloc ADL existant — is_all_fees_mass_update ne matche QUE
# notre nouveau template (headers différents de l'ADL), donc pas de
# risque de collision, mais on le place avant par clarté et parce que
# c'est le chemin le plus récent/spécifique.
# -----------------------------------------------------------------------------

    workbook = openpyxl.load_workbook(
        filename=BytesIO(cos_mu_template),
        read_only=True,
        data_only=True,
    )

    mu_version = get_mu_version(workbook)

    # ==================================================================
    # NOUVEAU CAS : "All Fees" mass update (Management/Distribution/
    # Charity/Advisory/Subscription/Redemption/Conversion/Specific &
    # External) — détecté par le CONTENU du fichier, pas par mu_version
    # ni par task.name, pour rester robuste à un fichier modifié entre
    # le download et l'upload.
    # ==================================================================
    if is_all_fees_mass_update(workbook):
        diffs = process_all_fees_mass_update(workbook)

        cre_data_by_product_id, mapping_entity_line_dict, skipped_new_fees = (
            build_cre_data_for_all_fees(user, task, diffs)
        )

        if skipped_new_fees:
            for skipped in skipped_new_fees:
                report_document_content += (
                    f"SKIPPED (no fee_id/fee_value_id, cannot create via "
                    f"mass update): sha_cd={skipped['sha_cd']} "
                    f"field={skipped['field']} "
                    f"new_value={skipped['new_value']}\n"
                )
            report_document_log(report_document, report_document_content)

        if not cre_data_by_product_id:
            # Rien à envoyer (soit aucune diff, soit tout était skipped)
            report_document_content += "No valid changes to send to Cosmos.\n"
            report_document_log(report_document, report_document_content)
            return []

        # À partir d'ici, la suite du flux est IDENTIQUE à la boucle
        # d'envoi existante plus bas dans la fonction (celle qui itère
        # sur cre_data_by_product_id.items(), appelle send_cre,
        # gère les erreurs via check_send_mass_update_data_to_cosmos_response_for_error,
        # etc.) — pas besoin de la dupliquer : remplace juste
        # cre_data_by_product_id / mapping_entity_line_dict obtenus par
        # create_cre_data_to_send_to_cosmos par les nôtres, et laisse le
        # reste de la fonction continuer tel quel (la boucle
        # "for k, v in cre_data_by_product_id.items():" et tout ce qui
        # suit n'a besoin d'aucune modification).

    # Handle special case for Specific Fees (ADL) — bloc EXISTANT, inchangé
    elif mass_update_template.entity_type == FEES and mu_version == MASS_UPDATE_VERSION_3:
        (
            cre_data_by_product_id,
            mapping_entity_line_dict,
        ) = create_cre_data_for_mass_update_fees_to_send_to_cosmos(user, task, workbook, mass_update_template)

    # ... reste du elif/else existant, INCHANGÉ
