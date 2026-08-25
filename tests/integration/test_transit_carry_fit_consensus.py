"""Five-validator GLSim flow for multi-leg strictest aggregation."""

import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context(status):
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {"Determine whether one described item": json.dumps({"status": status})}},
    )
    return {"validators": [validator.to_dict() for validator in validators]}


def test_five_validator_leg_assessments_seal_strictest_result():
    traveler_account, first_authority_account, second_authority_account = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "transit_carry_fit.py")
    deployed = factory.deploy_contract_tx(args=[], account=traveler_account, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(deployed)
    address = extract_contract_address(deployed)
    traveler = factory.build_contract(address, account=traveler_account)
    first_authority = factory.build_contract(address, account=first_authority_account)
    second_authority = factory.build_contract(address, account=second_authority_account)
    rule = "Small tools may be carried when enclosed in checked baggage. Loose blades are prohibited, and staff review is required for powered equipment or uncertain items."
    first_rule = f"{str(first_authority_account.address).lower()}:BUS"
    second_rule = f"{str(second_authority_account.address).lower()}:RAIL"
    trip_id = f"{str(traveler_account.address).lower()}:TRIP-1"
    _ok(first_authority.publish_rule(args=["BUS", "Regional Carrier", "City bus leg", rule, "fixture://bus-rule"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(second_authority.publish_rule(args=["RAIL", "Regional Carrier", "Regional rail leg", rule, "fixture://rail-rule"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    itinerary = {"legs": [{"leg_id": "LEG-1", "rule_id": first_rule}, {"leg_id": "LEG-2", "rule_id": second_rule}]}
    _ok(traveler.open_trip(args=["TRIP-1", "One compact hand tool with no blade or battery, enclosed inside a locked checked-baggage case.", itinerary]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(traveler.assess_leg(args=[trip_id, "LEG-1"]).transact(transaction_context=_context("ALLOWED"), wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(traveler.assess_leg(args=[trip_id, "LEG-2"]).transact(transaction_context=_context("RESTRICTED"), wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(traveler.seal_trip(args=[trip_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert traveler.get_trip(args=[trip_id]).call()["strictest_status"] == "RESTRICTED"
