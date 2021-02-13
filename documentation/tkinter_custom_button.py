import tkinter
import sys


class TkinterCustomButton(tkinter.Frame):
    """ tkinter custom button with border, rounded corners and hover effect """

    def __init__(self,
                 bg_color=None,
                 fg_color=None,
                 hover_color=None,
                 border_color=None,
                 border_width=0,
                 command=None,
                 width=50,
                 height=20,
                 corner_radius=4,
                 text_font=("Arial", 10),
                 text_color="white",
                 text="",
                 hover=True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        if bg_color is None:
            self.bg_color = self.master.cget("bg")
        else:
            self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.border_color = border_color

        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.border_width = border_width
        if self.corner_radius >= self.border_width:
            self.inner_corner_radius = self.corner_radius - self.border_width
        else:
            self.inner_corner_radius = 0

        self.text = text
        self.text_font = text_font
        self.text_color = text_color

        self.function = command
        self.hover = hover

        self.configure(width=self.width, height=self.height)

        if sys.platform == "darwin" and self.function is not None:
            self.configure(cursor="pointinghand")

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     background=self.bg_color,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(x=0, y=0)

        if self.hover is True:
            self.canvas.bind("<Enter>", self.on_enter)
            self.canvas.bind("<Leave>", self.on_leave)

        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<Button-1>", self.clicked)

        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.text_part = None

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.canvas.configure(bg=self.bg_color)

        # border button parts

        self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                0,
                                                                self.corner_radius * 2,
                                                                self.corner_radius * 2))
        self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                0,
                                                                self.width,
                                                                self.corner_radius * 2))
        self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                self.height - self.corner_radius * 2,
                                                                self.corner_radius * 2,
                                                                self.height))
        self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                self.height - self.corner_radius * 2,
                                                                self.width,
                                                                self.height))

        self.canvas_border_parts.append(self.canvas.create_rectangle(0,
                                                                     self.corner_radius,
                                                                     self.width,
                                                                     self.height - self.corner_radius))
        self.canvas_border_parts.append(self.canvas.create_rectangle(self.corner_radius,
                                                                     0,
                                                                     self.width - self.corner_radius,
                                                                     self.height))

        # inner button parts

        self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                            self.border_width,
                                                            self.border_width + self.inner_corner_radius * 2,
                                                            self.border_width + self.inner_corner_radius * 2))
        self.canvas_fg_parts.append(self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                                            self.border_width,
                                                            self.width - self.border_width,
                                                            self.border_width + self.inner_corner_radius * 2))
        self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                            self.height - self.border_width - self.inner_corner_radius * 2,
                                                            self.border_width + self.inner_corner_radius * 2,
                                                            self.height-self.border_width))
        self.canvas_fg_parts.append(self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                                            self.height - self.border_width - self.inner_corner_radius * 2,
                                                            self.width - self.border_width,
                                                            self.height - self.border_width))

        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width + self.inner_corner_radius,
                                                                 self.border_width,
                                                                 self.width - self.border_width - self.inner_corner_radius,
                                                                 self.height - self.border_width))
        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width,
                                                                 self.border_width + self.inner_corner_radius,
                                                                 self.width - self.border_width,
                                                                 self.height - self.inner_corner_radius - self.border_width))

        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.fg_color, outline=self.fg_color, width=0)

        for part in self.canvas_border_parts:
            self.canvas.itemconfig(part, fill=self.border_color, outline=self.border_color, width=0)

        self.text_part = self.canvas.create_text(self.width / 2,
                                                 self.height / 2,
                                                 text=self.text,
                                                 font=self.text_font,
                                                 fill=self.text_color)

        self.set_text(self.text)

    def configure_color(self, bg_color=None, fg_color=None, hover_color=None, text_color=None):
        if bg_color is not None:
            self.bg_color = bg_color

        if fg_color is not None:
            self.fg_color = fg_color

        if hover_color is not None:
            self.hover_color = hover_color

        if text_color is not None:
            self.text_color = text_color
            self.canvas.itemconfig(self.text_part, fill=self.text_color)

        self.draw()

    def set_text(self, text):
        self.canvas.itemconfig(self.text_part, text=text)

    def on_enter(self, event=0):
        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.hover_color, outline=self.hover_color)

    def on_leave(self, event=0):
        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.fg_color, outline=self.fg_color)

    def clicked(self, event=0):
        if self.function is not None:
            self.function()
            self.on_leave()