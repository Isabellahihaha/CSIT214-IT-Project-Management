# second version
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
        """Determines the member's status tier based on points."""
        if points >= STATUS_TIERS["Diamond Elite"]:
            return "Diamond Elite"
        elif points >= STATUS_TIERS["Gold"]:
            return "Gold"
        elif points >= STATUS_TIERS["Silver"]:
            return "Silver"
        else:
            return "Blue"

    def update_status(self):
        """Check if member qualifies for a higher tier."""
        new_status = self._get_status_from_points(self.points)
        if new_status != self.status:
            old_status = self.status
            self.status = new_status
            print(f"🎉 Status upgraded from {old_status} → {self.status}!")
        return self.status

    def __str__(self):
        return f"ID: {self.member_id} | Name: {self.name} | Points: {self.points:,} | Status: {self.status}"


# --- LoyaltyProgram Class ---
class LoyaltyProgram:
    """Manages all members and point operations."""
    def __init__(self):
        self.members = {}

    def enroll_member(self, name):
        """Registers a new member."""
        member = LoyaltyMember(name)
        self.members[member.member_id] = member
        print(f"✅ New member enrolled: {member}")
        return member

    def earn_points(self, member_id, flight_cost):
        """Earn points based on flight cost and member status."""
        member = self.members.get(member_id)
        if not member:
            print(f"❌ Member ID {member_id} not found.")
            return

        base_points = int(flight_cost * 5)
        multiplier = {"Blue": 1.0, "Silver": 1.2, "Gold": 1.5, "Diamond Elite": 2.0}[member.status]
        earned = int(base_points * multiplier)
        member.points += earned

        print(f"💰 {member.name} earned {earned:,} pts from a ${flight_cost:.2f} flight.")
        member.update_status()

    def redeem_points(self, member_id, reward_key):
        """Redeems a reward if member has enough points."""
        member = self.members.get(member_id)
        if not member:
            print(f"❌ Member ID {member_id} not found.")
            return

        reward_cost = REWARDS.get(reward_key)
        if not reward_cost:
            print("❌ Invalid reward key.")
            return

        if member.points < reward_cost:
            print(f"⚠️ Not enough points for {member.name} ({member.points:,}/{reward_cost:,}).")
            return

        member.points -= reward_cost
        print(f"🎁 {member.name} redeemed {reward_key.replace('_',' ').title()}! Remaining: {member.points:,} pts.")
        member.update_status()

    def show_rewards(self):
        """Displays available rewards."""
        print("\n🎯 Available Rewards:")
        for key, cost in REWARDS.items():
            print(f" - {key.replace('_', ' ').title()} : {cost:,} points")

    def get_member(self, member_id):
        return self.members.get(member_id)


# --- Demonstration ---
if __name__ == "__main__":
    print("=== FlyDreamAir Loyalty Program v2 ===")
    program = LoyaltyProgram()

    # Enroll
    alex = program.enroll_member("Alex Johnson")
    bella = program.enroll_member("Bella Chen")
    print("-" * 40)

    # Earn Points
    program.earn_points(alex.member_id, 1200)
    program.earn_points(bella.member_id, 300)
    print("-" * 40)

    # View Rewards
    program.show_rewards()
    print("-" * 40)

    # Attempt Redemption
    program.redeem_points(bella.member_id, "LOUNGE_ACCESS")
    program.redeem_points(alex.member_id, "LOUNGE_ACCESS")

    print("\nFinal Member Summary:")
    for member in program.members.values():
        print(member)