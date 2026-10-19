
from engine.models import DataAsset, Destination, Sensitivity
from engine.engine import analyze_flow


def make_asset(name, sensitivity):
    return DataAsset(
        name=name,
        sensitivity=sensitivity,
        description="Fictional test data",
    )


def make_destination(destination_id, name, approved):
    return Destination(
        destination_id=destination_id,
        name=name,
        approved=approved,
        description="Test destination",
    )


# Test 1: Public data -> approved database
def test_public_data_to_approved_database():
    asset = make_asset(
        "Public product information",
        Sensitivity.PUBLIC,
    )
    destination = make_destination(
        "database_1",
        "Approved Database",
        True,
    )

    finding = analyze_flow(asset, destination)

    assert finding is None
    print("Test 1 passed: Public data -> approved database = no finding")


# Test 2: Secret data -> approved database
def test_secret_to_approved_database():
    asset = make_asset(
        "Secret API key",
        Sensitivity.SECRET,
    )
    destination = make_destination(
        "database_1",
        "Approved Database",
        True,
    )

    finding = analyze_flow(asset, destination)

    assert finding is None
    print("Test 2 passed: Secret -> approved database = no finding")


# Test 3: Confidential data -> unapproved logging service
def test_confidential_to_unapproved_logging():
    asset = make_asset(
        "Confidential customer email",
        Sensitivity.CONFIDENTIAL,
    )
    destination = make_destination(
        "logging_1",
        "Public Logging Service",
        False,
    )

    finding = analyze_flow(asset, destination)

    assert finding is not None
    assert finding.severity == "high"
    print("Test 3 passed: Confidential data -> unapproved logging = high")


# Test 4: Secret data -> unapproved external API
def test_secret_to_unapproved_external_api():
    asset = make_asset(
        "Secret API key",
        Sensitivity.SECRET,
    )
    destination = make_destination(
        "external_api_1",
        "Unapproved External API",
        False,
    )

    finding = analyze_flow(asset, destination)

    assert finding is not None
    assert finding.severity == "critical"
    print("Test 4 passed: Secret -> unapproved API = critical")


# Test 5: Internal data -> approved public-only logging service
def test_internal_to_public_only_logging():
    asset = make_asset(
        "Internal company notes",
        Sensitivity.INTERNAL,
    )
    destination = make_destination(
        "logging_1",
        "Public-only Logging Service",
        True,
    )

    finding = analyze_flow(asset, destination)

    assert finding is not None
    assert finding.severity == "medium"
    print("Test 5 passed: Internal data -> public-only logging = medium")
