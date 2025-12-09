import pygame

class ScoreTracker:
    """Handles all score tracking and display for the Pac-Man game"""
    
    def __init__(self, total_pellets, pellet_value=10):
        """
        Initialize the score tracker
        
        Args:
            total_pellets: Total number of pellets in the game
            pellet_value: Points awarded per pellet (default: 10)
        """
        self.score = 0
        self.pellets_eaten = 0
        self.total_pellets = total_pellets
        self.pellet_value = pellet_value
    
    def eat_pellet(self, position):
        """
        Called when Pac-Man eats a pellet
        
        Args:
            position: (x, y) position of the pellet eaten
        
        Returns:
            tuple: (score, pellets_eaten, remaining_pellets)
        """
        self.score += self.pellet_value
        self.pellets_eaten += 1
        remaining = self.total_pellets - self.pellets_eaten
        return self.score, self.pellets_eaten, remaining
    
    def get_score(self):
        """Get current score"""
        return self.score
    
    def get_pellets_eaten(self):
        """Get number of pellets eaten"""
        return self.pellets_eaten
    
    def get_total_pellets(self):
        """Get total number of pellets"""
        return self.total_pellets
    
    def draw(self, window, pellets_remaining, width, height):
        """
        Draw the score and pellet count on the screen
        
        Args:
            window: Pygame window surface
            pellets_remaining: Number of pellets still in the game
            width: Window width
            height: Window height
        """
        try: 
            font = pygame.font.Font('assets/BitCountGridSingle.ttf', 20)
        except Exception:
            font = pygame.font.Font(None, 36)
        
        
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        window.blit(score_text, (10, 10))
        
        # Draw pellets remaining
        pellets_text = font.render(f"Pellets: {pellets_remaining}/{self.total_pellets}", True, (255, 255, 255))
        window.blit(pellets_text, (width - 200, 10))
        
        # Draw win message if all pellets eaten
        if pellets_remaining == 0:
            win_text = font.render("YOU WIN!", True, (0, 255, 0))
            text_rect = win_text.get_rect(center=(width//2, height//2))
            window.blit(win_text, text_rect)
    
    def print_stats(self):
        """Print final game statistics"""
        print(f"\nGame Over! Final Score: {self.score}")
        print(f"Pellets eaten: {self.pellets_eaten}/{self.total_pellets}")

