class ComposeHandler:
    def handle_draw_type(self, mdc, spchar_idxs):
        return "compose_up" if mdc[spchar_idxs[0]] == "*" else "compose"


class SecondOnTopHandler:
    def handle_draw_type(self, mdc, spchar_idxs):
        return "second_on_top"


class VerticalDrawHandler:
    def handle_draw_type(self, mdc, spchar_idxs):
        return "vertical_draw"
