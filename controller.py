class Event:
    pass

class RuleAdded(Event):
    def __init__(self, port):
        self.port = port

class RuleRemoved(Event):
    def __init__(self, port):
        self.port = port

class TrafficReceived(Event):
    def __init__(self, source_ip, port):
        self.source_ip = source_ip
        self.port = port

class TrafficAllowed(Event):
    def __init__(self, source_ip, port):
        self.source_ip = source_ip
        self.port = port

class TrafficBlocked(Event):
    def __init__(self, source_ip, port):
        self.source_ip = source_ip
        self.port = port

#Current state of the port rules
class Policy:
    def __init__(self):
        self.allowed_ports = set()

    def apply_event(self, event):
        if isinstance(event,RuleAdded):
            self.allowed_ports.add(event.port)
        elif isinstance(event, RuleRemoved):
            self.allowed_ports.discard(event.port)

    def is_allowed(self, port):
        return port in self.allowed_ports

#in-memoery event store for replay
class EventStore:
    def __init__(self):
        self.events = []

    def record_event(self, event):
        self.events.append(event)

    def replay_events(self, policy):
        for event in self.events:
            print(f"Replaying event: {event.__class__.__name__} with data {vars(event)}")  # Log each event
            policy.apply_event(event)

class SDNController:
    def __init__(self):
        self.event_store = EventStore()
        self.policy = Policy()

    def add_rule(self, port):
        event = RuleAdded(port)
        self.event_store.record_event(event)
        self.policy.apply_event(event)

    def remove_rule(self, port):
        event = RuleRemoved(port)
        self.event_store.record_event(event)
        self.policy.apply_event(event)

    def process_traffic(self, source_ip, port):
        event = TrafficReceived(source_ip, port)
        print(f"Traffic Received on: {source_ip}, Port {port}")
        self.event_store.record_event(event)

        if self.policy.is_allowed(port):
            result_event = TrafficAllowed(source_ip,port)
            print(f"Traffic Allowed for: {source_ip}, Port {port}")
        else:
            result_event = TrafficBlocked(source_ip,port)
            print(f"Traffic Blocked for: {source_ip}, Port {port}")

        self.event_store.record_event(result_event)

    #Replay event
    def replay_policy(self):
        self.policy = Policy()
        self.event_store.replay_events(self.policy)
