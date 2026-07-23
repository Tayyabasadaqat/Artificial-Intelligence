
import pygame,random,sys,math
WIDTH=700;HEIGHT=700;CELL=20;ROWS=WIDTH//CELL
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT));pygame.display.set_caption("Modern Snake")
clock=pygame.time.Clock()
sf=pygame.font.SysFont("arial",24,True);gf=pygame.font.SysFont("arial",60,True)
WHITE=(255,255,255);RED=(240,70,70);GREEN=(70,220,100);GOLD=(255,215,0)
class Food:
    def spawn(self,snake):
        while True:
            self.pos=(random.randrange(ROWS),random.randrange(ROWS))
            if self.pos not in snake: break
        r=random.randint(1,100)
        if r<=60:self.points,self.growth,self.color=10,1,RED
        elif r<=90:self.points,self.growth,self.color=20,2,GREEN
        else:self.points,self.growth,self.color=50,5,GOLD
    def draw(self):
        x,y=self.pos[0]*CELL,self.pos[1]*CELL
        rad=CELL//2-2+int(abs(math.sin(pygame.time.get_ticks()/200))*2)
        pygame.draw.circle(screen,self.color,(x+CELL//2,y+CELL//2),rad)
class Snake:
    def __init__(self):self.reset()
    def reset(self):
        self.body=[(10,10)];self.dir=(1,0);self.grow=0
    def change(self,d):
        if d!=(-self.dir[0],-self.dir[1]):self.dir=d
    def move(self):
        hx,hy=self.body[0];dx,dy=self.dir
        self.body.insert(0,(hx+dx,hy+dy))
        if self.grow>0:self.grow-=1
        else:self.body.pop()
    def dead(self):
        x,y=self.body[0]
        return x<0 or y<0 or x>=ROWS or y>=ROWS or self.body[0] in self.body[1:]
    def draw(self):
        for i,(gx,gy) in enumerate(self.body):
            x,y=gx*CELL,gy*CELL
            c=(50,230,120) if i==0 else (20,170,70)
            pygame.draw.rect(screen,c,(x+1,y+1,CELL-2,CELL-2),border_radius=7)
            if i==0:
                pygame.draw.circle(screen,WHITE,(x+6,y+6),2)
                pygame.draw.circle(screen,WHITE,(x+14,y+6),2)
snake=Snake();food=Food();food.spawn(snake.body)
score=0;over=False
while True:
    clock.tick(10+score//50)
    for e in pygame.event.get():
        if e.type==pygame.QUIT:pygame.quit();sys.exit()
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_UP:snake.change((0,-1))
            if e.key==pygame.K_DOWN:snake.change((0,1))
            if e.key==pygame.K_LEFT:snake.change((-1,0))
            if e.key==pygame.K_RIGHT:snake.change((1,0))
            if e.key==pygame.K_r and over:
                snake.reset();food.spawn(snake.body);score=0;over=False
            if e.key==pygame.K_ESCAPE:pygame.quit();sys.exit()
    if not over:
        snake.move()
        if snake.dead(): over=True
        elif snake.body[0]==food.pos:
            score+=food.points;snake.grow+=food.growth;food.spawn(snake.body)
    for y in range(HEIGHT):
        pygame.draw.line(screen,(20,20+y//8,40),(0,y),(WIDTH,y))
    for x in range(0,WIDTH,CELL): pygame.draw.line(screen,(40,40,55),(x,0),(x,HEIGHT))
    for y in range(0,HEIGHT,CELL): pygame.draw.line(screen,(40,40,55),(0,y),(WIDTH,y))
    pygame.draw.rect(screen,(30,30,45),(0,0,WIDTH,40))
    screen.blit(sf.render(f"Score: {score}",True,WHITE),(10,8))
    food.draw();snake.draw()
    if over:
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA);ov.fill((0,0,0,170));screen.blit(ov,(0,0))
        screen.blit(gf.render("GAME OVER",True,RED),gf.render("GAME OVER",True,RED).get_rect(center=(WIDTH//2,250)))
        for txt,yy in [(f"Final Score: {score}",340),("Press R to Restart",390),("ESC to Quit",430)]:
            s=sf.render(txt,True,GOLD if "Restart" in txt else WHITE)
            screen.blit(s,s.get_rect(center=(WIDTH//2,yy)))
    pygame.display.flip()
