import re


# =================================================
# REFERENCE MATCHER
# =================================================

class ReferenceMatcher:

    # =================================================
    # NORMALIZE REFERENCE
    # =================================================

    def normalize_reference(
        self,
        reference
    ):

        if reference is None:
            return ""

        reference = str(
            reference
        ).upper()

        # Extract numeric component
        numbers = re.findall(
            r"\d+",
            reference
        )

        if numbers:
            return numbers[-1]

        return reference


    # =================================================
    # FIND RECOVERABLE MATCH
    # =================================================

    def find_match(
        self,
        payment,
        settlements
    ):

        payment_id = payment["payment_id"]

        normalized_payment = (
            self.normalize_reference(
                payment_id
            )
        )

        candidate_matches = []

        for _, settlement in settlements.iterrows():

            settlement_reference = (
                settlement[
                    "payment_reference"
                ]
            )

            normalized_settlement = (
                self.normalize_reference(
                    settlement_reference
                )
            )

            if (
                normalized_payment
                == normalized_settlement
            ):

                candidate_matches.append(
                    settlement
                )

        # No match
        if not candidate_matches:

            return None

        # More than one possible match
        if len(candidate_matches) > 1:

            return None

        return candidate_matches[0]