"""Direct tests for per-leg rule evaluation and strictest aggregation."""

import json


RULE = "Small tools may be carried when enclosed in checked baggage. Loose blades are prohibited, and staff review is required for powered equipment or uncertain items."
ITEM = "One compact hand tool with no blade or battery, enclosed inside a locked checked-baggage case."


def _rule(contract, direct_vm, publisher, key, route):
    direct_vm.sender = publisher
    return contract.publish_rule(key, "Regional Carrier", route, RULE, "fixture://carrier-rule")


def _trip(contract, direct_vm, traveler, rules):
    direct_vm.sender = traveler
    itinerary = {"legs": [{"leg_id": f"LEG-{index + 1}", "rule_id": rule_id} for index, rule_id in enumerate(rules)]}
    return contract.open_trip("TRIP-1", ITEM, itinerary)


def _assess(contract, direct_vm, traveler, trip_id, leg_id, status):
    direct_vm.sender = traveler
    direct_vm.clear_mocks()
    direct_vm.mock_llm(r".*Determine whether one described item.*", json.dumps({"status": status}))
    contract.assess_leg(trip_id, leg_id)


def test_rule_publisher_can_retire_snapshot(contract, direct_vm, direct_bob):
    rule_id = _rule(contract, direct_vm, direct_bob, "BUS", "City bus leg")
    contract.retire_rule(rule_id)
    assert contract.get_rule(rule_id)["active"] is False


def test_retired_rule_cannot_enter_new_trip(contract, direct_vm, direct_alice, direct_bob):
    rule_id = _rule(contract, direct_vm, direct_bob, "BUS", "City bus leg")
    contract.retire_rule(rule_id)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("itinerary_uses_retired_rule"):
        contract.open_trip("BAD", ITEM, {"legs": [{"leg_id": "LEG-1", "rule_id": rule_id}]})


def test_each_leg_is_evaluated_and_strictest_status_seals(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    first = _rule(contract, direct_vm, direct_bob, "BUS", "City bus leg")
    second = _rule(contract, direct_vm, direct_charlie, "RAIL", "Regional rail leg")
    trip_id = _trip(contract, direct_vm, direct_alice, [first, second])
    _assess(contract, direct_vm, direct_alice, trip_id, "LEG-1", "ALLOWED")
    _assess(contract, direct_vm, direct_alice, trip_id, "LEG-2", "RESTRICTED")
    contract.seal_trip(trip_id)
    trip = contract.get_trip(trip_id)
    assert trip["status"] == "SEALED"
    assert trip["strictest_status"] == "RESTRICTED"


def test_trip_cannot_seal_with_pending_leg(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    first = _rule(contract, direct_vm, direct_bob, "BUS", "City bus leg")
    second = _rule(contract, direct_vm, direct_charlie, "RAIL", "Regional rail leg")
    trip_id = _trip(contract, direct_vm, direct_alice, [first, second])
    _assess(contract, direct_vm, direct_alice, trip_id, "LEG-1", "ALLOWED")
    with direct_vm.expect_revert("unassessed_leg"):
        contract.seal_trip(trip_id)


def test_only_traveler_can_assess(contract, direct_vm, direct_alice, direct_bob):
    rule_id = _rule(contract, direct_vm, direct_bob, "BUS", "City bus leg")
    trip_id = _trip(contract, direct_vm, direct_alice, [rule_id])
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_traveler"):
        contract.assess_leg(trip_id, "LEG-1")


def test_duplicate_leg_identifier_is_rejected(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    first = _rule(contract, direct_vm, direct_bob, "BUS", "City bus leg")
    second = _rule(contract, direct_vm, direct_charlie, "RAIL", "Regional rail leg")
    direct_vm.sender = direct_alice
    itinerary = {"legs": [{"leg_id": "SAME", "rule_id": first}, {"leg_id": "SAME", "rule_id": second}]}
    with direct_vm.expect_revert("duplicate_leg_id"):
        contract.open_trip("BAD", ITEM, itinerary)


def test_unknown_model_status_fails_without_leg_mutation(contract, direct_vm, direct_alice, direct_bob):
    rule_id = _rule(contract, direct_vm, direct_bob, "BUS", "City bus leg")
    trip_id = _trip(contract, direct_vm, direct_alice, [rule_id])
    direct_vm.mock_llm(r".*Determine whether one described item.*", json.dumps({"status": "MAYBE"}))
    with direct_vm.expect_revert("invalid_status"):
        contract.assess_leg(trip_id, "LEG-1")
    assert contract.get_trip(trip_id)["legs"][0]["status"] == "PENDING"
