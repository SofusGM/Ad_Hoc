import tkinter as tk
from tkinter import ttk

class ManyCategoriesTreeviewApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Betting App with Auto-Expanded Categories")
        self.state("zoomed")  # try to open maximized; adjust as needed

        # Background color
        self.configure(bg="#BCEE68")  # light lemon-chiffon

        # Example categories (dict of {category_name: {member_name: amount}})
        self.categories = {
    "Tysk": {},  # German
    "Fransk": {},  # French
    "Spansk": {},  # Spanish
    "Italiensk": {},  # Italian
    "Portugisisk": {},  # Portuguese
    "Hollandsk": {},  # Dutch
    "Belgisk": {},  # Belgian
    "Schweizisk": {},  # Swiss
    "Østrigsk": {},  # Austrian
    "Britisk": {},  # British
    "Irsk": {},  # Irish
    "Norsk": {},  # Norwegian
    "Svensk": {},  # Swedish
    "Finsk": {},  # Finnish
    "Islandsk": {},  # Icelandic
    "Dansk": {},  # Danish
    "Polsk": {},  # Polish
    "Ungarsk": {},  # Hungarian
    "Rumænsk": {},  # Romanian
    "Bulgarsk": {},  # Bulgarian
    "Græsk": {},  # Greek
    "Russisk": {},  # Russian
    "Ukrainsk": {},  # Ukrainian
    "Estisk": {},  # Estonian
    "Letlandsk": {},  # Latvian
    "Slovensk": {},  # Slovenian
    "Kroatisk": {},  # Croatian
    "Serbisk": {},  # Serbian
    "Bosnisk": {},  # Bosnian
    "Montenegrinsk": {},  # Montenegrin
    "Makedonsk": {},  # Macedonian (North Macedonia)
    "Albansk": {},  # Albanian
    "Maltesisk": {},  # Maltese
    "Andorransk": {},  # Andorran
    "Liechtensteinsk": {},  # Liechtensteiner
    "Luxembourgsk": {},  # Luxembourgish
    "Monegaskisk": {},  # Monégasque (Monaco)
    "Peruiansk": {},  # Sanmarinese (San Marino)
    "Mexikansk": {},  # Vatican (Holy See)
    "Brasiliansk": {},
    "Columbisk": {},
    "Pudorikansk":{},
}

        # Currently selected category
        self.selected_category = None

        # Countdown variables
        self.countdown_running = False
        self.remaining_time = 10
        self.color_index = 0
        self.countdown_colors = [
            "#FFC0CB",  # pink
            "#FFD700",  # gold
            "#98FB98",  # pale green
            "#00CED1",  # dark turquoise
            "#FFA500",  # orange
            "#FF69B4",  # hot pink
        ]

        self.create_widgets()
        self.refresh_tree()  # populate the tree initially

    def create_widgets(self):
        # -------------------------
        # TOP FRAME: Bet controls
        # -------------------------
        top_frame = tk.Frame(self, bg="#BCEE68")
        top_frame.pack(side="top", fill="x", padx=10, pady=10)

        bet_frame = tk.Frame(top_frame, bg="#BCEE68")
        bet_frame.pack(side="left", padx=20)

        tk.Label(bet_frame, text="Deltager:",
                 font=("Helvetica", 14, "bold"),
                 bg="#BCEE68").grid(row=0, column=0, sticky="e", pady=5)
        self.member_name_var = tk.StringVar()
        self.member_name_entry = tk.Entry(bet_frame, textvariable=self.member_name_var,
                                          font=("Helvetica", 12))
        self.member_name_entry.grid(row=0, column=1, pady=5)

        tk.Label(bet_frame, text="Placér bet (DKK):",
                 font=("Helvetica", 14, "bold"),
                 bg="#BCEE68").grid(row=1, column=0, sticky="e", pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = tk.Entry(bet_frame, textvariable=self.amount_var,
                                     font=("Helvetica", 12))
        self.amount_entry.grid(row=1, column=1, pady=5)

        self.add_bet_button = tk.Button(bet_frame, text="Tilføj / Opdatér Bet",
                                        command=self.add_or_update_bet,
                                        font=("Helvetica", 12, "bold"),
                                        bg="#B0E0E6")  # powder blue
        self.add_bet_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.current_category_label = tk.Label(bet_frame,
                                               text="Valgt Nationalitet: Ingen",
                                               font=("Helvetica", 12, "bold"),
                                               bg="#BCEE68")
        self.current_category_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Countdown area
        countdown_frame = tk.Frame(top_frame, bg="#BCEE68")
        countdown_frame.pack(side="right", padx=20)
        self.countdown_label = tk.Label(countdown_frame, text="Countdown not started.",
                                        font=("Helvetica", 16, "bold"),
                                        bg="#BCEE68")
        self.countdown_label.pack(pady=5)
        self.start_button = tk.Button(countdown_frame, text="Start Countdown",
                                      command=self.start_countdown,
                                      font=("Helvetica", 12, "bold"),
                                      bg="#90EE90")  # light green
        self.start_button.pack(pady=5)

        # -------------------------
        # MIDDLE FRAME: Category buttons + Treeview
        # -------------------------
        middle_frame = tk.Frame(self, bg="#BCEE68")
        middle_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        # LEFT: Category buttons in a 4-column grid
        self.category_frame = tk.Frame(middle_frame, bg="#BCEE68")
        self.category_frame.pack(side="left", fill="both", expand=False, padx=10)

        self.build_category_buttons()

        # RIGHT: A frame for the Treeview of bets
        table_frame = tk.Frame(middle_frame, bg="#BCEE68")
        table_frame.pack(side="right", fill="both", expand=True)

        # Create a Treeview with one “tree” column (#0) + an “amount” column
        self.tree = ttk.Treeview(table_frame, columns=("amount",), show="tree headings")
        # The #0 column is the "tree" column
        self.tree.heading("#0", text="Category / Member")
        self.tree.column("#0", width=200, stretch=True)

        # The second column is "amount"
        self.tree.heading("amount", text="Amount")
        self.tree.column("amount", width=80, anchor=tk.E, stretch=False)

        # Attach a scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # -------------------------
        # BOTTOM FRAME: Pick winner & results
        # -------------------------
        bottom_frame = tk.Frame(self, bg="#BCEE68")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        tk.Label(bottom_frame, text="Vinder:",
                 font=("Helvetica", 14, "bold"),
                 bg="#BCEE68").pack(side="left", padx=5)
        self.winning_var = tk.StringVar()
        self.winning_combobox = ttk.Combobox(bottom_frame,
                                             textvariable=self.winning_var,
                                             values=list(self.categories.keys()),
                                             state="disabled",
                                             font=("Helvetica", 12))
        self.winning_combobox.pack(side="left", padx=5)

        self.confirm_winner_button = tk.Button(
            bottom_frame, text="Confirm Winner",
            command=self.confirm_winner,
            state="disabled",
            font=("Helvetica", 12, "bold"),
            bg="#FFA07A"  # light salmon
        )
        self.confirm_winner_button.pack(side="left", padx=5)

        self.result_label = tk.Label(bottom_frame, text="",
                                     font=("Courier", 13),
                                     bg="#BCEE68",
                                     anchor="nw",
                                     justify="left")
        self.result_label.pack(side="left", padx=20)

    def build_category_buttons(self):
        """Create a 4-column grid of category buttons."""
        for widget in self.category_frame.winfo_children():
            widget.destroy()

        columns = 4
        cat_list = list(self.categories.keys())
        for i, cat_name in enumerate(cat_list):
            row = i // columns
            col = i % columns
            btn = tk.Button(
                self.category_frame,
                text=cat_name,
                font=("Helvetica", 12, "bold"),
                width=12,  # adjust to fit text
                command=lambda c=cat_name: self.select_category(c),
                bg="#E0FFFF"  # LightCyan
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="w")

    def select_category(self, cat_name):
        """User clicked a category button."""
        self.selected_category = cat_name
        self.current_category_label.config(text=f"Selected Category: {cat_name}")

    def add_or_update_bet(self):
        """Add or update a bet for the currently selected category."""
        if not self.selected_category:
            return  # no category selected

        member = self.member_name_var.get().strip()
        amount_str = self.amount_var.get().strip()

        if not member or not amount_str:
            return

        try:
            amount = float(amount_str)
        except ValueError:
            return

        current_val = self.categories[self.selected_category].get(member, 0.0)
        self.categories[self.selected_category][member] = current_val + amount

        # Clear the input fields
        self.member_name_var.set("")
        self.amount_var.set("")

        # Refresh the tree to show updated bets
        self.refresh_tree()

    def refresh_tree(self):
        """Clear the Treeview, then re-insert all categories + bets.
           Auto-expand categories that have bets (so they pop out)."""
        self.tree.delete(*self.tree.get_children())

        for cat_name, bets_dict in self.categories.items():
            # Insert a "parent" item for this category
            cat_id = self.tree.insert("", "end", text=cat_name, values=("",))

            # If there are bets, insert child items for each member
            # and then open (expand) the tree node so it's visible
            if bets_dict:
                for member, amount in bets_dict.items():
                    self.tree.insert(cat_id, "end", text=member, values=(amount,))
                
                # Expand category automatically if it has bets
                self.tree.item(cat_id, open=True)

    def start_countdown(self):
        """Start a non-blocking countdown with changing background colors."""
        if not self.countdown_running:
            self.countdown_running = True
            self.remaining_time = 60*20 # CHANGE IF NEEDED
            self.update_countdown()

    def update_countdown(self):
        if self.remaining_time > 0:
            self.countdown_label.config(text=f"Countdown: {self.remaining_time} sec remaining")
            color = self.countdown_colors[self.color_index % len(self.countdown_colors)]
            self.countdown_label.config(bg=color)
            self.color_index += 1

            self.remaining_time -= 1
            self.after(1000, self.update_countdown)
        else:
            # Countdown finished
            self.countdown_label.config(text="Countdown finished!", bg="#FF6347")
            self.disable_inputs_after_countdown()

    def disable_inputs_after_countdown(self):
        """Disable the bet controls and category buttons, enable winner selection."""
        self.member_name_entry.config(state="disabled")
        self.amount_entry.config(state="disabled")
        self.add_bet_button.config(state="disabled")
        self.start_button.config(state="disabled")

        for widget in self.category_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state="disabled")

        self.winning_combobox.config(state="readonly")
        self.confirm_winner_button.config(state="normal")

    def confirm_winner(self):
        """Calculate payouts for the chosen winning category."""
        winning_cat = self.winning_var.get()
        if not winning_cat or winning_cat not in self.categories:
            return

        # total pool: sum of bets across all categories
        total_pool = 0.0
        for cat_data in self.categories.values():
            total_pool += sum(cat_data.values())

        # sum in winning category
        sum_in_winning_cat = sum(self.categories[winning_cat].values())
        if sum_in_winning_cat == 0:
            self.result_label.config(text=f"No contributions in '{winning_cat}'! No payouts.")
            return

        payouts = {}
        for member, amount in self.categories[winning_cat].items():
            alpha = amount / sum_in_winning_cat
            payout = alpha * total_pool
            payouts[member] = payout

        # Display results
        lines = [
            f"Winning category: {winning_cat}",
            f"Total pool: {total_pool:.2f}",
            f"Sum in winning category: {sum_in_winning_cat:.2f}",
            "Payouts:",
        ]
        for member, p in payouts.items():
            lines.append(f" - {member}: {p:.2f}")

        self.result_label.config(text="\n".join(lines))


if __name__ == "__main__":
    app = ManyCategoriesTreeviewApp()
    app.mainloop()