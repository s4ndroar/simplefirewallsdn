from controller import SDNController

if __name__ == "__main__":
    controller = SDNController()

    #Initialization - Default Firewall state
    controller.add_rule(22)
    controller.add_rule(80)

    controller.process_traffic("192.168.1.10", 22)
    controller.process_traffic("192.168.1.10", 23)

    controller.add_rule(23)
    controller.process_traffic("192.168.1.10",23)

    controller.remove_rule(80)
    controller.process_traffic("192.168.1.10", 80)

    print(f"Replay events")
    controller.replay_policy()
    controller.process_traffic("192.168.1.10",80)