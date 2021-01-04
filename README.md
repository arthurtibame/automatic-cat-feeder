# Automatic cat feeder (updated on 04/01/2021)

## Structure of framework
Raspberry Pi server
```cmd
├── Dockerfile
├── HX711
│   ├── all_methods_example.py
│   ├── example.py
│   ├── example_save_state.py
│   ├── hx711.py
│   ├── simple_example.py
│   └── swap_file.swp
├── SG90
│   └── test.py
├── hx711.py
├── main.py
├── requirements.txt
├── settings.py
└── utils
    ├── __init__.py
    ├── google_api.py
    ├── scale.py
    ├── secret.json
    ├── sg_motor.py
    └── swap_file.swp
```

Line Chatbot server
```cmd
├── README.md
└── automatic_feeder_line_chatbot.gs
```
---
## ToDo List (Raspberry pi)
- [x] enable to use the scale
- [x] connect to google api
- [x] scale model
- [x] motor model
- [ ] design outward of feeder

## TODO List (Line chatbot)
- [x] User Registration
- [x] Save Files from user
- [ ] Automatic Push daily report message 
- [ ] Rich Menu
- [ ] Flex Message
- [ ] Weekly, Monthly report visualized with Python server
