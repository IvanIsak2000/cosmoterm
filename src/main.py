from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.application.current import get_app

from utils.client import Client
from utils.server import Server
from utils.logger import logger

client_buffer = Buffer()
server_buffer = Buffer()

style = Style.from_dict({
    'title': '#2668CB italic',
    'sended': '#09F247',
    'not_valid_key': '#D52525',
})

server = Server()
server_status = server.get_status()

client_win = Window(BufferControl(buffer=client_buffer))
server_win = Window(BufferControl(buffer=server_buffer))

body = VSplit(
    [ 
        client_win,
        Window(width=1, char="|", style="class:line"),
        server_win,
    ]
)

root_container = HSplit(
    [
        Window(
            height=1,
            content=FormattedTextControl([
                ("class:title", "cosmoterm"),
                ('class:title', server_status),
                ("class:title", " (Press [Ctrl-Q] to quit.)")]),
            align=WindowAlign.CENTER,
        ),
        Window(height=1, char="-", style="class:line"),
        body,
    ]
)

kb = KeyBindings()


@kb.add('c-q', eager=True)
@kb.add('c-c', eager=True)
def _(event):
    event.app.exit()


def add_message_on_server_window(_):
    try:
        while True:
            if server:
                server_buffer.text = server.start()
                server_buffer.cursor_position = len(server_buffer.text)
    except KeyboardInterrupt:
        get_app().exit()
    except Exception as e:
        logger.error(e)
        get_app().exit()


client_buffer.on_text_changed += add_message_on_server_window


application = Application(
    layout=Layout(root_container, focused_element=client_buffer),
    key_bindings=kb,
    mouse_support=True,
    full_screen=True,
)


def run():
    # Run the interface. (This runs the event loop until Ctrl-Q is pressed.)
    application.run()


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        get_app.exit()
    except Exception:
        get_app.exit()
