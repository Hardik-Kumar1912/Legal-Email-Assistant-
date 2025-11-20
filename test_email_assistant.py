import unittest
from email_assistant import analyze_email, draft_reply

class TestLegalAssistant(unittest.TestCase):
    """
    Unit tests for the Legal Email Assistant modules.
    """

    def setUp(self):
        # Test data setup
        self.sample_email_input = """
        Subject: Urgent: Termination Question
        From: Client X
        Date: 20 Nov 2025
        
        We need to terminate our agreement with Vendor Y dated 15 Jan 2024 due to repeated failures in delivery.
        Can we terminate immediately for cause?
        """
        
        self.sample_contract_snippet = """
        Clause 8.1: Immediate termination is permitted for material breach.
        Clause 8.2: Repeated delivery failure is a material breach.
        """

    def test_analyze_email_structure(self):
        """
        Verifies that analyze_email returns a dictionary with the required JSON schema keys.
        """
        result = analyze_email(self.sample_email_input)
        
        # Check strictly for type
        self.assertIsInstance(result, dict, "Analysis result must be a dictionary")
        
        # Check for required schema keys
        required_fields = [
            "intent", 
            "primary_topic", 
            "parties", 
            "agreement_reference", 
            "questions"
        ]
        
        for field in required_fields:
            self.assertIn(field, result, f"Missing required key: {field}")

        # Check specific nested fields
        self.assertIn("client", result["parties"])
        self.assertIn("counterparty", result["parties"])

    def test_draft_reply_generation(self):
        """
        Verifies that draft_reply returns a non-empty string containing key elements.
        """
        # Mock analysis output to isolate the drafting test
        mock_analysis_data = {
            "intent": "legal_advice",
            "parties": {
                "client": "Client X",
                "counterparty": "Vendor Y"
            },
            "questions": ["Can we terminate immediately?"]
        }

        reply = draft_reply(
            self.sample_email_input, 
            mock_analysis_data, 
            self.sample_contract_snippet
        )

        # Assertions
        self.assertIsInstance(reply, str)
        self.assertTrue(len(reply) > 50, "Generated reply is too short")
        self.assertIn("Vendor Y", reply, "Reply should reference the counterparty")
        self.assertIn("8.1", reply, "Reply should cite the relevant contract clause")

if __name__ == '__main__':
    unittest.main()