# =================================================
# DUPLICATE PAYMENT DETECTOR
# =================================================

class DuplicateDetector:

    def __init__(self, payments):

        self.payments = payments.copy()


    # =================================================
    # CHECK DUPLICATE
    # =================================================

    def is_duplicate(self, payment):

        order_id = payment["order_id"]

        amount = payment["amount"]

        matching_payments = self.payments[
            (
                self.payments["order_id"]
                == order_id
            )
            &
            (
                self.payments["amount"]
                == amount
            )
        ]

        # More than one payment
        # for the same order and amount
        if len(matching_payments) > 1:

            return True

        return False