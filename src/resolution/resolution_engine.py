# =================================================
# EXCEPTION RESOLUTION ENGINE
# =================================================

class ResolutionEngine:

    def __init__(self):

        self.resolution_rules = {

            "AMOUNT_MISMATCH": {

                "risk_level": "HIGH",

                "recommended_action": (
                    "Hold transaction for manual "
                    "financial review"
                ),

                "auto_resolvable": False
            },


            "MISSING_SETTLEMENT": {

                "risk_level": "HIGH",

                "recommended_action": (
                    "Investigate settlement pipeline "
                    "and contact payment provider "
                    "if required"
                ),

                "auto_resolvable": False
            },


            "REFERENCE_MISMATCH": {

                "risk_level": "LOW",

                "recommended_action": (
                    "Reference successfully recovered; "
                    "review and update reference mapping"
                ),

                "auto_resolvable": True
            },


            "DUPLICATE_PAYMENT": {

                "risk_level": "HIGH",

                "recommended_action": (
                    "Review duplicate transaction pair "
                    "before any refund or reversal action"
                ),

                "auto_resolvable": False
            },


            "MISSING_ORDER": {

                "risk_level": "HIGH",

                "recommended_action": (
                    "Investigate missing order record "
                    "in source system"
                ),

                "auto_resolvable": False
            }
        }


    # =================================================
    # RESOLVE EXCEPTION
    # =================================================

    def resolve(self, exception_type):

        # ---------------------------------------------
        # MATCHED TRANSACTION
        # ---------------------------------------------

        if exception_type is None:

            return {

                "risk_level": "NONE",

                "recommended_action": (
                    "No action required"
                ),

                "auto_resolvable": True
            }


        # ---------------------------------------------
        # KNOWN EXCEPTION
        # ---------------------------------------------

        resolution = (
            self.resolution_rules.get(
                exception_type
            )
        )

        if resolution:

            return resolution


        # ---------------------------------------------
        # UNKNOWN EXCEPTION
        # ---------------------------------------------

        return {

            "risk_level": "UNKNOWN",

            "recommended_action": (
                "Escalate for manual investigation"
            ),

            "auto_resolvable": False
        }