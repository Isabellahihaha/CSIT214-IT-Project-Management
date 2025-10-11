#frist version
# --- Configuration for Status and Rewards ---
STATUS_TIERS = {
    "Blue": 0,
    "Silver": 5000,   # Requires 5,000 points
    "Gold": 15000,    # Requires 15,000 points
    "Diamond Elite": 50000 # Requires 50,000 points
}

REWARDS = {
    "LOUNGE_ACCESS": 5000,
    "BUSINESS_UPGRADE": 15000,
    "REGIONAL_FLIGHT": 50000
}

# --- LoyaltyMember Class ---

class LoyaltyMember:
    """Represents a single FlyDreamAir loyalty program member."""
    # Class counter to generate simple, sequential IDs without external libraries
    _next_id = 1000 

    def __init__(self, name, member_id=None, initial_points=0):
        # Assign a sequential ID or use a provided one
        if member_id is None:
            self.member_id = LoyaltyMember._next_id
            LoyaltyMember._next_id += 1
        else:
            self.member_id = member_id

        self.name = name
        self.points = initial_points
        self.status = self._get_status_from_points(initial_points)

    def _get_status_from_points(self, points):
        """Determines the member's status tier based on their current points."""
        if points >= STATUS_TIERS["Diamond Elite"]:
            return "Diamond Elite"
        elif points >= STATUS_TIERS["Gold"]:
            return "Gold"
        elif points >= STATUS_TIERS["Silver"]:
            return "Silver"
        else:
            return "Blue"

    def update_status(self):
        """Checks if the member qualifies for a status upgrade and updates it."""
        new_status = self._get_status_from_points(self.points)
        if new_status != self.status:
            old_status = self.status
            self.status = new_status
            return f"🎉 Status upgraded from {old_status} to {self.status}!"
        return None

    def __str__(self):
        """String representation for printing member details."""
        return f"Member ID: {self.member_id} | Name: {self.name} | Points: {self.points:,} | Status: {self.status}"

# --- LoyaltyProgram Manager Class ---

class LoyaltyProgram:
    """Manages all members, transactions, and core program logic."""
    def __init__(self):
        # Dictionary to store members with ID as key for quick lookup
        self.members = {}

    def enroll_member(self, name):
        """Creates a new member and adds them to the program."""
        member = LoyaltyMember(name)
        self.members[member.member_id] = member
        print(f"✅ Enrolled new member: {member.name} (ID: {member.member_id})")
        return member

    def earn_points(self, member_id, flight_cost):
        """
        Calculates and adds points to a member's account based on flight cost.
        Elite tiers earn bonus points.
        """
        member = self.members.get(member_id)
        if not member:
            print(f"❌ Error: Member ID {member_id} not found.")
            return False

        # Base earning rate: 5 points per dollar
        base_points = int(flight_cost * 5)
        
        # Apply status bonus multiplier
        multiplier = 1.0
        if member.status == "Silver":
            multiplier = 1.2
        elif member.status == "Gold":
            multiplier = 1.5
        elif member.status == "Diamond Elite":
            multiplier = 2.0
            
        earned_points = int(base_points * multiplier)
        member.points += earned_points
        
        print(f"✅ {member.name} earned {earned_points:,} points (Cost: ${flight_cost:.2f}). Total points: {member.points:,}.")
        
        # Check and announce status change
        status_message = member.update_status()
        if status_message:
            print(status_message)
            
        return True

    def redeem_points(self, member_id, reward_key):
        """Redeems points for a specified reward."""
        member = self.members.get(member_id)
        if not member:
            print(f"❌ Error: Member ID {member_id} not found.")
            return False

        reward_cost = REWARDS.get(reward_key)
        if reward_cost is None:
            print(f"❌ Error: Invalid reward key '{reward_key}'.")
            return False

        if member.points < reward_cost:
            print(f"❌ Redemption failed for {member.name}: Not enough points ({member.points:,} < {reward_cost:,} required for {reward_key.replace('_', ' ').title()}).")
            return False

        member.points -= reward_cost
        print(f"✅ {member.name} redeemed {reward_cost:,} points for {reward_key.replace('_', ' ').title()}. Remaining points: {member.points:,}.")
        
        member.update_status()
        
        return True

    def get_member_details(self, member_id):
        """Retrieves and prints a member's full details."""
        member = self.members.get(member_id)
        if member:
            return member
        return None

# --- Demonstration ---

if __name__ == "__main__":
    print("--- FlyDreamAir Loyalty Program Simulation ---")
    program = LoyaltyProgram()

    # 1. Enroll Members - IDs will be 1000, 1001, 1002
    member_a = program.enroll_member("Alex Johnson")
    member_b = program.enroll_member("Bella Chen")
    member_c = program.enroll_member("Chris Evans")
    print("-" * 40)

    # 2. Earn Points (Initial Earning & Status Check)
    program.earn_points(member_a.member_id, 1000) # Reaches Silver
    program.earn_points(member_b.member_id, 500)  
    program.earn_points(member_c.member_id, 3000) # Reaches Gold

    # 3. Alex (Silver) earns more to reach Gold
    print("\n--- Alex's Journey to Gold ---")
    program.earn_points(member_a.member_id, 2000) # Should trigger an upgrade message
    print("-" * 40)
    
    # 4. Bella (Blue) attempts redemption without enough points
    print("\n--- Bella's Redemption Attempt ---")
    program.redeem_points(member_b.member_id, "LOUNGE_ACCESS") 
    print("-" * 40)
    
    # 5. Chris (Gold) earns and then redeems
    print("\n--- Chris's Redemption ---")
    program.earn_points(member_c.member_id, 1000) 
    program.redeem_points(member_c.member_id, "BUSINESS_UPGRADE") 
    
    # Final Summary
    print("\n" + "=" * 50)
    print("FINAL MEMBER STATUSES:")
    print("=" * 50)
    for member_id in program.members:
        member = program.get_member_details(member_id)
        print(member)
