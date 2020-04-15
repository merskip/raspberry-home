from raspberry_home.controller.input_controls import InputControls


class InputController(InputControls.Listener):

    def on_clicked_button(self, index: int):
        print("Selected %d" % index)
