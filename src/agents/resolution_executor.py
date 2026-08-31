
#RESOLUTION EXECUTOR



class ResolutionExecutor:

    # =============================================
    # EXECUTE RESOLUTION
    # =============================================

    def execute(
        self,
        decision,
        context
    ):

        action = decision.get(
            "action_taken"
        )


        # -----------------------------------------
        # LINK RECOVERED SETTLEMENT
        # -----------------------------------------

        if action == "LINK_RECOVERED_SETTLEMENT":

            return self.link_recovered_settlement(
                decision,
                context
            )


        # -----------------------------------------
        # NO AUTO EXECUTION
        # -----------------------------------------

        return {

            "execution_status":
                "NOT_EXECUTED",

            "execution_message":
                "No automatic execution performed",

            "action":
                action

        }


    # =============================================
    # LINK RECOVERED SETTLEMENT
    # =============================================

    def link_recovered_settlement(
        self,
        decision,
        context
    ):

        payment = context.get(
            "payment",
            {}
        )

        settlement = context.get(
            "settlement",
            {}
        )


        payment_id = context.get(
            "payment_id"
        )


        settlement_id = settlement.get(
            "settlement_id"
        )


        payment_amount = payment.get(
            "amount"
        )


        settlement_amount = settlement.get(
            "gross_amount"
        )


        # -----------------------------------------
        # SAFETY VALIDATION
        # -----------------------------------------

        if settlement_id is None:

            return {

                "execution_status":
                    "FAILED",

                "execution_message":
                    "Recovered settlement ID is missing"

            }


        if (

            payment_amount is None

            or

            settlement_amount is None

        ):

            return {

                "execution_status":
                    "FAILED",

                "execution_message":
                    "Payment or settlement amount is missing"

            }


        if payment_amount != settlement_amount:

            return {

                "execution_status":
                    "FAILED",

                "execution_message":
                    (
                        "Settlement amount does not match "
                        "payment amount"
                    )

            }


        # -----------------------------------------
        # EXECUTION SUCCESS
        # -----------------------------------------

        return {

            "execution_status":
                "EXECUTED",

            "execution_message":
                (
                    "Recovered settlement successfully "
                    "linked to payment"
                ),

            "payment_id":
                payment_id,

            "settlement_id":
                settlement_id,

            "payment_amount":
                payment_amount,

            "settlement_amount":
                settlement_amount,

            "execution_action":
                "LINK_RECOVERED_SETTLEMENT"

        }