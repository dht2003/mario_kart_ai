from controller import ControllerState


def main():
    cs = ControllerState()
    state = [1, -1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    cs.load_state(state)
    while True:
        cs.emulate_outputs()


if __name__ == "__main__":
    main()
