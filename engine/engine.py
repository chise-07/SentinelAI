
from engine.models import (
    DataAsset,
    Destination,
    Finding,
    Sensitivity,
)


SEVERITY_BY_SENSITIVITY = {
    Sensitivity.PUBLIC: "low",
    Sensitivity.INTERNAL: "medium",
    Sensitivity.CONFIDENTIAL: "high",
    Sensitivity.SECRET: "critical",
}


# Define the maximum sensitivity each destination may receive.
# These are simulated policies for the LeakPath prototype.
MAX_SENSITIVITY_BY_DESTINATION = {
    "database_1": Sensitivity.SECRET,
    "external_api_1": None,
    "logging_1": Sensitivity.PUBLIC,
}


def analyze_flow(
    asset: DataAsset,
    destination: Destination,
) -> Finding | None:
    """
    Analyze a simulated data flow.

    Detect:
    1. Data sent to an unapproved destination.
    2. Data exceeding a destination's sensitivity allowance.
    """

    sensitivity_order = {
        Sensitivity.PUBLIC: 0,
        Sensitivity.INTERNAL: 1,
        Sensitivity.CONFIDENTIAL: 2,
        Sensitivity.SECRET: 3,
    }

    # Rule 1: Never allow a flow to an unapproved destination.
    if not destination.approved:
        severity = SEVERITY_BY_SENSITIVITY[asset.sensitivity]

        return Finding(
            asset_name=asset.name,
            destination_name=destination.name,
            severity=severity,
            message=(
                f"{asset.sensitivity.value.title()} data "
                f"'{asset.name}' was sent to unapproved destination "
                f"'{destination.name}'."
            ),
        )

    # Rule 2: Check whether an approved destination is suitable
    # for the sensitivity of the selected data.
    maximum_sensitivity = MAX_SENSITIVITY_BY_DESTINATION.get(
        destination.destination_id
    )

    # Unknown destinations have no configured sensitivity allowance.
    if maximum_sensitivity is None:
        severity = SEVERITY_BY_SENSITIVITY[asset.sensitivity]

        return Finding(
            asset_name=asset.name,
            destination_name=destination.name,
            severity=severity,
            message=(
                f"Data '{asset.name}' cannot be verified as safe "
                f"for destination '{destination.name}' because "
                "its sensitivity allowance is not configured."
            ),
        )

    if (
        sensitivity_order[asset.sensitivity]
        > sensitivity_order[maximum_sensitivity]
    ):
        severity = SEVERITY_BY_SENSITIVITY[asset.sensitivity]

        return Finding(
            asset_name=asset.name,
            destination_name=destination.name,
            severity=severity,
            message=(
                f"{asset.sensitivity.value.title()} data "
                f"'{asset.name}' exceeds the maximum permitted "
                f"sensitivity for destination '{destination.name}'."
            ),
        )

    # No violation found by the currently configured rules.
    return None
