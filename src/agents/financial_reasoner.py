# =================================================
# FINANCIAL REASONING ENGINE
# =================================================


class FinancialReasoner:


    # =============================================
    # MAIN ANALYSIS ENTRY POINT
    # =============================================

    def analyze_exception(
        self,
        context
    ):

        exception_type = (
            context.get(
                "exception_type"
            )
        )


        if exception_type == "AMOUNT_MISMATCH":

            return (
                self.analyze_amount_mismatch(
                    context
                )
            )


        elif exception_type == "REFERENCE_MISMATCH":

            return (
                self.analyze_reference_mismatch(
                    context
                )
            )


        elif exception_type == "MISSING_SETTLEMENT":

            return (
                self.analyze_missing_settlement(
                    context
                )
            )


        elif exception_type == "DUPLICATE_PAYMENT":

            return (
                self.analyze_duplicate_payment(
                    context
                )
            )


        elif exception_type == "MISSING_ORDER":

            return (
                self.analyze_missing_order(
                    context
                )
            )


        else:

            return {

                "analysis_status":
                    "UNKNOWN_EXCEPTION",

                "financial_risk":
                    "UNKNOWN",

                "auto_resolvable":
                    False,

                "confidence":
                    0.0,

                "evidence":
                    [
                        "Unsupported exception type"
                    ]

            }


    # =============================================
    # AMOUNT MISMATCH
    # =============================================

    def analyze_amount_mismatch(
        self,
        context
    ):

        payment = context.get(
            "payment",
            {}
        )

        order = context.get(
            "order",
            {}
        )

        settlement = context.get(
            "settlement",
            {}
        )


        payment_amount = payment.get(
            "amount"
        )

        order_amount = order.get(
            "order_amount"
        )

        settlement_amount = settlement.get(
            "gross_amount"
        )


        if (

            payment_amount is None

            or

            settlement_amount is None

        ):

            return {

                "analysis_status":
                    "INSUFFICIENT_DATA",

                "financial_risk":
                    "HIGH",

                "auto_resolvable":
                    False,

                "confidence":
                    0.30,

                "evidence":
                    [
                        "Payment or settlement amount is missing"
                    ]

            }


        amount_difference = (

            payment_amount
            -
            settlement_amount

        )


        absolute_difference = abs(
            amount_difference
        )


        difference_percentage = (

            absolute_difference
            /
            payment_amount
            *
            100

        )


        evidence = [

            f"Payment amount: {payment_amount}",

            f"Settlement amount: {settlement_amount}",

            f"Difference: {amount_difference}",

            f"Difference percentage: "
            f"{difference_percentage:.2f}%"

        ]


        if order_amount is not None:

            if payment_amount == order_amount:

                evidence.append(

                    "Payment amount matches "
                    "the original order amount"

                )

            else:

                evidence.append(

                    "Payment amount does not match "
                    "the original order amount"

                )


        return {

            "analysis_status":
                "AMOUNT_MISMATCH_CONFIRMED",

            "financial_risk":
                "HIGH",

            "auto_resolvable":
                False,

            "confidence":
                0.95,

            "amount_difference":
                amount_difference,

            "difference_percentage":
                round(
                    difference_percentage,
                    2
                ),

            "evidence":
                evidence

        }


    # =============================================
    # REFERENCE MISMATCH
    # =============================================

    def analyze_reference_mismatch(
        self,
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


        payment_amount = payment.get(
            "amount"
        )

        settlement_amount = settlement.get(
            "gross_amount"
        )


        evidence = [

            "Settlement recovered through "
            "reference matching"

        ]


        if (

            payment_amount is not None

            and

            settlement_amount is not None

        ):

            if payment_amount == settlement_amount:

                evidence.append(

                    "Recovered settlement amount "
                    "matches payment amount"

                )

                return {

                    "analysis_status":
                        "REFERENCE_RECOVERY_VALIDATED",

                    "financial_risk":
                        "LOW",

                    "auto_resolvable":
                        True,

                    "confidence":
                        0.92,

                    "evidence":
                        evidence

                }


            else:

                evidence.append(

                    "Recovered settlement amount "
                    "does not match payment amount"

                )

                return {

                    "analysis_status":
                        "REFERENCE_RECOVERY_RISKY",

                    "financial_risk":
                        "HIGH",

                    "auto_resolvable":
                        False,

                    "confidence":
                        0.85,

                    "evidence":
                        evidence

                }


        return {

            "analysis_status":
                "REFERENCE_RECOVERY_INSUFFICIENT_DATA",

            "financial_risk":
                "MEDIUM",

            "auto_resolvable":
                False,

            "confidence":
                0.50,

            "evidence":
                evidence

        }


    # =============================================
    # MISSING SETTLEMENT
    # =============================================

    def analyze_missing_settlement(
        self,
        context
    ):

        payment = context.get(
            "payment",
            {}
        )


        evidence = [

            "No settlement record was found "
            "for this payment"

        ]


        if payment:

            evidence.append(

                "Payment record exists and "
                "requires settlement investigation"

            )


        return {

            "analysis_status":
                "SETTLEMENT_MISSING",

            "financial_risk":
                "HIGH",

            "auto_resolvable":
                False,

            "confidence":
                0.90,

            "evidence":
                evidence

        }


    # =============================================
    # DUPLICATE PAYMENT
    # =============================================

    def analyze_duplicate_payment(
        self,
        context
    ):

        return {

            "analysis_status":
                "DUPLICATE_PAYMENT_CONFIRMED",

            "financial_risk":
                "HIGH",

            "auto_resolvable":
                False,

            "confidence":
                0.95,

            "evidence":
                [

                    "Duplicate payment pattern "
                    "detected during reconciliation",

                    "Transaction requires review "
                    "to prevent double processing"

                ]

        }


    # =============================================
    # MISSING ORDER
    # =============================================

    def analyze_missing_order(
        self,
        context
    ):

        return {

            "analysis_status":
                "ORDER_MISSING",

            "financial_risk":
                "HIGH",

            "auto_resolvable":
                False,

            "confidence":
                0.95,

            "evidence":
                [

                    "Payment references an "
                    "order that does not exist",

                    "Order validation failed"

                ]

        }