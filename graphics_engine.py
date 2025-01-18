import pygame
import math

class Graphics:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Circle Game")
        self.font = pygame.font.Font(None, 36)
        
    def draw_game(self, players_data, foods_data):
        self.screen.fill((30, 30, 30))
        
        # Draw food
        for food in foods_data:
            x, y = food
            pygame.draw.circle(self.screen, (255,255,255), (int(float(x)), int(float(y))), 5)
            
        # Draw players
        for p in players_data:
            name, x, y, angle, color, radius, score = p
            x = float(x)
            y = float(y)
            angle = float(angle)
            radius = float(radius)
            
            # Draw player circle
            r,g,b = map(int, color.split('.'))
            pygame.draw.circle(self.screen, (r,g,b), (int(x), int(y)), int(radius))
            
            # Draw direction indicator (eye)
            eye_x = x + radius * 0.5 * math.cos(angle)
            eye_y = y - radius * 0.5 * math.sin(angle)
            pygame.draw.circle(self.screen, (255,255,255), (int(eye_x), int(eye_y)), int(radius/3))
            
            # Draw score under player
            score_text = self.font.render(str(score), True, (255,255,255))
            score_pos = (int(x - score_text.get_width()/2), int(y + radius + 5))
            self.screen.blit(score_text, score_pos)
            
        pygame.display.flip()
        
    def get_name(self):
        input_text = ""
        clock = pygame.time.Clock()
        
        while True:
            self.screen.fill((30, 30, 30))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and input_text:
                        return input_text
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif len(input_text) < 10 and event.unicode.isalnum():
                        input_text += event.unicode
                        
            # Draw prompt
            prompt = self.font.render("Enter your name:", True, (255,255,255))
            prompt_pos = (self.width/2 - prompt.get_width()/2, self.height/2 - 50)
            self.screen.blit(prompt, prompt_pos)
            
            # Draw input
            if input_text:
                text_surface = self.font.render(input_text, True, (255,255,255))
                text_pos = (self.width/2 - text_surface.get_width()/2, self.height/2)
                self.screen.blit(text_surface, text_pos)
                
            pygame.display.flip()
            clock.tick(60)
            
    def cleanup(self):
        pygame.quit()