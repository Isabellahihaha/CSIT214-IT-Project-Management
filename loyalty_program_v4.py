# fourth version
# --- Configuration for Status and Rewards ---
STATUS_TIERS = {
    "Nova": 0,
    "Orbit": 5000,
    "Galaxy": 12000,
    "Cosmos": 50000
}

REWARDS = {
    "LOUNGE_ACCESS": 5000,
    "BUSINESS_UPGRADE": 12000,
    "REGIONAL_FLIGHT": 50000
}

# --- LoyaltyMember Class ---
class LoyaltyMember:
    """Represents a single FlyDreamAir loyalty program member."""
    _next_id = 1000

    def __init__(self, name, member_id=None, initial_points=0):
        if member_id is None:
            self.member_id = LoyaltyMember._next_id
            LoyaltyMember._next_id += 1
        else:
            self.member_id = member_id
        self.name = name
        self.points = max(0, int(initial_points))
        self.status = self._get_status_from_points(self.points)
        # NEW: keep a very simple transaction history
        self.history = []  # list of tuples: (type, detail)

    def _get_status_from_points(self, points):
        """Determines member's tier."""
        if points >= STATUS_TIERS["Cosmos"]:
            return "Cosmos"
        elif points >= STATUS_TIERS["Galaxy"]:
            return "Galaxy"
        elif points >= STATUS_TIERS["Orbit"]:
            return "Orbit"
        else:
            return "Nova"

    def update_status(self):
        """Updates member tier if qualified."""
        new_status = self._get_status_from_points(self.points)
        if new_status != self.status:
            old = self.status
            self.status = new_status
            self.add_history("STATUS", f"{old} → {self.status}")
            print(f"🎉 Status upgraded from {old} → {self.status}")
        return self.status

    def add_history(self, htype, detail):
        self.history.append((htype, detail))

    def __str__(self):
        return f"ID:{self.member_id} | {self.name:<12} | Points:{self.points:>6} | Status:{self.status}"


# --- Utility: next tier progress ---
def next_tier_progress(points):
    """Return (next_tier_name, next_threshold, remaining_points). If at top tier, next_tier_name is None."""
    tiers = sorted(STATUS_TIERS.items(), key=lambda kv: kv[1])  # ascending by threshold
    for name, thr in tiers:
        if points < thr:
            return name, thr, max(0, thr - points)
    return None, None, 0  # already at top


# --- LoyaltyProgram Class ---
class LoyaltyProgram:
    """Manages members, transactions, and rewards."""
    def __init__(self):
        self.members = {}

    def enroll_member(self, name):
        member = LoyaltyMember(name)
        self.members[member.member_id] = member
        print(f"✅ Enrolled: {member.name} (ID:{member.member_id})")
        member.add_history("ENROLL", "new member")
        return member

    def earn_points(self, member_id, flight_cost):
        member = self.members.get(member_id)
        if not member:
            print(f"❌ Member {member_id} not found.")
            return
        # NEW: basic validation
        try:
            flight_cost = float(flight_cost)
        except ValueError:
            print("⚠️ Flight cost must be a number.")
            return
        if flight_cost <= 0:
            print("⚠️ Flight cost must be positive.")
            return

        base = int(flight_cost * 5)
        bonus = {"Nova":1.0,"Orbit":1.2,"Galaxy":1.5,"Cosmos":2.0}[member.status]
        earned = int(base * bonus)
        member.points += earned
        print(f"💰 {member.name} earned {earned:,} points from ${flight_cost:.2f}. Total: {member.points:,}.")
        member.add_history("EARN", f"+{earned} (from ${flight_cost:.2f})")
        member.update_status()

    def redeem_points(self, member_id, reward_key):
        member = self.members.get(member_id)
        if not member:
            print(f"❌ Member {member_id} not found.")
            return
        # NEW: more tolerant key (allow "lounge access")
        normalized = str(reward_key).strip().upper().replace(" ", "_")
        cost = REWARDS.get(normalized)
        if not cost:
            print("⚠️ Invalid reward key.")
            return
        if member.points < cost:
            print(f"❌ Not enough points for {normalized.replace('_',' ').title()}. Need {cost:,}, has {member.points:,}.")
            return

        member.points -= cost
        print(f"🎁 {member.name} redeemed {normalized.replace('_',' ').title()}! Remaining {member.points:,}.")
        member.add_history("REDEEM", f"-{cost} for {normalized.replace('_',' ').title()}")
        member.update_status()

    def show_rewards(self):
        print("\n🎯 Available Rewards:")
        for r, c in REWARDS.items():
            print(f" - {r.replace('_',' ').title():20} : {c:,} pts")

    # NEW: preview rewards affordable right now
    def preview_affordable_rewards(self, member_id):
        m = self.members.get(member_id)
        if not m:
            print(f"❌ Member {member_id} not found.")
            return
        print(f"\n🛍️ Rewards {m.name} can redeem now:")
        affordable = [(k, v) for k, v in REWARDS.items() if m.points >= v]
        if not affordable:
            print(" - None (earn more points!)")
        else:
            for k, v in sorted(affordable, key=lambda kv: kv[1]):
                print(f" - {k.replace('_',' ').title():20} : {v:,} pts")

    # NEW: detail view with next tier hint & last actions
    def show_member_details(self, member_id):
        m = self.members.get(member_id)
        if not m:
            print(f"❌ Member {member_id} not found.")
            return
        print("\n👤 Member Detail")
        print(m)
        nxt_name, nxt_thr, remain = next_tier_progress(m.points)
        if nxt_name:
            print(f"🔜 {remain:,} points to reach {nxt_name} (at {nxt_thr:,} pts)")
        else:
            print("🏆 Already at top tier.")
        if m.history:
            print("📝 Recent history:")
            for htype, detail in m.history[-5:]:
                print(f" - {htype}: {detail}")

    def save_summary(self, filename="members_summary.txt"):
        """Saves all members' data to a local file."""
        with open(filename, "w") as f:
            f.write("=== FlyDreamAir Loyalty Member Summary ===\n")
            for m in self.members.values():
                f.write(str(m) + "\n")
        print(f"\n💾 Member data saved to {filename}")


# --- Demonstration ---
if __name__ == "__main__":
    print("=== FlyDreamAir Loyalty Program v4 ===")
    program = LoyaltyProgram()

    # Enroll members
    alex = program.enroll_member("Alex Johnson")
    bella = program.enroll_member("Bella Chen")

    # Earn points (with validation)
    program.earn_points(alex.member_id, 1500)
    program.earn_points(bella.member_id, 800)
    program.earn_points(bella.member_id, -10)   # will trigger validation warning

    # View rewards & preview what each can redeem now
    program.show_rewards()
    program.preview_affordable_rewards(alex.member_id)

    # Redeem (case-insensitive / space-tolerant key)
    program.redeem_points(alex.member_id, "lounge access")
    program.redeem_points(bella.member_id, "BUSINESS_UPGRADE")

    # Member detail page (next tier hint + short history)
    program.show_member_details(alex.member_id)

    # Save results
    program.save_summary()

    print("\nFinal Member List:")
    for m in program.members.values():
        print(m)