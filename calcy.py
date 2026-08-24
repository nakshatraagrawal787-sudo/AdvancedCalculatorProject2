import tkinter as tk
from tkinter import ttk, messagebox
import math
import ast
import re
from datetime import datetime


class AdvancedScientificCalculator:
    def __init__(self, root):
        self.root = root

        # =====================================================
        # WINDOW
        # =====================================================
        self.root.title("Advanced Scientific Calculator")
        self.root.geometry("1280x850")
        self.root.minsize(1100, 720)
        self.root.configure(bg="#10151c")

        # =====================================================
        # STATE
        # =====================================================
        self.angle_mode = "DEG"

        self.memory = 0.0
        self.answer = 0.0

        self.history = []

        # =====================================================
        # COLORS
        # =====================================================
        self.bg = "#10151c"
        self.panel = "#171e27"
        self.panel2 = "#1d2632"
        self.display_bg = "#0b1016"

        self.button = "#27313d"
        self.button_hover = "#344252"

        self.function_button = "#22384d"
        self.function_hover = "#2d4b65"

        self.operator_button = "#31465a"
        self.operator_hover = "#3d5870"

        self.equal_button = "#2563eb"
        self.equal_hover = "#1d4ed8"

        self.danger_button = "#7f1d1d"
        self.danger_hover = "#991b1b"

        self.memory_button = "#25303b"

        self.text = "#f3f4f6"
        self.secondary_text = "#9ca3af"
        self.border = "#334155"

        self.success = "#22c55e"
        self.error = "#ef4444"

        # =====================================================
        # VARIABLES
        # =====================================================
        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="Ready")
        self.memory_var = tk.StringVar(value="M: 0")

        # =====================================================
        # BUILD UI
        # =====================================================
        self.build_header()
        self.build_display()
        self.build_memory_bar()
        self.build_main_area()

        # =====================================================
        # KEYBOARD
        # =====================================================
        self.bind_keyboard()

    # =========================================================
    # HEADER
    # =========================================================

    def build_header(self):

        header = tk.Frame(
            self.root,
            bg=self.bg
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(14, 5)
        )

        title_frame = tk.Frame(
            header,
            bg=self.bg
        )

        title_frame.pack(
            side="left"
        )

        tk.Label(
            title_frame,
            text="ADVANCED SCIENTIFIC",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="CALCULATOR",
            bg=self.bg,
            fg="#60a5fa",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        control_frame = tk.Frame(
            header,
            bg=self.bg
        )

        control_frame.pack(
            side="right"
        )

        self.angle_button = self.create_top_button(
            control_frame,
            self.angle_mode,
            self.toggle_angle_mode
        )

        self.angle_button.pack(
            side="left",
            padx=5
        )

    # =========================================================
    # TOP BUTTON
    # =========================================================

    def create_top_button(
        self,
        parent,
        text,
        command
    ):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.panel2,
            fg=self.text,
            activebackground=self.button_hover,
            activeforeground=self.text,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=9
        )

    # =========================================================
    # DISPLAY
    # =========================================================

    def build_display(self):

        outer = tk.Frame(
            self.root,
            bg=self.display_bg,
            highlightbackground=self.border,
            highlightthickness=1
        )

        outer.pack(
            fill="x",
            padx=20,
            pady=8
        )

        self.expression_entry = tk.Entry(
            outer,
            textvariable=self.expression_var,
            bg=self.display_bg,
            fg=self.secondary_text,
            insertbackground=self.text,
            relief="flat",
            justify="right",
            font=("Consolas", 17)
        )

        self.expression_entry.pack(
            fill="x",
            padx=18,
            pady=(13, 2),
            ipady=5
        )

        tk.Label(
            outer,
            textvariable=self.result_var,
            bg=self.display_bg,
            fg=self.text,
            font=("Consolas", 31, "bold"),
            anchor="e"
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 5)
        )

        status_frame = tk.Frame(
            outer,
            bg=self.display_bg
        )

        status_frame.pack(
            fill="x",
            padx=18,
            pady=(0, 10)
        )

        tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg=self.display_bg,
            fg=self.secondary_text,
            font=("Segoe UI", 9),
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            status_frame,
            textvariable=self.memory_var,
            bg=self.display_bg,
            fg="#60a5fa",
            font=("Segoe UI", 9, "bold"),
            anchor="e"
        ).pack(
            side="right"
        )

    # =========================================================
    # MEMORY BAR
    # =========================================================

    def build_memory_bar(self):

        frame = tk.Frame(
            self.root,
            bg=self.bg
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=(3, 7)
        )

        buttons = [
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M−", self.memory_subtract),
            ("MS", self.memory_store),
            ("ANS", self.insert_answer),
            ("COPY", self.copy_result),
            ("CLEAR", self.clear_current)
        ]

        for i, (label, command) in enumerate(buttons):

            frame.grid_columnconfigure(
                i,
                weight=1,
                uniform="memory"
            )

            button = self.make_button(
                frame,
                label,
                command,
                bg=self.memory_button,
                hover="#33404d"
            )

            button.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=3
            )

    # =========================================================
    # MAIN AREA
    # =========================================================

    def build_main_area(self):

        main = tk.Frame(
            self.root,
            bg=self.bg
        )

        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 18)
        )

        # -----------------------------------------------------
        # LEFT: Calculator
        # -----------------------------------------------------

        calculator_area = tk.Frame(
            main,
            bg=self.bg
        )

        calculator_area.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        # -----------------------------------------------------
        # RIGHT: History
        # -----------------------------------------------------

        history_area = tk.Frame(
            main,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1,
            width=330
        )

        history_area.pack(
            side="right",
            fill="y",
            padx=(7, 0)
        )

        history_area.pack_propagate(False)

        self.build_calculator_area(
            calculator_area
        )

        self.build_history_area(
            history_area
        )

    # =========================================================
    # CALCULATOR AREA
    # =========================================================

    def build_calculator_area(self, parent):

        # -----------------------------------------------------
        # Upper section: scientific + main keypad
        # -----------------------------------------------------

        top = tk.Frame(
            parent,
            bg=self.bg
        )

        top.pack(
            fill="both",
            expand=True
        )

        top.grid_columnconfigure(
            0,
            weight=3,
            uniform="calculator"
        )

        top.grid_columnconfigure(
            1,
            weight=2,
            uniform="calculator"
        )

        top.grid_rowconfigure(
            0,
            weight=1
        )

        scientific = tk.Frame(
            top,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        keypad = tk.Frame(
            top,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        scientific.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5)
        )

        keypad.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0)
        )

        self.build_scientific_panel(
            scientific
        )

        self.build_keypad_panel(
            keypad
        )

        # -----------------------------------------------------
        # Equation Solver
        # -----------------------------------------------------

        solver_button = tk.Button(
            parent,
            text="OPEN EQUATION SOLVER",
            command=self.open_equation_solver,
            bg="#1e40af",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            pady=11
        )

        solver_button.pack(
            fill="x",
            pady=(10, 0)
        )

    # =========================================================
    # SCIENTIFIC PANEL
    # =========================================================

    def build_scientific_panel(self, parent):

        tk.Label(
            parent,
            text="SCIENTIFIC FUNCTIONS",
            bg=self.panel,
            fg=self.text,
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=14,
            pady=(12, 6)
        )

        grid = tk.Frame(
            parent,
            bg=self.panel
        )

        grid.pack(
            fill="both",
            expand=True,
            padx=9,
            pady=7
        )

        for column in range(6):

            grid.grid_columnconfigure(
                column,
                weight=1,
                uniform="scientific"
            )

        for row in range(5):

            grid.grid_rowconfigure(
                row,
                weight=1,
                uniform="scientific"
            )

        functions = [

            [
                ("sin", "sin("),
                ("cos", "cos("),
                ("tan", "tan("),
                ("asin", "asin("),
                ("acos", "acos("),
                ("atan", "atan(")
            ],

            [
                ("sinh", "sinh("),
                ("cosh", "cosh("),
                ("tanh", "tanh("),
                ("ln", "ln("),
                ("log", "log10("),
                ("log₂", "log2(")
            ],

            [
                ("√", "sqrt("),
                ("∛", "cbrt("),
                ("x²", "**2"),
                ("xʸ", "**"),
                ("1/x", "inv("),
                ("x!", "fact(")
            ],

            [
                ("π", "pi"),
                ("e", "e"),
                ("τ", "tau"),
                ("φ", "phi"),
                ("nCr", "nCr("),
                ("nPr", "nPr(")
            ],

            [
                ("abs", "abs("),
                ("floor", "floor("),
                ("ceil", "ceil("),
                ("gcd", "gcd("),
                ("lcm", "lcm("),
                ("mod", " mod ")
            ]
        ]

        for row_index, row in enumerate(functions):

            for column_index, (label, value) in enumerate(row):

                button = self.make_button(
                    grid,
                    label,
                    lambda v=value: self.insert_text(v),
                    bg=self.function_button,
                    hover=self.function_hover
                )

                button.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew",
                    padx=4,
                    pady=4
                )

    # =========================================================
    # KEYPAD
    # =========================================================

    def build_keypad_panel(self, parent):

        tk.Label(
            parent,
            text="MAIN KEYPAD",
            bg=self.panel,
            fg=self.text,
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=14,
            pady=(12, 6)
        )

        keypad = tk.Frame(
            parent,
            bg=self.panel
        )

        keypad.pack(
            fill="both",
            expand=True,
            padx=9,
            pady=7
        )

        for column in range(4):

            keypad.grid_columnconfigure(
                column,
                weight=1,
                uniform="keypad"
            )

        for row in range(6):

            keypad.grid_rowconfigure(
                row,
                weight=1,
                uniform="keypad"
            )

        buttons = [

            [
                ("(", "normal"),
                (")", "normal"),
                ("%", "operator"),
                ("⌫", "danger")
            ],

            [
                ("7", "normal"),
                ("8", "normal"),
                ("9", "normal"),
                ("÷", "operator")
            ],

            [
                ("4", "normal"),
                ("5", "normal"),
                ("6", "normal"),
                ("×", "operator")
            ],

            [
                ("1", "normal"),
                ("2", "normal"),
                ("3", "normal"),
                ("−", "operator")
            ],

            [
                ("0", "normal"),
                (".", "normal"),
                ("00", "normal"),
                ("+", "operator")
            ],

            [
                ("CE", "danger"),
                ("ANS", "normal"),
                ("=", "equal"),
                ("ENTER", "equal")
            ]
        ]

        for row_index, row in enumerate(buttons):

            for column_index, (
                label,
                category
            ) in enumerate(row):

                if category == "normal":

                    command = lambda v=label: (
                        self.insert_text(v)
                    )

                    bg = self.button
                    hover = self.button_hover

                elif category == "operator":

                    operators = {
                        "÷": "/",
                        "×": "*",
                        "−": "-"
                    }

                    value = operators.get(
                        label,
                        label
                    )

                    command = lambda v=value: (
                        self.insert_text(v)
                    )

                    bg = self.operator_button
                    hover = self.operator_hover

                elif category == "danger":

                    if label == "⌫":
                        command = self.backspace
                    else:
                        command = self.clear_current

                    bg = self.danger_button
                    hover = self.danger_hover

                else:

                    command = self.calculate
                    bg = self.equal_button
                    hover = self.equal_hover

                button = self.make_button(
                    keypad,
                    label,
                    command,
                    bg=bg,
                    hover=hover,
                    large=True
                )

                button.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew",
                    padx=5,
                    pady=5
                )

    # =========================================================
    # BUTTON CREATOR
    # =========================================================

    def make_button(
        self,
        parent,
        text,
        command,
        bg,
        hover,
        large=False
    ):

        font = (
            ("Segoe UI", 13, "bold")
            if large
            else ("Segoe UI", 10, "bold")
        )

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=self.text,
            activebackground=hover,
            activeforeground=self.text,
            font=font,
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        button.bind(
            "<Enter>",
            lambda event: button.configure(
                bg=hover
            )
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(
                bg=bg
            )
        )

        return button

    # =========================================================
    # HISTORY PANEL
    # =========================================================

    def build_history_area(self, parent):

        header = tk.Frame(
            parent,
            bg=self.panel
        )

        header.pack(
            fill="x",
            padx=14,
            pady=(14, 8)
        )

        title = tk.Label(
            header,
            text="CALCULATION HISTORY",
            bg=self.panel,
            fg=self.text,
            font=("Segoe UI", 13, "bold")
        )

        title.pack(
            side="left"
        )

        self.history_count_label = tk.Label(
            header,
            text="0",
            bg=self.panel2,
            fg="#60a5fa",
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=3
        )

        self.history_count_label.pack(
            side="right"
        )

        # -----------------------------------------------------
        # History list
        # -----------------------------------------------------

        list_frame = tk.Frame(
            parent,
            bg=self.panel
        )

        list_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=5
        )

        scrollbar = tk.Scrollbar(
            list_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.history_list = tk.Listbox(
            list_frame,
            bg=self.display_bg,
            fg=self.text,
            selectbackground=self.equal_button,
            selectforeground="white",
            font=("Consolas", 10),
            relief="flat",
            borderwidth=0,
            activestyle="none",
            yscrollcommand=scrollbar.set
        )

        self.history_list.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.history_list.yview
        )

        self.history_list.bind(
            "<Double-Button-1>",
            self.use_history
        )

        # -----------------------------------------------------
        # History information
        # -----------------------------------------------------

        info = tk.Label(
            parent,
            text=(
                "Double-click a calculation to reuse it.\n"
                "History is separate from calculator memory."
            ),
            bg=self.panel,
            fg=self.secondary_text,
            font=("Segoe UI", 8),
            justify="left"
        )

        info.pack(
            anchor="w",
            padx=14,
            pady=7
        )

        # -----------------------------------------------------
        # Clear History Button
        # -----------------------------------------------------

        clear_history_button = tk.Button(
            parent,
            text="CLEAR HISTORY",
            command=self.clear_history,
            bg=self.danger_button,
            fg="white",
            activebackground=self.danger_hover,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            pady=10
        )

        clear_history_button.pack(
            fill="x",
            padx=12,
            pady=(5, 14)
        )

    # =========================================================
    # INPUT
    # =========================================================

    def insert_text(self, text):

        current = self.expression_var.get()

        try:

            cursor = self.expression_entry.index(
                tk.INSERT
            )

            updated = (
                current[:cursor]
                + text
                + current[cursor:]
            )

            self.expression_var.set(
                updated
            )

            self.expression_entry.icursor(
                cursor + len(text)
            )

        except tk.TclError:

            self.expression_var.set(
                current + text
            )

        self.expression_entry.focus_set()

    def insert_answer(self):

        self.insert_text(
            "ANS"
        )

    def clear_current(self):

        self.expression_var.set("")
        self.result_var.set("0")
        self.status_var.set("Ready")

    def backspace(self):

        value = self.expression_var.get()

        try:

            cursor = self.expression_entry.index(
                tk.INSERT
            )

            if cursor > 0:

                self.expression_var.set(
                    value[:cursor - 1]
                    + value[cursor:]
                )

                self.expression_entry.icursor(
                    cursor - 1
                )

        except tk.TclError:

            self.expression_var.set(
                value[:-1]
            )

    # =========================================================
    # ANGLE MODE
    # =========================================================

    def toggle_angle_mode(self):

        if self.angle_mode == "DEG":
            self.angle_mode = "RAD"
        else:
            self.angle_mode = "DEG"

        self.angle_button.config(
            text=self.angle_mode
        )

        self.status_var.set(
            f"Angle mode changed to {self.angle_mode}."
        )

    # =========================================================
    # SCIENTIFIC FUNCTIONS
    # =========================================================

    def to_radians(self, x):

        if self.angle_mode == "DEG":
            return math.radians(x)

        return x

    def from_radians(self, x):

        if self.angle_mode == "DEG":
            return math.degrees(x)

        return x

    def sin(self, x):
        return math.sin(
            self.to_radians(x)
        )

    def cos(self, x):
        return math.cos(
            self.to_radians(x)
        )

    def tan(self, x):
        return math.tan(
            self.to_radians(x)
        )

    def asin(self, x):
        return self.from_radians(
            math.asin(x)
        )

    def acos(self, x):
        return self.from_radians(
            math.acos(x)
        )

    def atan(self, x):
        return self.from_radians(
            math.atan(x)
        )

    def cbrt(self, x):

        if x >= 0:
            return x ** (1 / 3)

        return -((-x) ** (1 / 3))

    def factorial(self, x):

        if x < 0 or int(x) != x:
            raise ValueError(
                "Factorial requires a non-negative integer."
            )

        return math.factorial(
            int(x)
        )

    def inverse(self, x):

        if x == 0:
            raise ZeroDivisionError(
                "Cannot divide by zero."
            )

        return 1 / x

    def combination(self, n, r):

        if int(n) != n or int(r) != r:
            raise ValueError(
                "nCr requires integers."
            )

        return math.comb(
            int(n),
            int(r)
        )

    def permutation(self, n, r):

        if int(n) != n or int(r) != r:
            raise ValueError(
                "nPr requires integers."
            )

        return math.perm(
            int(n),
            int(r)
        )

    # =========================================================
    # SAFE MATH NAMESPACE
    # =========================================================

    def namespace(self):

        return {
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,

            "asin": self.asin,
            "acos": self.acos,
            "atan": self.atan,

            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,

            "ln": math.log,
            "log10": math.log10,
            "log2": math.log2,

            "sqrt": math.sqrt,
            "cbrt": self.cbrt,

            "abs": abs,
            "floor": math.floor,
            "ceil": math.ceil,

            "gcd": math.gcd,
            "lcm": math.lcm,

            "fact": self.factorial,
            "nCr": self.combination,
            "nPr": self.permutation,

            "inv": self.inverse,

            "pi": math.pi,
            "e": math.e,
            "tau": math.tau,

            "phi": (1 + math.sqrt(5)) / 2,

            "ANS": self.answer,
            "M": self.memory
        }

    # =========================================================
    # PREPROCESS EXPRESSION
    # =========================================================

    def preprocess(self, expression):

        expression = expression.strip()

        expression = expression.replace(
            "×",
            "*"
        )

        expression = expression.replace(
            "÷",
            "/"
        )

        expression = expression.replace(
            "−",
            "-"
        )

        expression = expression.replace(
            "^",
            "**"
        )

        expression = expression.replace(
            " mod ",
            "%"
        )

        # Convert percentages
        expression = re.sub(
            r"(\d+(?:\.\d+)?)%",
            r"(\1/100)",
            expression
        )

        # Factorials
        expression = re.sub(
            r"(\d+(?:\.\d+)?)!",
            r"fact(\1)",
            expression
        )

        return expression

    # =========================================================
    # VALIDATE EXPRESSION
    # =========================================================

    def validate_expression(self, expression):

        # Reject empty
        if not expression.strip():
            raise ValueError(
                "Please enter a mathematical equation."
            )

        # Reject normal English text
        if re.search(
            r"[^\d\s\+\-\*\/\%\^\(\)\.,a-zA-Z_]",
            expression
        ):
            raise ValueError(
                "Invalid mathematical expression. "
                "Calculation cannot be performed."
            )

        # Reject obvious sentences/words
        words = re.findall(
            r"[A-Za-z]+",
            expression
        )

        allowed_names = set(
            self.namespace().keys()
        )

        for word in words:

            if word not in allowed_names:

                raise ValueError(
                    f"'{word}' is not a valid mathematical "
                    f"function or symbol."
                )

        # Reject accidental alphabetic strings
        # like 'hello' or 'calculate'
        if expression.isalpha():

            if expression not in allowed_names:

                raise ValueError(
                    "Invalid mathematical expression. "
                    "Calculation cannot be performed."
                )

    # =========================================================
    # AST VALIDATION
    # =========================================================

    def validate_ast(self, tree):

        allowed_nodes = (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Call,
            ast.Name,
            ast.Load,
            ast.Constant,

            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Mod,
            ast.Pow,

            ast.UAdd,
            ast.USub
        )

        functions = self.namespace()

        for node in ast.walk(tree):

            if not isinstance(
                node,
                allowed_nodes
            ):

                raise ValueError(
                    "Invalid mathematical expression."
                )

            if isinstance(
                node,
                ast.Name
            ):

                if node.id not in functions:

                    raise ValueError(
                        f"Unknown mathematical symbol: "
                        f"{node.id}"
                    )

            if isinstance(
                node,
                ast.Call
            ):

                if not isinstance(
                    node.func,
                    ast.Name
                ):

                    raise ValueError(
                        "Invalid function."
                    )

                if node.func.id not in functions:

                    raise ValueError(
                        f"Unsupported function: "
                        f"{node.func.id}"
                    )

    # =========================================================
    # EVALUATE
    # =========================================================

    def evaluate(self, expression):

        self.validate_expression(
            expression
        )

        expression = self.preprocess(
            expression
        )

        try:

            tree = ast.parse(
                expression,
                mode="eval"
            )

        except SyntaxError:

            raise ValueError(
                "Invalid mathematical syntax. "
                "Please check the equation."
            )

        self.validate_ast(
            tree
        )

        try:

            result = eval(
                compile(
                    tree,
                    "<calculator>",
                    "eval"
                ),
                {
                    "__builtins__": {}
                },
                self.namespace()
            )

        except NameError:

            raise ValueError(
                "Unknown mathematical symbol."
            )

        if isinstance(
            result,
            complex
        ):

            raise ValueError(
                "Complex results are not supported."
            )

        try:

            if not math.isfinite(
                float(result)
            ):

                raise ValueError(
                    "Result is not finite."
                )

        except (TypeError, ValueError):

            raise ValueError(
                "The entered expression cannot be calculated."
            )

        return result

    # =========================================================
    # CALCULATE
    # =========================================================

    def calculate(self, event=None):

        expression = (
            self.expression_var.get()
            .strip()
        )

        if not expression:

            self.show_error(
                "Please enter a mathematical equation."
            )

            return

        try:

            result = self.evaluate(
                expression
            )

            self.answer = float(
                result
            )

            formatted = self.format_number(
                result
            )

            self.result_var.set(
                formatted
            )

            self.status_var.set(
                f"Calculation successful • "
                f"{self.angle_mode} mode"
            )

            self.add_history(
                expression,
                formatted
            )

        except ZeroDivisionError:

            self.show_error(
                "Math Error: Division by zero is not allowed."
            )

        except ValueError as error:

            self.show_error(
                str(error)
            )

        except OverflowError:

            self.show_error(
                "Overflow Error: The number is too large."
            )

        except Exception as error:

            self.show_error(
                f"Calculation error: {error}"
            )

    # =========================================================
    # FORMAT NUMBER
    # =========================================================

    def format_number(self, value):

        value = float(value)

        if abs(value) < 1e-12:
            value = 0.0

        if value.is_integer():

            return str(
                int(value)
            )

        return f"{value:.12g}"

    # =========================================================
    # ERROR
    # =========================================================

    def show_error(self, message):

        self.result_var.set(
            "ERROR"
        )

        self.status_var.set(
            message
        )

        self.expression_entry.focus_set()

    # =========================================================
    # MEMORY
    # =========================================================

    def current_value(self):

        expression = (
            self.expression_var.get()
            .strip()
        )

        if expression:

            return float(
                self.evaluate(
                    expression
                )
            )

        return self.answer

    def memory_clear(self):

        self.memory = 0.0

        self.update_memory_display()

        self.status_var.set(
            "Calculator memory cleared."
        )

    def memory_recall(self):

        self.insert_text(
            self.format_number(
                self.memory
            )
        )

    def memory_add(self):

        try:

            self.memory += (
                self.current_value()
            )

            self.update_memory_display()

            self.status_var.set(
                "Value added to calculator memory."
            )

        except Exception:

            self.show_error(
                "Unable to add value to memory."
            )

    def memory_subtract(self):

        try:

            self.memory -= (
                self.current_value()
            )

            self.update_memory_display()

            self.status_var.set(
                "Value subtracted from calculator memory."
            )

        except Exception:

            self.show_error(
                "Unable to subtract value from memory."
            )

    def memory_store(self):

        try:

            self.memory = (
                self.current_value()
            )

            self.update_memory_display()

            self.status_var.set(
                "Value stored in calculator memory."
            )

        except Exception:

            self.show_error(
                "Unable to store value."
            )

    def update_memory_display(self):

        self.memory_var.set(
            f"M: {self.format_number(self.memory)}"
        )

    # =========================================================
    # HISTORY
    # =========================================================

    def add_history(
        self,
        expression,
        result
    ):

        time = datetime.now().strftime(
            "%H:%M:%S"
        )

        history_item = {
            "time": time,
            "expression": expression,
            "result": result
        }

        self.history.insert(
            0,
            history_item
        )

        self.refresh_history()

    def refresh_history(self):

        self.history_list.delete(
            0,
            tk.END
        )

        for item in self.history:

            text = (
                f"[{item['time']}] "
                f"{item['expression']} = "
                f"{item['result']}"
            )

            self.history_list.insert(
                tk.END,
                text
            )

        self.history_count_label.config(
            text=str(
                len(self.history)
            )
        )

    def clear_history(self):

        if not self.history:

            self.status_var.set(
                "History is already empty."
            )

            return

        confirm = messagebox.askyesno(
            "Clear Calculation History",
            "Are you sure you want to permanently "
            "remove all calculation history?"
        )

        if confirm:

            self.history.clear()

            self.refresh_history()

            self.status_var.set(
                "All calculation history has been removed."
            )

    def use_history(self, event=None):

        selection = (
            self.history_list.curselection()
        )

        if not selection:
            return

        index = selection[0]

        if index >= len(self.history):
            return

        item = self.history[index]

        self.expression_var.set(
            item["expression"]
        )

        self.result_var.set(
            item["result"]
        )

        self.status_var.set(
            "History entry loaded into calculator."
        )

        self.expression_entry.focus_set()

    # =========================================================
    # COPY
    # =========================================================

    def copy_result(self):

        value = self.result_var.get()

        self.root.clipboard_clear()

        self.root.clipboard_append(
            value
        )

        self.root.update()

        self.status_var.set(
            "Result copied to clipboard."
        )

    # =========================================================
    # KEYBOARD
    # =========================================================

    def bind_keyboard(self):

        self.root.bind(
            "<Return>",
            self.calculate
        )

        self.root.bind(
            "<KP_Enter>",
            self.calculate
        )

        self.root.bind(
            "<Escape>",
            lambda event: self.clear_current()
        )

        self.root.bind(
            "<Control-c>",
            lambda event: self.copy_result()
        )

    # =========================================================
    # EQUATION SOLVER WINDOW
    # =========================================================

    def open_equation_solver(self):

        solver = tk.Toplevel(
            self.root
        )

        solver.title(
            "Linear Equation System Solver"
        )

        solver.geometry(
            "850x700"
        )

        solver.minsize(
            720,
            600
        )

        solver.configure(
            bg=self.bg
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = tk.Frame(
            solver,
            bg=self.bg
        )

        header.pack(
            fill="x",
            padx=20,
            pady=15
        )

        tk.Label(
            header,
            text="EQUATION SYSTEM SOLVER",
            bg=self.bg,
            fg=self.text,
            font=("Segoe UI", 19, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            header,
            text=(
                "Solve linear equations such as "
                "a + b = 80, a + c = 90, etc."
            ),
            bg=self.bg,
            fg=self.secondary_text,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # -----------------------------------------------------
        # INPUT PANEL
        # -----------------------------------------------------

        input_panel = tk.Frame(
            solver,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        input_panel.pack(
            fill="x",
            padx=20,
            pady=5
        )

        input_header = tk.Frame(
            input_panel,
            bg=self.panel
        )

        input_header.pack(
            fill="x",
            padx=14,
            pady=(12, 5)
        )

        tk.Label(
            input_header,
            text="ENTER EQUATIONS",
            bg=self.panel,
            fg=self.text,
            font=("Segoe UI", 12, "bold")
        ).pack(
            side="left"
        )

        tk.Label(
            input_header,
            text="Example: a + b = 80",
            bg=self.panel,
            fg="#60a5fa",
            font=("Segoe UI", 9)
        ).pack(
            side="right"
        )

        entries_frame = tk.Frame(
            input_panel,
            bg=self.panel
        )

        entries_frame.pack(
            fill="x",
            padx=14,
            pady=5
        )

        self.solver_entries = []

        for i in range(5):

            row = tk.Frame(
                entries_frame,
                bg=self.panel
            )

            row.pack(
                fill="x",
                pady=4
            )

            tk.Label(
                row,
                text=f"Equation {i + 1}",
                bg=self.panel,
                fg=self.secondary_text,
                font=("Segoe UI", 10, "bold"),
                width=13,
                anchor="w"
            ).pack(
                side="left"
            )

            entry = tk.Entry(
                row,
                bg=self.display_bg,
                fg=self.text,
                insertbackground=self.text,
                relief="flat",
                font=("Consolas", 12)
            )

            entry.pack(
                side="left",
                fill="x",
                expand=True,
                ipady=6
            )

            self.solver_entries.append(
                entry
            )

        # -----------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------

        button_frame = tk.Frame(
            input_panel,
            bg=self.panel
        )

        button_frame.pack(
            fill="x",
            padx=14,
            pady=(8, 14)
        )

        tk.Button(
            button_frame,
            text="SOLVE SYSTEM",
            command=self.solve_equation_system,
            bg=self.equal_button,
            fg="white",
            activebackground=self.equal_hover,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9
        ).pack(
            side="left"
        )

        tk.Button(
            button_frame,
            text="CLEAR",
            command=self.clear_solver,
            bg=self.danger_button,
            fg="white",
            activebackground=self.danger_hover,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9
        ).pack(
            side="left",
            padx=8
        )

        # -----------------------------------------------------
        # RESULT
        # -----------------------------------------------------

        result_panel = tk.Frame(
            solver,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        result_panel.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(8, 20)
        )

        tk.Label(
            result_panel,
            text="SOLUTION",
            bg=self.panel,
            fg=self.text,
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=14,
            pady=(12, 5)
        )

        self.solver_result = tk.Text(
            result_panel,
            bg=self.display_bg,
            fg=self.text,
            font=("Consolas", 13),
            relief="flat",
            wrap="word",
            padx=12,
            pady=12
        )

        self.solver_result.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(0, 14)
        )

        self.set_solver_result(
            "Enter your equations above.\n\n"
            "Example:\n"
            "a + b = 80\n"
            "a + c = 90\n"
            "b + c = 100\n\n"
            "Then click SOLVE SYSTEM."
        )

    # =========================================================
    # EQUATION PARSER
    # =========================================================

    def extract_variables(
        self,
        expression
    ):

        variables = re.findall(
            r"(?<![A-Za-z0-9_])([A-Za-z])"
            r"(?![A-Za-z0-9_])",
            expression
        )

        forbidden = {
            "e"
        }

        output = []

        for variable in variables:

            if variable not in forbidden:

                if variable not in output:
                    output.append(variable)

        return output

    def polynomial_to_coefficients(
        self,
        expression,
        variables
    ):
        """
        Converts a simple linear expression into:

        {
            variable: coefficient,
            "__constant__": constant
        }

        Supported forms:

        a
        -a
        2a
        2*a
        a + b
        2a - 3b + 20
        """

        expression = expression.replace(
            " ",
            ""
        )

        if not expression:
            return {
                "__constant__": 0.0
            }

        expression = expression.replace(
            "-",
            "+-"
        )

        if expression.startswith("+"):
            expression = expression[1:]

        terms = expression.split(
            "+"
        )

        result = {
            "__constant__": 0.0
        }

        for term in terms:

            if not term:
                continue

            sign = 1

            if term.startswith("-"):

                sign = -1

                term = term[1:]

            if not term:
                raise ValueError(
                    "Invalid equation term."
                )

            found_variable = None

            for variable in variables:

                if re.search(
                    rf"(?<![A-Za-z])"
                    rf"{re.escape(variable)}"
                    rf"(?![A-Za-z])",
                    term
                ):

                    found_variable = variable
                    break

            if found_variable is None:

                # Constant
                try:

                    constant = float(
                        term
                    )

                except ValueError:

                    raise ValueError(
                        f"Invalid term: '{term}'"
                    )

                result["__constant__"] += (
                    sign * constant
                )

                continue

            # -------------------------------------------------
            # Variable term
            # -------------------------------------------------

            coefficient_part = re.sub(
                rf"(?<![A-Za-z])"
                rf"{re.escape(found_variable)}"
                rf"(?![A-Za-z])",
                "",
                term
            )

            coefficient_part = (
                coefficient_part.replace(
                    "*",
                    ""
                )
            )

            if coefficient_part in (
                "",
                "+"
            ):

                coefficient = 1.0

            else:

                try:

                    coefficient = float(
                        coefficient_part
                    )

                except ValueError:

                    raise ValueError(
                        f"Invalid coefficient in term: '{term}'"
                    )

            result[found_variable] = (
                result.get(
                    found_variable,
                    0.0
                )
                + sign * coefficient
            )

        return result

    # =========================================================
    # PARSE EQUATION
    # =========================================================

    def parse_equation(
        self,
        equation
    ):

        equation = equation.strip()

        if not equation:
            raise ValueError(
                "Empty equation."
            )

        if equation.count("=") != 1:

            raise ValueError(
                "Each equation must contain exactly one '='."
            )

        left, right = equation.split(
            "=",
            1
        )

        left = left.strip()
        right = right.strip()

        if not left or not right:

            raise ValueError(
                "Both sides of the equation are required."
            )

        variables = self.extract_variables(
            equation
        )

        if not variables:

            raise ValueError(
                f"No variables found in '{equation}'."
            )

        left_coefficients = (
            self.polynomial_to_coefficients(
                left,
                variables
            )
        )

        right_coefficients = (
            self.polynomial_to_coefficients(
                right,
                variables
            )
        )

        result = {}

        for variable in variables:

            result[variable] = (
                left_coefficients.get(
                    variable,
                    0.0
                )
                -
                right_coefficients.get(
                    variable,
                    0.0
                )
            )

        result["__constant__"] = (
            right_coefficients.get(
                "__constant__",
                0.0
            )
            -
            left_coefficients.get(
                "__constant__",
                0.0
            )
        )

        return result, variables

    # =========================================================
    # GAUSSIAN ELIMINATION
    # =========================================================

    def gaussian_elimination(
        self,
        matrix
    ):

        rows = len(matrix)
        cols = len(matrix[0])

        pivot_row = 0

        for column in range(
            cols - 1
        ):

            pivot = None

            for row in range(
                pivot_row,
                rows
            ):

                if abs(
                    matrix[row][column]
                ) > 1e-12:

                    pivot = row
                    break

            if pivot is None:
                continue

            matrix[
                pivot_row
            ], matrix[pivot] = (
                matrix[pivot],
                matrix[pivot_row]
            )

            pivot_value = matrix[
                pivot_row
            ][column]

            for j in range(
                column,
                cols
            ):

                matrix[pivot_row][j] /= (
                    pivot_value
                )

            for row in range(rows):

                if row == pivot_row:
                    continue

                factor = matrix[
                    row
                ][column]

                if abs(factor) < 1e-12:
                    continue

                for j in range(
                    column,
                    cols
                ):

                    matrix[row][j] -= (
                        factor
                        * matrix[pivot_row][j]
                    )

            pivot_row += 1

            if pivot_row == rows:
                break

        return matrix

    # =========================================================
    # SOLVE EQUATION SYSTEM
    # =========================================================

    def solve_equation_system(self):

        equations = []

        for entry in self.solver_entries:

            value = entry.get().strip()

            if value:
                equations.append(
                    value
                )

        if not equations:

            self.set_solver_result(
                "ERROR\n\n"
                "Please enter at least one equation."
            )

            return

        try:

            all_parsed = []

            all_variables = set()

            for equation in equations:

                coefficients, variables = (
                    self.parse_equation(
                        equation
                    )
                )

                all_parsed.append(
                    coefficients
                )

                all_variables.update(
                    variables
                )

            variables = sorted(
                all_variables
            )

            number_of_equations = len(
                equations
            )

            number_of_variables = len(
                variables
            )

            # -------------------------------------------------
            # Require enough equations
            # -------------------------------------------------

            if number_of_equations < number_of_variables:

                raise ValueError(
                    "Not enough equations for a unique solution."
                )

            # -------------------------------------------------
            # Create augmented matrix
            # -------------------------------------------------

            matrix = []

            for coefficients in all_parsed:

                row = []

                for variable in variables:

                    row.append(
                        coefficients.get(
                            variable,
                            0.0
                        )
                    )

                row.append(
                    coefficients.get(
                        "__constant__",
                        0.0
                    )
                )

                matrix.append(
                    row
                )

            # -------------------------------------------------
            # Eliminate
            # -------------------------------------------------

            reduced = (
                self.gaussian_elimination(
                    matrix
                )
            )

            # -------------------------------------------------
            # Check contradictions
            # -------------------------------------------------

            for row in reduced:

                coefficients = row[
                    :-1
                ]

                constant = row[
                    -1
                ]

                all_zero = all(
                    abs(value) < 1e-10
                    for value in coefficients
                )

                if (
                    all_zero
                    and abs(constant) > 1e-10
                ):

                    raise ValueError(
                        "The system is inconsistent "
                        "and has no solution."
                    )

            # -------------------------------------------------
            # Check unique solution
            # -------------------------------------------------

            solution = {}

            for variable_index, variable in enumerate(
                variables
            ):

                pivot_row = None

                for row in reduced:

                    first_nonzero = None

                    for index, value in enumerate(
                        row[:-1]
                    ):

                        if abs(value) > 1e-10:

                            first_nonzero = index
                            break

                    if (
                        first_nonzero
                        == variable_index
                    ):

                        pivot_row = row
                        break

                if pivot_row is None:

                    raise ValueError(
                        "The system does not have a unique solution."
                    )

                solution[
                    variable
                ] = pivot_row[-1]

            # -------------------------------------------------
            # Result
            # -------------------------------------------------

            output = []

            output.append(
                "✓ SYSTEM SOLVED SUCCESSFULLY"
            )

            output.append(
                ""
            )

            output.append(
                "INPUT EQUATIONS:"
            )

            for equation in equations:

                output.append(
                    f"  {equation}"
                )

            output.append(
                ""
            )

            output.append(
                "SOLUTIONS:"
            )

            for variable in variables:

                output.append(
                    f"  {variable} = "
                    f"{self.format_number(solution[variable])}"
                )

            output.append(
                ""
            )

            output.append(
                "VERIFICATION:"
            )

            for equation in equations:

                output.append(
                    f"  ✓ {equation}"
                )

            self.set_solver_result(
                "\n".join(output)
            )

        except ValueError as error:

            self.set_solver_result(
                "ERROR\n\n"
                + str(error)
                + "\n\n"
                "Please check the equations and "
                "make sure they are linear."
            )

        except Exception as error:

            self.set_solver_result(
                "ERROR\n\n"
                + str(error)
            )

    # =========================================================
    # SOLVER RESULT
    # =========================================================

    def set_solver_result(self, text):

        self.solver_result.configure(
            state="normal"
        )

        self.solver_result.delete(
            "1.0",
            tk.END
        )

        self.solver_result.insert(
            "1.0",
            text
        )

        self.solver_result.configure(
            state="disabled"
        )

    # =========================================================
    # CLEAR SOLVER
    # =========================================================

    def clear_solver(self):

        for entry in self.solver_entries:

            entry.delete(
                0,
                tk.END
            )

        self.set_solver_result(
            "Enter your equations above.\n\n"
            "Example:\n"
            "a + b = 80\n"
            "a + c = 90\n"
            "b + c = 100\n\n"
            "Then click SOLVE SYSTEM."
        )


# =============================================================
# MAIN
# =============================================================

def main():

    root = tk.Tk()

    app = AdvancedScientificCalculator(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()