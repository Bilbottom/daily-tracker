"""
The form for the pop-up box.
"""
import datetime
import tkinter
from typing import Callable


class TextBox:
    """
    A text box with a label for the main form.
    """
    def __init__(self, parent: tkinter.Misc, label_text: str):
        self.parent = parent
        self.label_text = label_text

        self.frame = self._build()

    def _build(self) -> tkinter.Frame:
        """
        Build the text box and return it.
        """
        frame = tkinter.Frame(self.parent)
        label = tkinter.Label(
            master=frame,
            height=1,
            width=8,
            borderwidth=2,
            text=self.label_text,
            justify="right",
            background="white",
            relief="flat",
        )
        text_box = tkinter.Text(
            master=frame,
            height=1,
            width=30,
            borderwidth=2,
        )

        label.pack(in_=frame, side=tkinter.LEFT)
        text_box.pack(in_=frame, side=tkinter.RIGHT)
        frame.pack(in_=self.parent)

        return frame


class TrackerForm:
    """
    The pop-up box for the tracker.
    """
    def __init__(self, at_datetime: datetime.datetime, interval: int, action: Callable):
        """
        Create the form handler.
        """
        self._interval = interval
        self._at_datetime = at_datetime
        self._action = action
        self._width = 350
        self._height = 150
        # self._top = 0
        # self._left = 0
        self._root: tkinter.Tk | None = None
        self.project_text_box: TextBox | None = None
        self.detail_text_box: TextBox | None = None

    @property
    def date_time(self) -> str:
        """
        Return the pop-up datetime in the hh:mm format.
        """
        return self._at_datetime.strftime("%H:%M")

    def action_wrapper(self) -> None:
        """
        Wrap the action so that we can schedule the next event when it's called.
        """
        self._action()
        self._root.destroy()

    def on_project_change(self) -> None:
        """
        When the value of the Project box changes, update the Detail box with
        the latest value from the Project.
        """
        pass

    def create_text_box_frame(self, master: tkinter.Misc, label_text: str) -> tkinter.Frame:
        """
        Generate a frame that has a label and a textbox.
        """
        frame = tkinter.Frame(master)
        label = tkinter.Label(
            master=frame,
            height=1,
            width=round(self._width * 0.02),
            borderwidth=2,
            text=label_text,
            justify="right",
            background="white",
            relief="flat",
        )
        text_box = tkinter.Text(
            master=frame,
            height=1,
            width=round(self._width * 0.09),
            borderwidth=2,
        )

        label.pack(in_=frame, side=tkinter.LEFT)
        text_box.pack(in_=frame, side=tkinter.RIGHT)
        frame.pack(in_=master)

        return frame

    def generate_form(self) -> None:
        """
        Generate the tracker pop-up form.
        """
        self._root = tkinter.Tk()
        self._root.geometry(f"{self._width}x{self._height}")
        self._root.title(f"Interval Tracker at {self.date_time} ({self._interval})")

        text_box_frame = tkinter.LabelFrame(
            self._root,
            text="Current Task Details",
            borderwidth=2,
            background="white",
        )
        text_box_frame.pack(
            in_=self._root,
            fill="both",
            expand=tkinter.YES,
            side=tkinter.TOP,
        )

        button_frame = tkinter.Frame(
            self._root,
            borderwidth=15,
        )
        button_frame.pack(
            in_=self._root,
            side=tkinter.BOTTOM,
            fill=tkinter.BOTH,
            expand=True,
        )

        # self.create_text_box_frame(master=text_box_frame, label_text="Project")
        # self.create_text_box_frame(master=text_box_frame, label_text="Detail")
        # TextBox(text_box_frame, "Project").pack()
        # TextBox(text_box_frame, "Detail").pack()
        self.project_text_box = TextBox(text_box_frame, "Project")
        self.detail_text_box = TextBox(text_box_frame, "Detail")

        okay_button = tkinter.Button(
            self._root,
            height=2,
            width=20,
            borderwidth=3,
            text="OK",
            command=self.action_wrapper,
        )
        okay_button.pack(
            in_=button_frame,
            side=tkinter.LEFT,
        )

        cancel_button = tkinter.Button(
            self._root,
            height=2,
            width=20,
            borderwidth=3,
            text="Cancel",
            command=lambda: self._root.destroy(),
        )
        cancel_button.pack(
            in_=button_frame,
            side=tkinter.RIGHT,
        )

        self._root.mainloop()
