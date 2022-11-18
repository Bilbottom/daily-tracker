"""
The form for the pop-up box.

https://youtu.be/5qOnzF7RsNA
"""
import datetime
import tkinter as tk

import daily_tracker.actions


STYLE = {
    "font": ("Tahoma", 8),
}
OPTIONS = ["Item 1", "Item 2", "Item 3"]


class TrackerForm:
    """
    The pop-up box for the tracker.
    """
    def __init__(
        self,
        at_datetime: datetime.datetime,
        interval: int,
    ):
        """
        Create the form handler.
        """
        self.interval = interval
        self.at_datetime = at_datetime
        self.task = "This is the task value"
        self.detail = "This is the detail value"
        self.action_handler = daily_tracker.actions.ActionHandler(form=self)
        self._width = 350
        self._height = 150
        # self._top = 0
        # self._left = 0
        self._root: tk.Tk | None = None
        self.project_text_box: TextBox | None = None
        self.detail_text_box: TextBox | None = None
        # self._root.mainloop()
        # Add properties like `is_meeting` and `is_jira_ticket`?

    @property
    def date_time(self) -> str:
        """
        Return the pop-up datetime in the hh:mm format.
        """
        return self.at_datetime.strftime("%H:%M")

    def action_wrapper(self) -> None:
        """
        Wrap the action so that we can schedule the next event when it's called.
        """
        self.action_handler.ok_button_actions()
        print(  # Need to get the class properties looking at the Entry, not the Frame
            f"Project: {self.project_text_box.text_box.get()}\n",
            f"Detail: {self.detail_text_box.text_box.get()}",
        )
        self._root.destroy()

    def on_project_change(self) -> None:
        """
        When the value of the Project box changes, update the Detail box with
        the latest value from the Project.
        """
        pass

    def ok_shortcut(self, event: tk.Event) -> None:
        """
        Enable keyboard shortcut CTRL + ENTER to the OK button.

        https://youtu.be/ibf5cx221hk
        """
        if event.state == 12 and event.keysym == "Return":
            self.action_wrapper()

    def generate_form(self) -> None:
        """
        Generate the tracker pop-up form.
        """
        self._root = tk.Tk()
        self._root.geometry(f"{self._width}x{self._height}")
        self._root.eval("tk::PlaceWindow . center")  # Middle of screen
        self._root.title(f"Interval Tracker at {self.date_time} ({self.interval})")

        text_box_frame_outer = tk.Frame(
            self._root,
            background="white",
        )
        text_box_frame_outer.pack(
            in_=self._root,
            fill="both",
            expand=tk.YES,
        )

        text_box_frame = tk.LabelFrame(
            self._root,
            text="Current Task Details",
            borderwidth=2,
            background="white",
            font=STYLE["font"],
        )
        text_box_frame.pack(
            # in_=self._root,
            in_=text_box_frame_outer,
            fill="both",
            expand=tk.YES,
            side=tk.TOP,
            padx=10,
            pady=10,
        )

        button_frame = tk.Frame(
            self._root,
            borderwidth=15,
        )
        button_frame.pack(
            in_=self._root,
            side=tk.BOTTOM,
            fill=tk.BOTH,
            expand=True,
        )

        self.project_text_box = TextBox(text_box_frame, "Project")
        self.detail_text_box = TextBox(text_box_frame, "Detail")

        self.project_text_box.text_box.bind("<KeyPress>", self.ok_shortcut)
        self.detail_text_box.text_box.bind("<KeyPress>", self.ok_shortcut)

        okay_button = tk.Button(
            self._root,
            height=2,
            width=20,
            borderwidth=3,
            text="OK",
            command=self.action_wrapper,
            font=STYLE["font"],
        )
        okay_button.pack(
            in_=button_frame,
            side=tk.LEFT,
        )

        cancel_button = tk.Button(
            self._root,
            height=2,
            width=20,
            borderwidth=3,
            text="Cancel",
            command=lambda: self._root.destroy(),
            font=STYLE["font"],
        )
        cancel_button.pack(
            in_=button_frame,
            side=tk.RIGHT,
        )

        self._root.mainloop()


class TextBox:
    """
    A text box with a label for the main form.
    """
    def __init__(self, parent: tk.Misc, label_text: str):
        """
        Set the text box properties and create the widget.
        """
        self.parent = parent
        self.label_text = label_text
        self.frame = self._build()

        self.variable: str
        self.text_box: tk.Entry

    def _build(self) -> tk.Frame:
        """
        Build the text box and return it.
        """
        frame = tk.Frame(self.parent, background="white")
        inner = tk.Frame(self.parent, background="white")
        label = tk.Label(
            master=inner,
            height=1,
            width=8,
            borderwidth=2,
            text=self.label_text,
            justify="right",
            background="white",
            relief="flat",
            font=STYLE["font"],
        )
        text_box_value = tk.StringVar(inner)
        text_box_value.set("Select an option...")
        self.variable = text_box_value

        text_box = tk.Entry(
            master=inner,
            textvariable=text_box_value,
            width=40,
            borderwidth=2,
            font=STYLE["font"],
        )
        # text_box = tk.OptionMenu(
        #     inner,
        #     text_box_value,
        #     *OPTIONS,
        # )
        self.text_box = text_box

        label.pack(in_=inner, side=tk.LEFT)
        text_box.pack(in_=inner, side=tk.RIGHT)
        inner.pack(in_=frame, pady=4)
        frame.pack(in_=self.parent)

        return frame
