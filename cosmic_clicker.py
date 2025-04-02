import tkinter as tk
import random
import json
import os
import webbrowser

class CosmicClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Cosmic Clicker: Stellar Ascension")
        self.root.geometry("800x600")

        self.player_name = self.get_player_name()
        self.save_file = f"cosmic_clicker_{self.player_name}.json"
        self.load_game()

        self.energy_label = tk.Label(root, text="Cosmic Energy: 0")
        self.energy_label.pack()
        self.power_label = tk.Label(root, text="Stellar Power: 0")
        self.power_label.pack()
        self.crystal_label = tk.Label(root, text="Void Crystals: 0")
        self.crystal_label.pack()
        self.research_label = tk.Label(root, text="Research Points: 0")
        self.research_label.pack()
        self.rebirth_label = tk.Label(root, text=f"Rebirth Multiplier: {self.rebirth_multiplier:.2f}")
        self.rebirth_label.pack()

        self.click_button = tk.Button(root, text="Harness Cosmic Energy", command=self.harness_energy)
        self.click_button.pack()
        self.rebirth_button = tk.Button(root, text="Rebirth", command=self.rebirth)
        self.rebirth_button.pack()
        self.donate_button = tk.Button(root, text="Donate!", command=self.donate)
        self.donate_button.pack()

        self.upgrade_frame = tk.Frame(root)
        self.upgrade_frame.pack()

        for upgrade_name, upgrade_data in self.upgrades.items():
            upgrade_button = tk.Button(self.upgrade_frame, text=f"Buy {upgrade_name} ({upgrade_data['cost']})",
                                        command=lambda name=upgrade_name: self.buy_upgrade(name))
            upgrade_button.pack()
            upgrade_count_label = tk.Label(self.upgrade_frame, text=f"{upgrade_name}s: {self.upgrade_counts[upgrade_name]}")
            upgrade_count_label.pack()

        self.event_label = tk.Label(root, text="")
        self.event_label.pack()

        self.root.after(1000, self.update_resources)
        self.root.protocol("WM_DELETE_WINDOW", self.save_and_exit)

    def get_player_name(self):
        name = tk.simpledialog.askstring("Player Name", "Enter your player name:")
        if not name:
            name = "default"
        return name

    def load_game(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                data = json.load(f)
                self.cosmic_energy = data.get("cosmic_energy", 0)
                self.stellar_power = data.get("stellar_power", 0)
                self.void_crystals = data.get("void_crystals", 0)
                self.research_points = data.get("research_points", 0)
                self.rebirth_multiplier = data.get("rebirth_multiplier", 1)
                self.total_energy_generated = data.get("total_energy_generated", 0)
                self.upgrade_counts = data.get("upgrade_counts", {name: 0 for name in self.upgrades})
                self.energy_mult = data.get("energy_mult", 1)
                self.power_mult = data.get("power_mult", 1)
                self.crystal_mult = data.get("crystal_mult", 1)
                self.research_mult = data.get("research_mult", 1)
                for upgrade_name, upgrade_data in self.upgrades.items():
                    upgrade_data["cost"] = int(upgrade_data["base_cost"] * (upgrade_data["cost_scale"] ** self.upgrade_counts[upgrade_name]))
        else:
            self.cosmic_energy = 0
            self.stellar_power = 0
            self.void_crystals = 0
            self.research_points = 0
            self.rebirth_multiplier = 1
            self.total_energy_generated = 0
            self.upgrade_counts = {name: 0 for name in self.upgrades}
            self.energy_mult = 1
            self.power_mult = 1
            self.crystal_mult = 1
            self.research_mult = 1

    def save_game(self):
        data = {
            "cosmic_energy": self.cosmic_energy,
            "stellar_power": self.stellar_power,
            "void_crystals": self.void_crystals,
            "research_points": self.research_points,
            "rebirth_multiplier": self.rebirth_multiplier,
            "total_energy_generated": self.total_energy_generated,
            "upgrade_counts": self.upgrade_counts,
            "energy_mult": self.energy_mult,
            "power_mult": self.power_mult,
            "crystal_mult": self.crystal_mult,
            "research_mult": self.research_mult,
        }
        with open(self.save_file, "w") as f:
            json.dump(data, f)

    def save_and_exit(self):
        self.save_game()
        self.root.destroy()

    def harness_energy(self):
        self.cosmic_energy += 1 * self.rebirth_multiplier
        self.research_points += 0.1 * self.research_mult * self.rebirth_multiplier
        self.total_energy_generated += 1
        self.update_labels()

    def buy_upgrade(self, upgrade_name):
        upgrade_data = self.upgrades[upgrade_name]
        if self.cosmic_energy >= upgrade_data["cost"]:
            self.cosmic_energy -= upgrade_data["cost"]
            self.upgrade_counts[upgrade_name] += 1
            upgrade_data["cost"] = int(upgrade_data["base_cost"] * (upgrade_data["cost_scale"] ** self.upgrade_counts[upgrade_name]))
            if upgrade_data["type"] == "research":
                if "energy_mult" in upgrade_data: self.energy_mult *= upgrade_data["energy_mult"]
                if "power_mult" in upgrade_data: self.power_mult *= upgrade_data["power_mult"]
                if "crystal_mult" in upgrade_data: self.crystal_mult *= upgrade_data["crystal_mult"]
                if "research_mult" in upgrade_data: self.research_mult *= upgrade_data["research_mult"]

            self.update_labels()
            self.update_upgrade_buttons()

    def rebirth(self):
        self.rebirth_multiplier *= (1 + (self.total_energy_generated / 1000000))
        self.cosmic_energy = 0
        self.stellar_power = 0
        self.void_crystals = 0
        self.research_points = 0
        self.upgrade_counts = {name: 0 for name in self.upgrades}
        self.energy_mult = 1
        self.power_mult = 1
        self.crystal_mult = 1
        self.research_mult = 1
        for upgrade in self.upgrades.values():
            upgrade["cost"] = upgrade["base_cost"]
        self.total_energy_generated = 0
        self.update_labels()
        self.update_upgrade_buttons()

    def update_labels(self):
        self.energy_label.config(text=f"Cosmic Energy: {self.cosmic_energy:.2f}")
        self.power_label.config(text=f"Stellar Power: {self.stellar_power:.2f}")
        self.crystal_label.config(text=f"Void Crystals: {self.void_crystals}")
        self.research_label.config(text=f"Research Points: {self.research_points:.2f}")
        self.rebirth_label.config(text=f"Rebirth Multiplier: {self.rebirth_multiplier:.2f}")

    def update_upgrade_buttons(self):
        for upgrade_name, upgrade_data in self.upgrades.items():
            for widget in self.upgrade_frame.winfo_children():
                if isinstance(widget, tk.Button) and widget.cget("text").startswith(f"Buy {upgrade_name}"):
                    widget.config(text=f"Buy {upgrade_name} ({upgrade_data['cost']})")
                if isinstance(widget, tk.Label) and widget.cget("text").startswith(f"{upgrade_name}s:"):
                    widget.config(text=f"{upgrade_name}s: {self.upgrade_counts[upgrade_name]}")

    def update_resources(self):
        for upgrade_name, upgrade_data in self.upgrades.items():
            count = self.upgrade_counts[upgrade_name]
            if upgrade_data["type"] == "production":
                self.cosmic_energy += count * upgrade_data["energy_cps"] * self.energy_mult * self.rebirth_multiplier
                self.stellar_power += count * upgrade_data["power_cps"] * self.power_mult * self.rebirth_multiplier
                if random.random() < count * upgrade_data["crystal_chance"] * self.crystal_mult:
                    self.void_crystals += 1
        self.research_points += 0.01 * self.research_mult * self.rebirth_multiplier
        self.total_energy_generated += self.cosmic_energy

        self.trigger_random_event()
        self.update_labels()
        self.root.after(1000, self.update_resources)

    def trigger_random_event(self):
        for event_name, event_data in self.events.items():
            if random.random() < event_data["chance"]:
                event_data["effect"]()
                self.event_label.config(text=event_data["message"])
                self.root.after(3000, lambda: self.event_label.config(text=""))
                self.update_labels()
                return

    def donate(self):
        # Replace with your actual donation link!
        donation_link = "https://www.paypal.com/donate/?hosted_button_id=YOUR_DONATION_ID"
        webbrowser.open_new(donation_link)

    upgrades = {
        "Nebula Generator": {"base_cost": 50, "cost": 50, "energy_cps": 1, "power_cps": 0, "crystal_chance": 0.005, "cost_scale": 1.12, "type": "production"},
        "Stellar Forge": {"base_cost": 500, "cost": 500, "energy_cps": 5, "power_cps": 2, "crystal_chance": 0.02, "cost_scale": 1.15, "type": "production"},
        "Void Conduit": {"base_cost": 5000, "cost": 5000, "energy_cps": 20, "power_cps": 10, "crystal_chance": 0.05, "cost_scale": 1.18, "type": "production"},
        "Celestial Refinery": {"base_cost": 50000, "cost": 50000, "energy_cps": 100, "power_cps": 50, "crystal_chance": 0.1, "cost_scale": 1.20, "type": "production"},
        "Quantum Extractor": {"base_cost": 500000, "cost": 500000, "energy_cps": 500, "power_cps": 200, "crystal_chance": 0.2, "cost_scale": 1.22, "type": "production"},
        "Singularity Core": {"base_cost": 5000000, "cost": 5000000, "energy_cps": 2500, "power_cps": 1000, "crystal_chance": 0.3, "cost_scale": 1.25, "type": "production"},
        "Galactic Nexus": {"base_cost": 50000000, "cost": 50000000, "energy_cps": 12500, "power_cps": 5000, "crystal_chance": 0.4, "cost_scale": 1.27, "type": "production"},
        "Cosmic Fabricator": {"base_cost": 500000000, "cost": 500000000, "energy_cps": 62500, "power_cps": 25000, "crystal_chance": 0.5, "cost_scale": 1.3, "type": "production"},
        "Energy Efficiency": {"base_cost": 1000, "cost": 1000, "energy_mult": 1.1, "power_mult": 1, "crystal_mult": 1, "cost_scale": 1.2, "type": "research"},
        "Stellar Amplification": {"base_cost": 5000, "cost": 5000, "energy_mult": 1, "power_mult": 1.15, "crystal_mult": 1, "cost_scale": 1.25, "type": "research"},
        "Crystal Resonance": {"base_cost": 25000, "cost": 25000, "energy_mult": 1, "power_mult": 1, "crystal_mult": 1.2, "cost_scale": 1.3, "type": "research"},
        "Research Optimization": {"base_cost": 100000, "cost": 100000, "research_mult": 1.1, "cost_scale": 1.35, "type": "research"}
    }
    events = {
        "Cosmic Surge": {"effect": lambda: cosmic_energy *= 2, "chance": 0.003, "message": "A Cosmic Surge doubles your energy!"},
        "Stellar Alignment": {"effect": lambda: stellar_power *= 1.5, "chance": 0.002, "message": "Stellar Alignment boosts your power!"},
        "Void Rift": {"effect": lambda: void_crystals += 5, "chance": 0.0008, "message": "A Void Rift yields 5 crystals!"},
        "Energy Drain": {"effect": lambda: cosmic_energy = max(0, cosmic_energy // 2), "chance": 0.0015, "message": "An Energy Drain halves your energy!"},
        "Power Flux": {"effect": lambda: stellar_power = max(0, stellar_power - (stellar_power // 3)), "chance": 0.001, "message": "Power Flux reduces your stellar power!"},
        "Crystal Bloom": {"effect": lambda: void_crystals += 3, "chance": 0.0005, "message": "Crystal Bloom! +3 Void Crystals!"},
        "Research Breakthrough": {"effect": lambda: research_points += 10, "chance": 0.0003, "message": "Research Breakthrough! +10 Research Points!"}
    }
def create_html_file():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cosmic Clicker</title>
        <style>
            body {
                font-family: sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
            }
            #game-container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <div id="game-container">
            <h1>Cosmic Clicker</h1>
            <p>To play this game, you need to run the Python script:</p>
            <pre><code>python cosmic_clicker.py</code></pre>
            <p>Make sure you have Python and tkinter installed.</p>
            <p>This page is just a placeholder because GitHub Pages does not run python code.</p>
            <p>If you would like to donate to me, you can click the button in the python game.</p>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    create_html_file()
    root = tk.Tk()
    game = CosmicClicker(root)
    root.mainloop()
