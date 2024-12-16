import unittest
from controller import SDNController,RuleAdded,RuleRemoved,TrafficAllowed,TrafficReceived,TrafficBlocked

class TestSDNController(unittest.TestCase):

    def setUp(self):
        self.controller = SDNController()

    def test_add_rule(self):
        self.controller.add_rule(22)
        self.assertIn(22,self.controller.policy.allowed_ports)

    def test_remove_rule(self):
        self.controller.add_rule(22)
        self.controller.remove_rule(22)
        self.assertNotIn(22,self.controller.policy.allowed_ports)

    def test_process_traffic_allowed(self):
        self.controller.add_rule(80)
        self.controller.process_traffic("192.168.1.10",80)
        last_event = self.controller.event_store.events[-1]
        self.assertIsInstance(last_event,TrafficAllowed)
        self.assertEqual(last_event.source_ip,"192.168.1.10")
        self.assertEqual(last_event.port,80)

    def test_process_traffic_blocked(self):
        self.controller.process_traffic("192.168.1.10",23)
        last_event = self.controller.event_store.events[-1]
        self.assertIsInstance(last_event,TrafficBlocked)
        self.assertEqual(last_event.source_ip,"192.168.1.10")
        self.assertEqual(last_event.port,23)

    def test_replay_policy(self):
        self.controller.add_rule(22)
        self.controller.add_rule(80)
        self.controller.remove_rule(22)
        # replay event
        self.controller.replay_policy()
        self.assertNotIn(22, self.controller.policy.allowed_ports)
        self.assertIn(80, self.controller.policy.allowed_ports)

if __name__ == "__main__":
    unittest.main()