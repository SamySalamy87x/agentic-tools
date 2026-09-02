import unittest

from followthrough.core import build_decision_packet, evidence_checklist, missing_evidence, policy_gate


class FollowThroughCoreTests(unittest.TestCase):
    def test_proposal_checklist_contains_required_fields(self):
        fields = evidence_checklist("proposal_followup")
        self.assertIn("scope_status", fields)
        self.assertIn("latest_proposal_version", fields)
        self.assertIn("deadline", fields)

    def test_missing_evidence_is_explicit(self):
        required = ["requester", "deadline", "recipient"]
        available = {"requester": "A", "deadline": "2026-09-10", "recipient": ""}
        self.assertEqual(missing_evidence(required, available), ["recipient"])

    def test_low_risk_followup_is_allowed(self):
        decision = policy_gate("request_missing_information")
        self.assertTrue(decision.allowed)
        self.assertFalse(decision.escalation_required)

    def test_payment_is_blocked(self):
        decision = policy_gate("payment", authority_confirmed=True)
        self.assertFalse(decision.allowed)
        self.assertTrue(decision.escalation_required)

    def test_unknown_action_escalates_without_authority(self):
        decision = policy_gate("publish_external_record")
        self.assertFalse(decision.allowed)
        self.assertTrue(decision.escalation_required)

    def test_decision_packet_requires_human_when_evidence_missing(self):
        packet = build_decision_packet(
            "Resend proposal",
            {"requester": "A", "deadline": "2026-09-10"},
            ["requester", "deadline", "recipient"],
            "send_followup",
        )
        self.assertEqual(packet["missing_fields"], ["recipient"])
        self.assertTrue(packet["human_decision_required"])
        self.assertFalse(packet["ready_for_low_risk_action"])


if __name__ == "__main__":
    unittest.main()
