"""
The form for the pop-up box.
"""
import datetime
import tkinter
from typing import Callable


# Private Sub UserForm_Initialize()
#     '''
#     ' Create the pop-up box and add the defaults to the boxes
#     '''
# '    On Error Resume Next
# '        Me.Left = GetSetting("Userform Positioning", ThisWorkbook.FullName & "-" & Me.Name, "Left", 0)
# '        Me.Top = GetSetting("Userform Positioning", ThisWorkbook.FullName & "-" & Me.Name, "Top", 0)
# '    On Error GoTo 0
#
#     Dim sDefaults As String
#     Let pCounter = 0
#
#     With Me
#         Let sDefaults = GetDefaultTaskAndDetail(sTime:=.ScheduleTime)
#
#         ' Position and size
#         .Left = 0: .Top = 0: .Height = 144: .Width = 240
#
#         ' Caption
#         .Caption = "Interval Tracker at " & Me.ScheduleTime & " (" & Me.Interval & ")"
#
#         ' Update the drop-down
#         Call ManageUpcomingTicketsInDropDown
#
#         ' Input boxes
#         .tbxDetail.Value = Mid(sDefaults, 1 + InStr(sDefaults, ","))
#         With Me.cbxProject
#             .List = Split(Me.ProjectDropDownList, ",")
#             .Value = Split(sDefaults, ",")(0)
#
#             ' Select the text within the Project box upon loading
#             .SelStart = 0
#             .SelLength = Len(.text)
#         End With
#     End With
# End Sub


class TrackerForm:
    """
    The pop-up box for the tracker.
    """
    def __init__(self, date_time: datetime.datetime, interval: int, action: Callable):
        """
        Create the form handler.
        """
        self._interval = interval
        self._date_time = date_time
        self._action = action
        self._width = 350
        self._height = 150
        self._root: tkinter.Tk | None = None

    @property
    def date_time(self) -> str:
        """
        Return the pop-up datetime in the hh:mm format.
        """
        return self._date_time.strftime("%H:%M")

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
            text=label_text,
            width=8,  # round(self._width * 0.1)
            borderwidth=2,
            justify="right",
            background="white",
            relief="flat",
        )
        text_box = tkinter.Text(
            master=frame,
            height=1,
            width=30,  # round(self._width * 0.8)
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

        self.create_text_box_frame(master=text_box_frame, label_text="Project")
        self.create_text_box_frame(master=text_box_frame, label_text="Detail")

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
