# cosmos_api — Endpoint fees complet (scope de ce microservice)

## Ce que `cosmos_api` doit faire, et RIEN de plus

`cosmos_api` expose **un seul endpoint** : `POST /retrieve_fees_data`.
Son unique rôle est de renvoyer, en JSON, toutes les données de fees
(métadonnées produit + ADL in/out existant + tous les autres types de
fees) pour une liste de produits donnée, avec les labels déjà traduits.

**Ce que `cosmos_api` NE fait PAS** (c'est le rôle de `flowr_api`) :
- Générer le fichier Excel
- Gérer le téléchargement
- Détecter les champs modifiés après réupload
- Émettre des events

## Schéma du flux (rappel)

```
flowr_api  ──POST /retrieve_fees_data──▶  cosmos_api
                                              │
                                              ▼
                              ┌─────────────────────────────┐
                              │ single_export / subfund_export│
                              │ (EXISTANT, inchangé — ADL       │
                              │  in/out inclus)                   │
                              └───────────────┬─────────────────┘
                                              │
                                              ▼
                              ┌─────────────────────────────┐
                              │ get_raw_fees(sha_cds)          │
                              │ 1 requête product_fee            │
                              │ + 1 requête field_value (cache)    │
                              └───────────────┬─────────────────┘
                                              │
                                              ▼
                              ┌─────────────────────────────┐
                              │ FeeExportService                │
                              │ .build_fee_columns()              │
                              │ (pivot Python, config FEE_GROUPS)    │
                              └───────────────┬─────────────────┘
                                              │
                                              ▼
                                  Merge dans les lignes
                                              │
                                              ▼
                              Réponse JSON {SIN, SUB, unknown}
                                              │
                                              ▼
                              flowr_api (génère l'Excel, gère
                              le téléchargement, la détection
                              de diff, les events)
```

## Fichiers livrés — tous testés

| Fichier | Action | Destination |
|---|---|---|
| `constants/export_query_constants_ADDITIONS.py` | Copier à la fin de `src/constants/export_query_constants.py` | idem |
| `constants/field_value_types_config.py` | Nouveau fichier | `src/constants/field_value_types_config.py` |
| `constants/fee_groups_config.py` | Nouveau fichier | `src/constants/fee_groups_config.py` |
| `repositories/field_value_repository.py` | Nouveau fichier | `src/repositories/field_value_repository.py` |
| `repositories/export_query_repository_ADDITION.py` | Ajouter la méthode `get_raw_fees` dans `ExportQueryRepository` existant | `src/repositories/export_query_repository.py` |
| `models/field_value_A_CREER_SI_ABSENT.py` | Seulement si `FieldValue` n'existe pas déjà (`grep -r "class FieldValue" src/models/`) | `src/models/field_value.py` |
| `services/field_value_cache.py` | Nouveau fichier | `src/services/field_value_cache.py` |
| `services/fee_export_service.py` | Nouveau fichier | `src/services/fee_export_service.py` |
| `resources/retrieve_fees_data.py` | Nouveau fichier | `src/resources/retrieve_fees_data.py` |
| `routes/retrieve_fees_data.py` | Nouveau fichier | `src/routes/retrieve_fees_data.py` |
| `swagger/retrieve_fees_data/POST.yml` | Nouveau fichier | `src/swagger/retrieve_fees_data/POST.yml` |
| `tests/test_fee_pivot_complete.py` | Test unitaire — **déjà exécuté, 2/2 OK** | `tests/` |

## Résultat des tests (déjà validés)

```
✅ test_pivot_with_translated_labels OK
✅ test_missing_fee_returns_none OK

🎉 Tous les tests passent.
```

## Étapes pour toi

1. Placer les fichiers selon le tableau
2. **Enregistrer le blueprint dans `app.py`** — regarde EXACTEMENT
   comment `RETRIEVE_ADL_FEES_DATA_BLUEPRINT` est enregistré (avec ou
   sans `url_prefix`) et fais pareil, pour éviter les problèmes d'URL
   qu'on a eus avec Postman
3. Relancer le serveur Flask (arrêt complet, pas juste un hot-reload)
4. Tester avec Postman : `POST /retrieve_fees_data` (même host/port que
   ADL), body JSON `{"prod_cd_list": ["..."]}`, avec le même token que
   pour ADL
5. Vérifier que les labels sont bien traduits dans la réponse (pas de
   codes bruts du style `"M"`, `"1"` dans les colonnes `Basis of
   Calculation` / `Calculation Frequency` / `Payment Frequency` / `Paid To`)

## Ce qui n'est pas touché

- `single_export` / `subfund_export` (ADL in/out) restent identiques
- Aucun modèle SQLAlchemy modifié à part l'ajout éventuel de `FieldValue`
  s'il n'existait pas déjà

## Ce qui reste à valider avec le métier

- Hedging fees et Performance fees ne sont pas encore dans `FEE_GROUPS`
- Charity est traité comme un subtype direct (`CHARITY_SUBTYPE="4"`)
