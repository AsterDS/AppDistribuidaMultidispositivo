import socket
import json
import random

HOST = "0.0.0.0"
PORT = 5000

def send_msg(conn, msg):
    if not msg.endswith("\n"):
        msg += "\n"
    conn.sendall(msg.encode("utf-8")) 

def recv_msg(conn):
    data = conn.recv(1024)
    if not data:
        return None
    return data.decode("utf-8").strip()

class Player:
    def __init__(self):
        self.name = None
        self.gender = None
        self.weapon_name = None
        self.hp = 20  # default HP
        self.alive = True

    def __str__(self):
        return (f"Player(name={self.name}, gender={self.gender}, "
                f"weapon={self.weapon_name}, hp={self.hp}, alive={self.alive})")

    def set_weapon(self, weapon_choice):
        self.weapon_name = weapon_choice.lower()

    def get_damage_output(self):
        total_damage = 0
        if self.weapon_name == "dagger":
            total_damage = 2 + 2
        elif self.weapon_name == "sword":
            total_damage = 5
        elif self.weapon_name in ["great axe", "axe"]:
            total_damage = 10
            self.hp -= 2
            if self.hp <= 0:
                self.alive = False
        elif self.weapon_name == "bow":
            total_damage = 3
        else:
            total_damage = 1
        return total_damage

def load_scenes(json_path="scenes.json"): 
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def handle_scene(conn, scenes, player, scene_id):
    scene = scenes.get(scene_id)
    if not scene:
        send_msg(conn, f"[Server Error] Scene '{scene_id}' not found.\n")
        return None

    send_msg(conn, scene["description"])

    if scene_id == "fight_orc":
        return fight_orc(conn, player, scenes)

    if not scene["choices"]:
        return None

    for ch in scene["choices"]:
        send_msg(conn, f"{ch['option']}) {ch['prompt']}")
    send_msg(conn, "Choose an option:")

    user_choice = recv_msg(conn)
    if not user_choice:
        return None

    print(f"[Server Log] {player.name} in scene '{scene_id}' chose option '{user_choice}'")

    for ch in scene["choices"]:
        if ch["option"] == user_choice:
            return ch["next"]

    # Invalid choice
    send_msg(conn, "Invalid choice!")
    return None

def fight_orc(conn, player, scenes):
    
    orc_hp = 15
    send_msg(conn, f"The orc snarls at you. You have {player.hp} HP. The orc has {orc_hp} HP.")

    while player.alive and orc_hp > 0:
        send_msg(conn, "Attack? (yes/no)")
        answer = recv_msg(conn)
        if not answer:
            return None

        if answer.lower().startswith("y"):
            dmg = player.get_damage_output()
            orc_hp -= dmg
            send_msg(conn, f"You deal {dmg} damage to the orc! Orc's HP is now {orc_hp}.")
            if not player.alive:
                send_msg(conn, "Your reckless axe swing has drained your life.\n")
                break
        else:
            send_msg(conn, "You flee the battle. Not heroic, but you're safe... for now.")
            return "run_away"

        if orc_hp <= 0:
            break

        import random
        orc_damage = random.randint(2, 5)
        player.hp -= orc_damage
        send_msg(conn, f"The orc strikes back for {orc_damage} damage! Your HP is now {player.hp}.")
        if player.hp <= 0:
            player.alive = False
            break

    if not player.alive:
        send_msg(conn, "You have been slain by the orc (or your own weapon)!\n")
        return "death"
    if orc_hp <= 0:
        send_msg(conn, "You stand victorious over the defeated orc!\n")
        return "victory"

    return None

def run_adventure(conn, scenes):
    player = Player()

    send_msg(conn, "Welcome to the RPG Adventure!\nWhat is your name?")
    player_name = recv_msg(conn)
    if not player_name:
        return False
    player.name = player_name.strip()
    print(f"[Server Log] Player name: {player.name}")

    send_msg(conn, f"Hello {player.name}, what is your gender? (male/female)")
    gender = recv_msg(conn)
    if not gender:
        return False
    player.gender = gender.strip().lower()
    print(f"[Server Log] Player gender: {player.gender}")

    send_msg(conn, "Choose your starter weapon:\n1) dagger\n2) sword\n3) great axe\n4) bow")
    weapon_choice = recv_msg(conn)
    if not weapon_choice:
        return False

    if weapon_choice == "1":
        weapon_name = "dagger"
    elif weapon_choice == "2":
        weapon_name = "sword"
    elif weapon_choice == "3":
        weapon_name = "great axe"
    elif weapon_choice == "4":
        weapon_name = "bow"
    else:
        weapon_name = "fists"

    player.set_weapon(weapon_name)
    print(f"[Server Log] Player weapon: {player.weapon_name}")

    current_scene = "start"
    while current_scene:
        next_scene = handle_scene(conn, scenes, player, current_scene)
        if not next_scene:
            break
        current_scene = next_scene

    send_msg(conn, "Do you want to play again? (yes/no)")
    answer = recv_msg(conn)
    if answer and answer.lower().startswith("y"):
        return True
    return False

def handle_client(conn, addr, scenes):
    print(f"[Server Log] Connected by {addr}")
    while True:
        play_again = run_adventure(conn, scenes)
        if not play_again:
            send_msg(conn, "Thanks for playing! Goodbye!")
            break
    conn.close()
    print(f"[Server Log] Connection closed by {addr}")

def main():
    scenes = load_scenes("scenes.json")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[Server Log] Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr, scenes)

if __name__ == "__main__":
    main()
