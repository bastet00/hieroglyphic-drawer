class ComposeHandler:
    def handle_draw_type(self, mdc, spchar_idxs):
        return "compose_up" if mdc[spchar_idxs[0]] == "*" else "compose"


class AmpersandHandler:
    def handle_draw_type(self, mdc, spchar_idxs):
        return "ampersand"


class VerticalDrawHandler:
    def handle_draw_type(self, mdc, spchar_idxs):
        return "vertical_draw"
