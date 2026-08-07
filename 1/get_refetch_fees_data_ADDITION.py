# -----------------------------------------------------------------------------
# À AJOUTER dans src/client/smartgps.py, à côté de get_adl_fees_data et
# get_fees_data (même fichier, même pattern).
# -----------------------------------------------------------------------------

def get_refetch_fees_data(sha_cd_list):
    """Calls /refetch_fees_data — renvoie l'état FRAIS des fees pour une
    liste de sha_cd (pas de codes produits), utilisé pour la diff au
    moment du traitement du mass update "All Fees".

    Retourne un dict :
        {
          "41455": {
            "Max Management fees Rate": {
              "value": "0.4",
              "fee_id": "...",
              "fee_value_id": "..."
            },
            ...
          },
          ...
        }
    """
    logging.debug("[SMARTGPS] Refetch fees data loading...")
    session = get_new_requests_session()
    url = "{}/refetch_fees_data".format(config.SMARTGPS_URL)

    headers = {"Api-Key": config.API_KEY}
    data = {"sha_cd_list": sha_cd_list}

    response = session.post(url, json=data, headers=headers, verify=False)
    handle_http_error(response)
    logging.debug("[SMARTGPS] Refetch fees data loaded.")

    return response.json()
