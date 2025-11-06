#библиотеки
import pygame

def main():
    pygame.init()
    screen=pygame.display.set_mode((640, 480))
    clock=pygame.time.Clock()
    
    radius=15
    x=0
    y=0
    mode='blue'
    points=[]
    
    #новые функций
    tool='pencil'  # 'pencil', 'rectangle', 'circle', 'eraser'
    start_pos=None
    end_pos=None
    drawing_shape=False
    color=(0, 0, 255)  # дефолт синий цвет
    
    # цветовая палитра
    colors={
        'red':(255, 0, 0),
        'green':(0, 255, 0),
        'blue':(0, 0, 255),
        'yellow':(255, 255, 0),
        'magenta':(255, 0, 255),
        'cyan':(0, 255, 255),
        'white':(255, 255, 255),
        'black':(0, 0, 0)
    }
    
    # new function:drawing surface
    canvas=pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))  # bfcground is black
    while True:
        pressed=pygame.key.get_pressed()
        alt_held=pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held=pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                return
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w and ctrl_held:
                    return
                if event.key==pygame.K_F4 and alt_held:
                    return
                if event.key==pygame.K_ESCAPE:
                    return
            
                # новые функ выборка инструментов
                if event.key==pygame.K_p:
                    tool='pencil'
                elif event.key==pygame.K_r and not ctrl_held:  # r for rectangle
                    tool='rectangle'
                elif event.key==pygame.K_c:  # c for circle
                    tool='circle'
                elif event.key==pygame.K_e:  # e for eraser
                    tool ='eraser'
                
                # выборка цветов
                if event.key==pygame.K_1:
                    color =colors['red']
                    mode='red'
                elif event.key==pygame.K_2:
                    color=colors['green']
                    mode='green'
                elif event.key==pygame.K_3:
                    color= colors['blue']
                    mode='blue'
                elif event.key==pygame.K_4:
                    color=colors['yellow']
                elif event.key==pygame.K_5:
                    color=colors['purple']
                elif event.key==pygame.K_6:
                    color =colors['cyan']
                elif event.key==pygame.K_7:
                    color=colors['white']
                elif event.key == pygame.K_8:
                    color=colors['black']
                
                # очищаем 
                if event.key==pygame.K_c and ctrl_held:
                    canvas.fill((0, 0, 0))
            
            # рисование форм
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:  # левая кнопка
                    if tool in ['rectangle', 'circle']:
                        start_pos=event.pos
                        drawing_shape=True
                    elif tool=='pencil':
                        radius=min(200, radius + 1)
                    elif tool =='eraser':
                        radius=min(50, radius + 1)
                elif event.button==3:  #правая кнопка
                    if tool in ['pencil', 'eraser']:
                        radius = max(1, radius-1)
            
            # новое конец рисования
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1 and drawing_shape and tool in ['rectangle', 'circle']:
                    end_pos =event.pos
                    if tool=='rectangle':
                        rect=pygame.Rect(
                            min(start_pos[0], end_pos[0]),
                            min(start_pos[1], end_pos[1]),
                            abs(end_pos[0]-start_pos[0]),
                            abs(end_pos[1]-start_pos[1])
                        )
                        pygame.draw.rect(canvas, color, rect, 2)
                    
                    elif tool=='circle':
                        center_x=(start_pos[0]+end_pos[0])//2
                        center_y=(start_pos[1]+end_pos[1])// 2
                        circle_radius=max(5, abs(end_pos[0]-start_pos[0]) // 2)
                        pygame.draw.circle(canvas, color, (center_x, center_y), circle_radius, 2)
                    
                    drawing_shape=False
                    start_pos=None
                    end_pos =None
            
            if event.type == pygame.MOUSEMOTION:
                if tool=='pencil':
                    position=event.pos
                    points=points +[position]
                    points = points[-256:]
                elif tool=='eraser':
                    erase_pos=event.pos
                    pygame.draw.circle(canvas, (0, 0, 0), erase_pos, radius)
                
        
        # ччто происходит на экране 
        if drawing_shape and start_pos:
            current_pos=pygame.mouse.get_pos()
            if tool=='rectangle':
                rect_preview=pygame.Rect(
                    min(start_pos[0], current_pos[0]),
                    min(start_pos[1], current_pos[1]),
                    abs(current_pos[0]-start_pos[0]),
                    abs(current_pos[1]-start_pos[1])
                )
                pygame.draw.rect(screen, color, rect_preview, 2)
            elif tool=='circle':
                center_x=(start_pos[0]+current_pos[0])//2
                center_y=(start_pos[1] +current_pos[1])//2
                circle_radius = max(5, abs(current_pos[0]-start_pos[0]) //2)
                pygame.draw.circle(screen, color, (center_x, center_y), circle_radius, 2)
        
        
        screen.blit(tool_text, (10, 10))
        screen.blit(color_text, (10, 40))
        screen.blit(radius_text, (10, 70))
        
        for i, text in enumerate(help_text):
            help_surface=pygame.font.Font(None, 24).render(text, True, (200, 200, 200))
            screen.blit(help_surface, (10, 430+i*20))
        
        pygame.display.flip()
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1=max(0, min(255, 2 *index-256))
    c2= max(0, min(255, 2*index))
    
    if color_mode=='blue':
        color= (c1, c1, c2)
    elif color_mode=='red':
        color=(c2, c1, c1)
    elif color_mode=='green':
        color=(c1, c2, c1)
    else:
        if color_mode=='red':
            color=(255, 0, 0)
        elif color_mode=='green':
            color =(0, 255, 0)
        elif color_mode=='blue':
            color=(0, 0, 255)
        else:
            color=(255, 255, 255)  #по дефолту белый цвет
    
    dx=start[0]-end[0]
    dy=start[1]-end[1]
    iterations=max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress=1.0*i/iterations
        aprogress=1-progress
        x=int(aprogress*start[0]+progress* end[0])
        y=int(aprogress*start[1]+progress*end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()