import pygame
import sys

class Screen:
    
    def __init__(self):
    
        # Initialize Pygame
        pygame.init()

        # Constants for the window dimensions
        self.WIDTH = 800
        self.HEIGHT = 800

        # Create the game window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tichu")

        # Define colors
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255,100,100)
        self.GREEN = (100,255,100)
        self.BLUE = (100,100,255)
        self.colors = [self.BLACK, self.BLUE ,self.GREEN, self.RED]

        self.values = ["Hound", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "Dragon", "Phoenix"]

        self.font = pygame.font.Font(None, 26)

        self.screen.fill((100,100,100))

    def display_cards(self,cards):

        x = (self.WIDTH-40*len(cards))/2
        y = self.HEIGHT/2-80
        for i in range(0, len(cards)):
            self.display_card(x+i*40,y,cards[i][1],cards[i][0])


    def display_card(self,x,y,color,value):
        width = 50
        height = 100
        pygame.draw.rect(self.screen, self.colors[color], (x, y, width, height))

        # Render and draw the text
        text_surface = self.font.render(self.values[value], True, self.WHITE)
        text_rect = text_surface.get_rect(center = (x+width/2, y+height/2))
        self.screen.blit(text_surface, text_rect)

    def display_player(self,x,y,name,team):
        circle_color = (255, 0, 0)  # Red color
        circle_radius = 30
        pygame.draw.circle(self.screen, circle_color, (x,y), circle_radius)
        # Render and draw the text
        text_surface = self.font.render(name, True, self.WHITE)
        text_rect = text_surface.get_rect(center = (x, y-10))
        self.screen.blit(text_surface, text_rect)

        text_surface = self.font.render(team, True,self.WHITE)
        text_rect = text_surface.get_rect(center = (x, y+10))
        self.screen.blit(text_surface, text_rect)
        
    def display_scores(self,score_A,score_B,x=0,y=0, color = (255,255,255)):
        text_surface = self.font.render("A", True, color)
        text_rect = text_surface.get_rect(center = (x+30,y+20))
        self.screen.blit(text_surface, text_rect)
        text_surface = self.font.render(str(score_A), True, color)
        text_rect = text_surface.get_rect(center = (x+30,y+60))
        self.screen.blit(text_surface, text_rect)

        text_surface = self.font.render("B", True, color)
        text_rect = text_surface.get_rect(center = (x+100,y+20))
        self.screen.blit(text_surface, text_rect)
        text_surface = self.font.render(str(score_B), True, color)
        text_rect = text_surface.get_rect(center = (x+100, y+60))
        self.screen.blit(text_surface, text_rect)

        pygame.draw.line(self.screen, color, (x+10,y+40), (x+126,y+40), 3)
        pygame.draw.line(self.screen, color, (x+30+35,y+10), (x+30+35,y+70),3)

    #def display_tichus(p0,p1,p2,p3):
     #   for i in range(0,4):

   
        
if __name__ == "__main__":
        cards = [(1,2),(11,3),(2,0),(3,0),(0,0),(1,2),(11,3),(2,0),(3,0),(0,0),(1,2),(11,3),(2,0),(3,0)]
        s = Screen()
        finished_round = False
        while(not finished_round):

            s.display_player(400,50,"Bot0", "A")
            s.display_player(400,730,"Bot1", "A")
            s.display_player(60,370,"Bot2", "B")
            s.display_player(750,370,"Bot3", "B")

            s.display_cards(cards)

            s.display_scores(score_A=0,score_B=0,x=10,y=10)

            # Update the display
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished_round = True


        
