import pygame
import sys

class Screen:
    
    def __init__(self):
    
        # Initialize Pygame
        pygame.init()

        # Constants for the window dimensions
        self.WIDTH = 800
        self.HEIGHT = 700

        # Create the game window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tichu")

        # Define colors
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED =  (136,0,0)
        self.GREEN = (53,104,45)
        self.BLUE = (100,100,255)
        self.YELLOW = (229, 190, 1)

        self.colors = [self.BLACK, self.BLUE ,self.GREEN, self.RED, self.YELLOW]
        self.backgroundcolor = (225,200,150)
        self.values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.special_values = ["H","1", "D", "P"]

        self.font = pygame.font.Font(None, 26)

        self.font_big = pygame.font.Font(None, 36)
      
        self.player_positions = [(400,600),(750,290),(400,50),(60,290)]

   
       

        self.screen.fill(self.backgroundcolor)

    def display_cards(self,cards):
        
        pygame.draw.rect(self.screen, self.backgroundcolor, (100, self.HEIGHT/2-80,610,120))

        x = (self.WIDTH-40*len(cards))/2
        y = self.HEIGHT/2-80
        for i in range(0, len(cards)):
            self.display_card(x+i*40,y,cards[i][1],cards[i][0])

      
    def display_card(self,x,y,color,value):
        width = 50
        height = 90
        pygame.draw.rect(self.screen, self.colors[color], (x, y, width, height))

        pval = -1
        if(color == 4):
            pval = self.special_values[value]
        else:
            pval = self.values[value]
        
        # Render and draw the text
        text_surface = self.font.render(pval, True, self.WHITE)
        text_rect = text_surface.get_rect(center = (x+width/2, y+height/2))
        self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, (48,32,24), (x,y, 4, height))
        pygame.draw.rect(self.screen, (48,32,24), (x+width-4,y, 4, height))
        pygame.draw.rect(self.screen, (48,32,24), (x,y, width, 4))
        pygame.draw.rect(self.screen, (48,32,24), (x,y+height-4, width, 4))



    def display_player(self,x,y,name,team, circle_color=(255,0,0)):
  
        font_color = (0,0,0)
        circle_radius = 30
        pygame.draw.circle(self.screen, circle_color, (x,y), circle_radius)
        # Render and draw the text
        text_surface = self.font.render(name, True, font_color)
        text_rect = text_surface.get_rect(center = (x, y-10))
        self.screen.blit(text_surface, text_rect)

        text_surface = self.font.render(team, True,font_color)
        text_rect = text_surface.get_rect(center = (x, y+10))
        self.screen.blit(text_surface, text_rect)
        
    def display_scores(self,score_A,score_B,x=0,y=0, color = (0,0,0)):

        pygame.draw.rect(self.screen, self.backgroundcolor, (x+30-20,y+60-10,50,30))

        text_surface = self.font.render("A", True, color)
        text_rect = text_surface.get_rect(center = (x+30,y+20))
        self.screen.blit(text_surface, text_rect)
        text_surface = self.font.render(str(score_A), True, color)
        text_rect = text_surface.get_rect(center = (x+30,y+60))
        self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, self.backgroundcolor, (x+100-20,y+60-10,50,30))
        text_surface = self.font.render("B", True, color)
        text_rect = text_surface.get_rect(center = (x+100,y+20))
        self.screen.blit(text_surface, text_rect)
        text_surface = self.font.render(str(score_B), True, color)
        text_rect = text_surface.get_rect(center = (x+100, y+60))
        self.screen.blit(text_surface, text_rect)

        pygame.draw.line(self.screen, color, (x+10,y+40), (x+126,y+40), 3)
        pygame.draw.line(self.screen, color, (x+30+35,y+10), (x+30+35,y+70),3)

    def display_tichus(self,x,y,small_tichus,great_tichus):
        for i in range(0,5):
            pygame.draw.line(self.screen, (0,0,0),(x+i*30,y+20),(x+i*30,y+60),3)
            if(i<4):
                pygame.draw.rect(self.screen,self.backgroundcolor,(x+i*30+5,y+5+18,20,17))
                pygame.draw.rect(self.screen,self.backgroundcolor,(x+i*30+5,y+5+38,20,17))

                text_surface = self.font.render(str(i), True, (0,0,0))
                text_rect = text_surface.get_rect(center = (x+i*30+15,y+5))
                self.screen.blit(text_surface, text_rect)
                if(small_tichus[i]):
                    pygame.draw.circle(self.screen,(0,0,0),(x+i*30+15,y+5+24),5)
                if(great_tichus[i]):
                    pygame.draw.circle(self.screen,(0,0,0),(x+i*30+15,y+5+44),5)


        pygame.draw.line(self.screen, (0,0,0), (x,y+20),(x+4*30,y+20),3)
        pygame.draw.line(self.screen, (0,0,0), (x,y+40),(x+4*30,y+40),3)
        pygame.draw.line(self.screen, (0,0,0), (x,y+60),(x+4*30,y+60),3)
        text_surface = self.font.render("ST", True, (0,0,0))
        text_rect = text_surface.get_rect(center = (x-30+5,y+30))
        self.screen.blit(text_surface, text_rect)
        text_surface = self.font.render("GT", True, (0,0,0))
        text_rect = text_surface.get_rect(center = (x-30+5,y+50))
        self.screen.blit(text_surface, text_rect)




    def display_num_of_remaining_cards(self,num,x,y):

        pygame.draw.rect(self.screen, self.backgroundcolor, (x-40,y+40, 80, 40))
        text_surface = self.font.render(str(num)+" cards", True, (0,0,0))
        text_rect = text_surface.get_rect(center = (x,y+40+10))
        self.screen.blit(text_surface, text_rect)
        text_surface = self.font.render("left", True, (0,0,0))
        text_rect = text_surface.get_rect(center = (x,y+40+10+15))
        self.screen.blit(text_surface, text_rect)
    
    def display_nums_of_remaining_cards(self,nums):

        self.display_num_of_remaining_cards(nums[0], self.player_positions[0][0], self.player_positions[0][1])
        self.display_num_of_remaining_cards(nums[1], self.player_positions[1][0], self.player_positions[1][1])
        self.display_num_of_remaining_cards(nums[2], self.player_positions[2][0],self.player_positions[2][1])
        self.display_num_of_remaining_cards(nums[3], self.player_positions[3][0],self.player_positions[3][1])

    def display_players(self):
            self.display_player(self.player_positions[0][0],self.player_positions[0][1],"Bot0", "A")
            self.display_player(self.player_positions[1][0],self.player_positions[1][1],"Bot1", "B")
            self.display_player(self.player_positions[2][0],self.player_positions[2][1],"Bot2", "A")
            self.display_player(self.player_positions[3][0],self.player_positions[3][1],"Bot3", "B")
           
    def display_text(self,text):
        
        pygame.draw.rect(self.screen, self.backgroundcolor, (100, self.HEIGHT/2-80,610,120))
        text_surface = self.font_big.render(text, True, (0,0,0))
        text_rect = text_surface.get_rect(center = (self.WIDTH/2,-40+self.HEIGHT/2-text_surface.get_size()[1]/2))
        self.screen.blit(text_surface, text_rect)
      
    def display_who_is_the_current_player(self,id):
      
        team = "A"
        if(id%2==1):
            team = "B"
        self.display_players()
        self.display_player(self.player_positions[id][0],self.player_positions[id][1],"Bot"+str(id),team,(100,255,100))
        



"""if __name__ == "__main__":
        cards = [(1,1),(11,3),(2,0),(3,0),(0,4),(2,4),(11,3),(2,0),(3,0),(12,1),(1,2),(11,3),(2,0),(3,0)]
        s = Screen()
        finished_round = False
        while(not finished_round):

            s.display_players()

            s.display_cards(cards)

            s.display_scores(score_A=0,score_B=0,x=30,y=30)

            s.display_tichus(630,40,(1,0,0,1),(0,1,0,0))

            s.display_nums_of_remaining_cards(4,5,2,4)
       
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished_round = True"""


        
