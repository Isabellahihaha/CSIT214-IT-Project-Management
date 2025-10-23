# third version
# --- Configuration for Status and Rewards ---
STATUS_TIERS = {
    "Blue": 0,
    "Silver": 5000,
    "Gold": 15000,
    "Diamond Elite": 50000
}

REWARDS = {
    "LOUNGE_ACCESS": 5000,
    "BUSINESS_UPGRADE": 15000,
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
        self.points = initial_points
        self.status = self._get_status_from_points(initial_points)

    def _get_status_from_points(self, points):
        """Determines member's tier."""
        if points >= STATUS_TIERS["Diamond Elite"]:
            return "Diamond Elite"
        elif points >= STATUS_TIERS["Gold"]:
            return "Gold"
        elif points >= STATUS_TIERS["Silver"]:
            return "Silver"
        else:
            return "Blue"

    def update_status(self):
        """Updates member tier if qualified."""
        new_status = self._get_status_from_points(self.points)
        if new_status != self.status:
            old = self.status
            self.status = new_status
            print(f"🎉 Status upgraded from {old} → {self.status}")
        return self.status

    def __str__(self):
        return f"ID:{self.member_id} | {self.name:<12} | Points:{self.points:>6} | Status:{self.status}"


# --- LoyaltyProgram Class ---
class LoyaltyProgram:
    """Manages members, transactions, and rewards."""
    def __init__(self):
        self.members = {}

    def enroll_member(self, name):
        member = LoyaltyMember(name)
        self.members[member.member_id] = member
        print(f"✅ Enrolled: {member.name} (ID:{member.member_id})")
        return member

    def earn_points(self, member_id, flight_cost):
        member = self.members.get(member_id)
        if not member:
            print(f"❌ Member {member_id} not found.")
            return
        base = int(flight_cost * 5)
        bonus = {"Blue":1.0,"Silver":1.2,"Gold":1.5,"Diamond Elite":2.0}[member.status]
        earned = int(base * bonus)
        member.points += earned
        print(f"💰 {member.name} earned {earned:,} points from ${flight_cost:.2f}. Total: {member.points:,}.")
        member.update_status()

    def redeem_points(self, member_id, reward_key):
        member = self.members.get(member_id)
        if not member:
            print(f"❌ Member {member_id} not found.")
            return
        cost = REWARDS.get(reward_key)
        if not cost:
            print("⚠️ Invalid reward key.")
            return
        if member.points < cost:
            print(f"❌ Not enough points for {reward_key.replace('_',' ').title()}. Need {cost:,}, has {member.points:,}.")
            return
        member.points -= cost
        print(f"🎁 {member.name} redeemed {reward_key.replace('_',' ').title()}! Remaining {member.points:,}.")
        member.update_status()

    def show_rewards(self):
        print("\n🎯 Available Rewards:")
        for r, c in REWARDS.items():
            print(f" - {r.replace('_',' ').title():20} : {c:,} pts")

    def save_summary(self, filename="members_summary.txt"):
        """Saves all members' data to a local file."""
        with open(filename, "w") as f:
            f.write("=== FlyDreamAir Loyalty Member Summary ===\n")
            for m in self.members.values():
                f.write(str(m) + "\n")
        print(f"\n💾 Member data saved to {filename}")

# --- Demonstration ---
if __name__ == "__main__":
    print("=== FlyDreamAir Loyalty Program v3 ===")
    program = LoyaltyProgram()

    # Enroll members
    alex = program.enroll_member("Alex Johnson")
    bella = program.enroll_member("Bella Chen")

    # Earn points
    program.earn_points(alex.member_id, 1500)
    program.earn_points(bella.member_id, 800)

    # View rewards
    program.show_rewards()

    # Redeem
    program.redeem_points(alex.member_id, "LOUNGE_ACCESS")
    program.redeem_points(bella.member_id, "BUSINESS_UPGRADE")

    # Save results
    program.save_summary()

    print("\nFinal Member List:")
    for m in program.members.values():
        print(m)