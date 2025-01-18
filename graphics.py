import pygame
import math

# ------- Constants ---------
# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAPTION = "Circle Game"
FPS = 60

# UI
FONT_SIZE = 32
TITLE_FONT_SIZE = 48
INPUT_BOX_WIDTH = 400
INPUT_BOX_HEIGHT = 50
# --------------------------

class GraphicsEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        
    def draw_game_state(self, players_data, foods_data):
        """Draw the main game state including players, food, and scoreboard"""
        self.screen.fill(BLACK)
        
        # Draw food
        for food in foods_data:
            pygame.draw.circle(self.screen, WHITE, 
                             (int(food['x']), int(food['y'])), 
                             int(food['radius']))
        
        # Draw players
        for player in players_data:
            # Main player circle
            pygame.draw.circle(self.screen, player['color'],
                             (int(player['x']), int(player['y'])),
                             int(player['radius']))
            
            # Direction indicator (eye)
            eye_x = player['x'] + player['radius'] * 0.5 * math.cos(player['dir'])
            eye_y = player['y'] - player['radius'] * 0.5 * math.sin(player['dir'])
            pygame.draw.circle(self.screen, WHITE,
                             (int(eye_x), int(eye_y)),
                             int(player['radius'] / 3))
            
            # Winner crown (if won last match)
            if player['won_last_match']:
                crown_x = player['x']
                crown_y = player['y']
                crown_radius = player['radius'] / 3
                pygame.draw.circle(self.screen, GOLD,
                                 (int(crown_x), int(crown_y)),
                                 int(crown_radius))
        
        # Draw scoreboard
        self.draw_scoreboard(players_data)
        
        pygame.display.flip()
        self.clock.tick(FPS)
        
    def draw_scoreboard(self, players_data):
        """Draw the scoreboard in the top-left corner"""
        # Sort players by score
        sorted_players = sorted(players_data, key=lambda x: x['score'], reverse=True)
        
        # Draw header
        header = self.font.render("Scoreboard", True, WHITE)
        self.screen.blit(header, (10, 10))
        
        # Draw player scores
        for i, player in enumerate(sorted_players):
            score_text = f"{i+1}. {player['name']}: {player['score']}"
            score_surface = self.font.render(score_text, True, player['color'])
            self.screen.blit(score_surface, (10, 40 + i * 30))
            
    def draw_name_input(self, victory=False, winner_name=None):
        """Draw the name input screen with optional victory message"""
        self.screen.fill(BLACK)
        
        # Draw title/victory message
        if victory and winner_name:
            title_text = f"{winner_name} Wins!"
            title_surf = self.title_font.render(title_text, True, GOLD)
        else:
            title_text = "Enter Your Name"
            title_surf = self.title_font.render(title_text, True, WHITE)
            
        title_rect = title_surf.get_rect(centerx=SCREEN_WIDTH/2, 
                                       centery=SCREEN_HEIGHT/3)
        self.screen.blit(title_surf, title_rect)
        
        # Draw input box
        input_box = pygame.Rect((SCREEN_WIDTH - INPUT_BOX_WIDTH)/2,
                              SCREEN_HEIGHT/2,
                              INPUT_BOX_WIDTH,
                              INPUT_BOX_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, input_box, 2)
        
        pygame.display.flip()
        self.clock.tick(FPS)
        
    def get_name_input(self, victory=False, winner_name=None):
        """Handle name input from user"""
        input_text = ""
        typing = True
        
        while typing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and input_text:
                        return input_text
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        # Limit name length and only accept printable characters
                        if len(input_text) < 15 and event.unicode.isprintable():
                            input_text += event.unicode
            
            # Redraw screen
            self.draw_name_input(victory, winner_name)
            
            # Draw current input text
            if input_text:
                text_surface = self.font.render(input_text, True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, 
                                                        SCREEN_HEIGHT/2 + INPUT_BOX_HEIGHT/2))
                self.screen.blit(text_surface, text_rect)
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
    def cleanup(self):
        """Clean up pygame resources"""
        pygame.quit()