"""
Config déclarative de la mise en page du template Excel de fees
(cosmos_api — /generate_fees_excel), utilisée par FeeExcelGenerator.

⚠️ CORRECTION du 10/08 : ordre des sections aligné sur celui de
flowr_api (constants/fees_template.py) — Specific & External vient
après Management et AVANT Distribution/Charity/Advisory, pas en
dernier. Les deux fichiers DOIVENT rester synchronisés (deux repos
séparés, pas de partage de code possible).

Les colonnes d'identification (BASE_COLUMNS) restent inchangées ici :
ce générateur sert à un export simple, pas au template éditable de
mass update — pas de colonnes techniques cachées (Cosmos ID/Product Cd)
nécessaires pour ce cas d'usage.
"""

# Couleurs (ARGB, sans le préfixe "FF" -> openpyxl l'ajoute)
COLOR_BASE = "8496B0"          # gris-bleu : colonnes d'identification
COLOR_SUBS_RED_CONV = "1F6F43"  # vert : subscription/redemption/conversion
COLOR_MANAGEMENT = "1F7A72"     # teal : management fees
COLOR_SPECIFIC_EXTERNAL = "1F3864"  # bleu marine : specific & external fees
COLOR_DISTRIB_CHARITY = "1F6F43"    # vert : distribution / charity
COLOR_ADVISORY = "1F6F43"           # vert : advisory

BASE_COLUMNS = [
    ("Umbrella name", "umb_name_lbl"),
    ("Sub-fund name", "sbf_name"),
    ("Sub-fund ALADDIN code", "prod_cd_valu"),
    ("Sub-fund status", "sbf_stat_lbl"),
    ("Share name", "sha_name"),
    ("ISIN code", "isin_cd"),
    ("Share status", "sha_stat_lbl"),
]

# --- ORDRE RÉEL confirmé le 10/08, identique à flowr_api ---
EXCEL_SECTIONS = [
    {
        "title": "Subscription/Redemption/Conversion fees",
        "color": COLOR_SUBS_RED_CONV,
        "subsections": [
            {
                "subtitle": "Subscription fees",
                "columns": [
                    ("Acquired MAX Rate", "Subscription Acquired MAX Rate"),
                    ("Non Acquired MAX Rate", "Subscription Non Acquired MAX Rate"),
                ],
            },
            {
                "subtitle": "Redemption fees",
                "columns": [
                    ("Acquired MAX Rate", "Redemption Acquired MAX Rate"),
                    ("Non Acquired MAX Rate", "Redemption Non Acquired MAX Rate"),
                ],
            },
            {
                "subtitle": "Conversion fees",
                "columns": [("Conversion Rate", "Conversion Rate")],
            },
        ],
    },
    {
        "title": "Management fees",
        "color": COLOR_MANAGEMENT,
        "subsections": [
            {
                "subtitle": "Maximum Management fees",
                "columns": [
                    ("Rate", "Max Management fees Rate"),
                    ("Basis of Calculation", "Max Management fees Basis of Calculation"),
                    ("Calculation Frequency", "Max Management fees Calculation Frequency"),
                    ("Payment Frequency", "Max Management fees Payment Frequency"),
                ],
            },
            {
                "subtitle": "Real Management fees",
                "columns": [
                    ("Rate", "Real Management fees Rate"),
                    ("Basis of Calculation", "Real Management fees Basis of Calculation"),
                    ("Calculation Frequency", "Real Management fees Calculation Frequency"),
                    ("Payment Frequency", "Real Management fees Payment Frequency"),
                ],
            },
        ],
    },
    {
        "title": "Specific & External fees",
        "color": COLOR_SPECIFIC_EXTERNAL,
        "subsections": [
            {
                "subtitle": "Max Other Costs",
                "columns": [
                    ("Rate", "Max Other Costs Rate"),
                    ("Basis of Calculation", "Max Other Costs Basis of Calculation"),
                    ("Calculation Frequency", "Max Other Costs Calculation Frequency"),
                    ("Payment Frequency", "Max Other Costs Payment Frequency"),
                    ("Paid To", "Max Other Costs Paid To"),
                ],
            },
            {
                "subtitle": "Real Other Costs",
                "columns": [
                    ("Rate", "Real Other Costs Rate"),
                    ("Basis of Calculation", "Real Other Costs Basis of Calculation"),
                    ("Calculation Frequency", "Real Other Costs Calculation Frequency"),
                    ("Payment Frequency", "Real Other Costs Payment Frequency"),
                    ("Paid To", "Real Other Costs Paid To"),
                ],
            },
            {
                "subtitle": "Max Foreign UCIs Tax",
                "columns": [
                    ("Rate", "Max Foreign UCIs Tax Rate"),
                    ("Basis of Calculation", "Max Foreign UCIs Tax Basis of Calculation"),
                    ("Calculation Frequency", "Max Foreign UCIs Tax Calculation Frequency"),
                    ("Payment Frequency", "Max Foreign UCIs Tax Payment Frequency"),
                    ("Paid To", "Max Foreign UCIs Tax Paid To"),
                ],
            },
            {
                "subtitle": "Real Foreign UCIs Tax",
                "columns": [
                    ("Rate", "Real Foreign UCIs Tax Rate"),
                    ("Basis of Calculation", "Real Foreign UCIs Tax Basis of Calculation"),
                    ("Calculation Frequency", "Real Foreign UCIs Tax Calculation Frequency"),
                    ("Payment Frequency", "Real Foreign UCIs Tax Payment Frequency"),
                    ("Paid To", "Real Foreign UCIs Tax Paid To"),
                ],
            },
            {
                "subtitle": "Max Taxe Abonnement",
                "columns": [
                    ("Rate", "Max Taxe Abonnement Rate"),
                    ("Basis of Calculation", "Max Taxe Abonnement Basis of Calculation"),
                    ("Calculation Frequency", "Max Taxe Abonnement Calculation Frequency"),
                    ("Payment Frequency", "Max Taxe Abonnement Payment Frequency"),
                    ("Paid To", "Max Taxe Abonnement Paid To"),
                ],
            },
            {
                "subtitle": "Real Taxe Abonnement",
                "columns": [
                    ("Rate", "Real Taxe Abonnement Rate"),
                    ("Basis of Calculation", "Real Taxe Abonnement Basis of Calculation"),
                    ("Calculation Frequency", "Real Taxe Abonnement Calculation Frequency"),
                    ("Payment Frequency", "Real Taxe Abonnement Payment Frequency"),
                    ("Paid To", "Real Taxe Abonnement Paid To"),
                ],
            },
        ],
    },
    {
        "title": "Distribution fees",
        "color": COLOR_DISTRIB_CHARITY,
        "subsections": [
            {
                "subtitle": "Maximum Distribution fees",
                "columns": [
                    ("Rate", "Max Distribution fees Rate"),
                    ("Basis of Calculation", "Max Distribution fees Basis of Calculation"),
                    ("Calculation Frequency", "Max Distribution fees Calculation Frequency"),
                    ("Payment Frequency", "Max Distribution fees Payment Frequency"),
                ],
            },
            {
                "subtitle": "Real Distribution fees",
                "columns": [
                    ("Rate", "Real Distribution fees Rate"),
                    ("Basis of Calculation", "Real Distribution fees Basis of Calculation"),
                    ("Calculation Frequency", "Real Distribution fees Calculation Frequency"),
                    ("Payment Frequency", "Real Distribution fees Payment Frequency"),
                ],
            },
        ],
    },
    {
        "title": "Charity fees",
        "color": COLOR_DISTRIB_CHARITY,
        "subsections": [
            {
                "subtitle": "Maximum Charity fees",
                "columns": [
                    ("Rate", "Max Charity fees Rate"),
                    ("Basis of Calculation", "Max Charity fees Basis of Calculation"),
                    ("Calculation Frequency", "Max Charity fees Calculation Frequency"),
                    ("Payment Frequency", "Max Charity fees Payment Frequency"),
                ],
            },
            {
                "subtitle": "Real Charity fees",
                "columns": [
                    ("Rate", "Real Charity fees Rate"),
                    ("Basis of Calculation", "Real Charity fees Basis of Calculation"),
                    ("Calculation Frequency", "Real Charity fees Calculation Frequency"),
                    ("Payment Frequency", "Real Charity fees Payment Frequency"),
                ],
            },
        ],
    },
    {
        "title": "Advisory fees",
        "color": COLOR_ADVISORY,
        "subsections": [
            {
                "subtitle": "Maximum Advisory fees",
                "columns": [
                    ("Rate", "Max Advisory fees Rate"),
                    ("Basis of Calculation", "Max Advisory fees Basis of Calculation"),
                    ("Calculation Frequency", "Max Advisory fees Calculation Frequency"),
                    ("Payment Frequency", "Max Advisory fees Payment Frequency"),
                ],
            },
            {
                "subtitle": "Real Advisory fees",
                "columns": [
                    ("Rate", "Real Advisory fees Rate"),
                    ("Basis of Calculation", "Real Advisory fees Basis of Calculation"),
                    ("Calculation Frequency", "Real Advisory fees Calculation Frequency"),
                    ("Payment Frequency", "Real Advisory fees Payment Frequency"),
                ],
            },
        ],
    },
    # TODO : Hedging fees — pas encore dans le pivot de référence.
]
