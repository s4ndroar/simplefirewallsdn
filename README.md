

*Execution:* 
* To run the program
`python main.py`

* To run the unit test case
  `python -m unittest test/test_controller.py`

Features:
1. Dynamic port rule management
2. Event-based policy tracking
3. Event logging
4. Event replay capabilities

* Components:
```
1. Event: Base event class
2. Policy: Manages allowed ports and rule application
3. EventStore: Tracks and replays events
4. SDNController: Central controller for firewall
```

Requirements
* Python 3.7+ Recommendation: (tested in 3.12.6)
* No external dependencies required

