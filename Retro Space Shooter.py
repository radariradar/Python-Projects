import math
import os
import random
import pygame

pygame.init()
pygame.mixer.init()

try:
    shoot_sound = pygame.mixer.Sound('chakong-laser-gun-shot-sound-future-sci-fi-lazer-wobble-chakongaudio-174883.mp3')
    blast_sound = pygame.mixer.Sound('freesound_community-blast-37988.mp3')
    power_up_sound = pygame.mixer.Sound('yodguard-level-up-2-540176.mp3')
    normal_score_sound = pygame.mixer.Sound('floraphonic-cute-level-up-3-189853.mp3')
    highscore_sound = pygame.mixer.Sound('vadim_makes_sound-retro-arcade-level-up-552982.mp3')

    shoot_sound.set_volume(0.2)
    blast_sound.set_volume(0.3)
    power_up_sound.set_volume(0.5)
    normal_score_sound.set_volume(0.6)
    highscore_sound.set_volume(0.8)
except FileNotFoundError:
    blast_sound = power_up_sound = normal_score_sound = highscore_sound = None
# --- 1. WINDOW SETUP ---
WIDTH = 1400
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Space Shooter")

clock = pygame.time.Clock()
FPS = 30  # Bumped to 60 for smooth controls

# --- 2. ASSET LOADING ---
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_PATH, "retro-futurism-style-with-purple-space-background-free-vector.jpg")

try:
    bg = pygame.image.load(IMAGE_PATH).convert()
    bg_width = bg.get_width()
except FileNotFoundError:
    bg = pygame.Surface((WIDTH, HEIGHT))
# Load background (if missing, fallback to dar
    bg.fill((20, 10, 30))
    bg_width = WIDTH

# --- 3. GAME VARIABLES ---
def reset_game():
    """Resets all variables so you can restart cleanly."""
    return {
        "player_x": 1200,
        "player_y": 300,
        "player_speed": 7,
        "base_speed": 4,  # Global speed multiplier for scrolling & enemies
        "scroll": 0,
        "lasers": [],     # [{rect: Rect, speed: int}]
        "enemies": [],    # [{rect: Rect}]
        "explosions": [], # [{x: int, y: int, radius: float, color: tuple}]
        "enemy_spawn_timer": 0,
        'special_effects': [],
        'special_effects_spawn_timer' : 0,
        "score": 0,
        "game_over": False,
        'new_highscore': False,
        "highscore_msg": "",
        'active_powerup' : None,
        'powerup_timer' : 0,
        'game_over_sound': False
    }

game = reset_game()
tiles = math.ceil(WIDTH / bg_width) + 1
font = pygame.font.SysFont("arial", 32, bold=True)

highscore = 0

# --- 4. MAIN GAME LOOP ---
run = True
while run:
    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            # Shoot Laser (SPACE)
            if event.key == pygame.K_SPACE and not game["game_over"]:
                if game["active_powerup"] == "double_laser":
                    # Spawn 2 lasers slightly above and below the center of the ship
                    laser1 = pygame.Rect(game["player_x"], game["player_y"] + 5, 20, 6)
                    laser2 = pygame.Rect(game["player_x"], game["player_y"] + 25, 20, 6)
                    game["lasers"].extend([laser1, laser2])
                else:
                    # Standard single laser
                    laser_rect = pygame.Rect(game["player_x"], game["player_y"] + 15, 20, 6)
                    game["lasers"].append(laser_rect)
                    # Restart Game (R)
                if shoot_sound:
                    shoot_sound.play()
            if event.key == pygame.K_r and game["game_over"]:
                game = reset_game()

    # --- GAMEPLAY LOGIC (Only runs if NOT game over) ---
    if not game["game_over"]:

        # A. PLAYER MOVEMENT (Up / Down)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and game["player_y"] > 0:
            game["player_y"] -= game["player_speed"]
        if keys[pygame.K_DOWN] and game["player_y"] < HEIGHT - 40:
            game["player_y"] += game["player_speed"]

        # B. SCROLLING BACKGROUND
        game["scroll"] -= game["base_speed"]
        if abs(game["scroll"]) > bg_width:
            game["scroll"] = 0

        # C. MOVE LASERS (Shooting Left)
        for laser in game["lasers"][:]:
            laser.x -= 15  # Lasers fly quickly to the left
            if laser.x < 0:
                game["lasers"].remove(laser)

        # D1. SPAWN ENEMIES (From Left)
        game["enemy_spawn_timer"] += 1
        if game["enemy_spawn_timer"] > 45:  # Spawn every 45 frames
            enemy_y = random.randint(50, HEIGHT - 90)
            enemy_rect = pygame.Rect(-40, enemy_y, 40, 40)
            game["enemies"].append(enemy_rect)
            game["enemy_spawn_timer"] = 0

        #D2. Spawn Special Effects(from left)
        game["special_effects_spawn_timer"] += 0.2
        if game["special_effects_spawn_timer"] > 45:  # Spawn every 45 frames
            special_y = random.randint(50, HEIGHT - 90)
            special_rect = pygame.Rect(-40, special_y, 40, 40)
            game["special_effects"].append(special_rect)
            game["special_effects_spawn_timer"] = 0
        
        # E1. MOVE ENEMIES & CHECK GAME OVER
        for enemy in game["enemies"][:]:
            enemy.x += game["base_speed"]  # Move right toward player
            # Game Over condition: Enemy escapes past player location
            if enemy.x >= game["player_x"]:
                game["game_over"] = True

        # E2. Move Special Effects 
        for special in game['special_effects'][:]:
            special.x += game['base_speed']
            target_y = game["player_y"] + 20  # Target the center of the ship
            if special.centery < target_y:
                special.y += 2  # Move down toward player
            elif special.centery > target_y:
                special.y -= 2
            if special.x >= bg_width:
                game['special_effects'].remove(special)

            

        # F1. COLLISION DETECTION (Laser hits Enemy)
        for laser in game["lasers"][:]:
            for enemy in game["enemies"][:]:
                if laser.colliderect(enemy):
                    # Create explosion particles at collision point
                    for _ in range(12):
                        game["explosions"].append(
                            {
                                "x": enemy.centerx,
                                "y": enemy.centery,
                                "vx": random.uniform(-4, 4),
                                "vy": random.uniform(-4, 4),
                                "radius": random.randint(4, 9),
                                "color": random.choice(
                                    [(255, 200, 0), (255, 80, 0), (255, 255, 200)]
                                ),
                            }
                        )
                    if blast_sound:
                        blast_sound.play()
                    
                    # Remove hit entities
                    if laser in game["lasers"]:
                        game["lasers"].remove(laser)
                    if enemy in game["enemies"]:
                        game["enemies"].remove(enemy)

                    # Update Score and Increase Speed!
                    game["score"] += 1
                    game["base_speed"] += 0.3  # Speed increases every hit!

        # F2. COLLISION: Laser hits Special Effect Circle
        for laser in game["lasers"][:]:
            for special in game["special_effects"][:]:
                if laser.colliderect(special):
                    # 1. Cyan explosion particles
                    for _ in range(12):
                        game["explosions"].append({
                            "x": special.centerx,
                            "y": special.centery,
                            "vx": random.uniform(-4, 4),
                            "vy": random.uniform(-4, 4),
                            "radius": random.randint(4, 9),
                            "color": (0, 255, 255)
                        })

                 # 2. Pick a random superpower!
                    game["active_powerup"] = random.choice(["double_laser", "speed_boost"])
                    game["powerup_timer"] = 150  # 150 frames at 30 FPS = 5 seconds

                    # 3. Apply speed boost immediately if selected
                    if game["active_powerup"] == "speed_boost":
                        game["player_speed"] = 14  # Double speed (from 7 to 14)

                    # 4. Remove laser and special effect circle
                    if laser in game["lasers"]:
                        game["lasers"].remove(laser)
                    if special in game["special_effects"]:
                        game["special_effects"].remove(special)

                    if power_up_sound:
                        power_up_sound.play()
                    
        # G. UPDATE EXPLOSION PARTICLES
        for particle in game["explosions"][:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["radius"] -= 0.3  # Particles shrink over time
            if particle["radius"] <= 0:
                game["explosions"].remove(particle)

        # H. POWER-UP TIMER MANAGEMENT
        if game["powerup_timer"] > 0:
            game["powerup_timer"] -= 1
            if game["powerup_timer"] == 0:
                # Timer expired! Reset player stats
                game["active_powerup"] = None
                game["player_speed"] = 7  # Reset back to default speed

    # --- DRAWING EVERYTHING ---

    # 1. Background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + game["scroll"], 0))

    # 2. Lasers (Neon Green Rectangles)
    for laser in game["lasers"]:
        pygame.draw.rect(screen, (0, 255, 120), laser)

    # 3. Enemies (Red Triangles pointing Right)
    for enemy in game["enemies"]:
        p1 = (enemy.right, enemy.centery)
        p2 = (enemy.left, enemy.top)
        p3 = (enemy.left, enemy.bottom)
        pygame.draw.polygon(screen, (255, 50, 80), [p1, p2, p3])

     # 4. Special Effects (Green Circles)
    for special in game['special_effects'][:]:
        pygame.draw.circle(screen, (0, 122, 122),special.center, 40)

    # 5. Player Spaceship (Blue Triangle pointing Left)
    player_rect = pygame.Rect(game["player_x"], game["player_y"], 40, 40)
    pt1 = (player_rect.left, player_rect.centery)
    pt2 = (player_rect.right, player_rect.top)
    pt3 = (player_rect.right, player_rect.bottom)
    pygame.draw.polygon(screen, (0, 200, 255), [pt1, pt2, pt3])

    # 6. Explosions
    for particle in game["explosions"]:
        pygame.draw.circle(
            screen,
            particle["color"],
            (int(particle["x"]), int(particle["y"])),
            int(particle["radius"]),
        )

    # 7. UI HUD (Score & Current Speed)
    
    score_txt = font.render(
        f"Score: {game['score']}  |  Speed: {game['base_speed']:.1f} \n Highscore: {highscore} ",
        True,
        (255, 255, 255),
    )
    screen.blit(score_txt, (20, 20))

    # Display active power-up & timer
    if game["active_powerup"]:
        seconds_left = math.ceil(game["powerup_timer"] / FPS)
        p_name = "DOUBLE LASERS" if game["active_powerup"] == "double_laser" else "SUPER SPEED"
        pw_txt = font.render(f"POWER-UP: {p_name} ({seconds_left}s)", True, (0, 255, 255))
        screen.blit(pw_txt, (20, 60))

    # 8. Checks if a new Highscore was achieved
    if game["game_over"]:
        if game['score'] > highscore:
            highscore = game ['score']
            game['new_highscore'] = True
        if game['new_highscore']:
            game['highscore_msg'] = f"Congratulations! New Highscore achieved: {highscore}"
            if game['game_over_sound'] == False:
                highscore_sound.play()
                game['game_over_sound'] = True
        else:
            game['highscore_msg'] = f"Current Highscore: {highscore}"
            if game['game_over_sound'] == False:
                normal_score_sound.play()
                game['game_over_sound'] = True


        # 9. Game Over Overlay
        over_txt = font.render(f"GAME OVER! Press 'R' to Restart ", True, (255, 255, 255))
        text_rect = over_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(over_txt, text_rect)

        hs_txt = font.render(game['highscore_msg'], True, (255, 255, 0))
        screen.blit(hs_txt, (WIDTH // 2 - hs_txt.get_width() //2, 400))



    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
