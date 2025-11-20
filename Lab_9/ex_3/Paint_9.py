import pygame
import math

def main():
    pygame.init()
    screen=pygame.display.set_mode((640, 480))
    clock=pygame.time.Clock()
    
    radius=15
    x=0
    y=0
    mode='blue'
    points=[]
    
    tool='pencil'
    start_pos=None
    end_pos=None
    drawing_shape = False
    color=(0, 0, 255)
    
    colors={
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (255, 0, 255),
        'cyan': (0, 255, 255),
        'white': (255, 255, 255),
        'black': (0, 0, 0)
    }
    canvas=pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))
    
    def draw_square(surface, start, end, draw_color, width=2):
        x1, y1=start
        x2, y2=end
        
        side_length=min(abs(x2-x1), abs(y2-y1))
        
        if x2>=x1 and y2>=y1:
            rect =pygame.Rect(x1, y1, side_length, side_length)
        elif x2 < x1 and y2 >= y1:
            rect=pygame.Rect(x1 - side_length, y1, side_length, side_length)
        elif x2 >= x1 and y2 < y1:
            rect = pygame.Rect(x1, y1 - side_length, side_length, side_length)
        else:
            rect = pygame.Rect(x1 - side_length, y1 - side_length, side_length, side_length)
        
        pygame.draw.rect(surface, draw_color, rect, width)
        return rect
    
    def draw_right_triangle(surface, start, end, draw_color, width=2):
        x1, y1 = start
        x2, y2 = end
        
        points=[
            (x1, y1),
            (x2, y2),
            (x1, y2)
        ]
        
        pygame.draw.polygon(surface, draw_color, points, width)
        return points
    
    def draw_equilateral_triangle(surface, start, end, draw_color, width=2):
        x1, y1 = start
        x2, y2 = end
        
        side_length=math.sqrt((x2-x1)**2+(y2-y1)**2)
        height=(math.sqrt(3)/2) * side_length
        
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        dx = x2 - x1
        dy = y2 - y1
        
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx, dy = dx/length, dy/length
            perp_x, perp_y = -dy, dx
            
            apex_x = mid_x + perp_x * height
            apex_y = mid_y + perp_y * height
            
            points = [
                (x1, y1),
                (x2, y2),
                (apex_x, apex_y)
            ]
            
            pygame.draw.polygon(surface, draw_color, points, width)
            return points
        
        return None
    
    def draw_rhombus(surface, start, end, draw_color, width=2):
        x1, y1 = start
        x2, y2 = end
        
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        half_width = abs(x2 - x1) / 2
        half_height = abs(y2 - y1) / 2
        
        points = [
            (center_x, center_y - half_height),
            (center_x + half_width, center_y),
            (center_x, center_y + half_height),
            (center_x - half_width, center_y)
        ]
        
        pygame.draw.polygon(surface, draw_color, points, width)
        return points
    
    while True:
        
        pressed = pygame.key.get_pressed()
        
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
            
                if event.key == pygame.K_p:
                    tool = 'pencil'
                elif event.key == pygame.K_r and not ctrl_held:
                    tool = 'rectangle'
                elif event.key == pygame.K_c:
                    tool = 'circle'
                elif event.key == pygame.K_e:
                    tool = 'eraser'
                elif event.key == pygame.K_s:
                    tool = 'square'
                elif event.key == pygame.K_t:
                    tool = 'right_triangle'
                elif event.key == pygame.K_q:
                    tool = 'equilateral_triangle'
                elif event.key == pygame.K_d:
                    tool = 'rhombus'
                
                if event.key == pygame.K_1:
                    color = colors['red']
                    mode = 'red'
                elif event.key == pygame.K_2:
                    color = colors['green']
                    mode = 'green'
                elif event.key == pygame.K_3:
                    color = colors['blue']
                    mode = 'blue'
                elif event.key == pygame.K_4:
                    color = colors['yellow']
                elif event.key == pygame.K_5:
                    color = colors['purple']
                elif event.key == pygame.K_6:
                    color = colors['cyan']
                elif event.key == pygame.K_7:
                    color = colors['white']
                elif event.key == pygame.K_8:
                    color = colors['black']
                
                if event.key == pygame.K_c and ctrl_held:
                    canvas.fill((0, 0, 0))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if tool in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                        start_pos = event.pos
                        drawing_shape = True
                    elif tool == 'pencil':
                        radius = min(200, radius + 1)
                    elif tool == 'eraser':
                        radius = min(50, radius + 1)
                elif event.button == 3:
                    if tool in ['pencil', 'eraser']:
                        radius = max(1, radius - 1)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing_shape and start_pos:
                    end_pos = event.pos
                    
                    if tool == 'rectangle':
                        rect = pygame.Rect(
                            min(start_pos[0], end_pos[0]),
                            min(start_pos[1], end_pos[1]),
                            abs(end_pos[0] - start_pos[0]),
                            abs(end_pos[1] - start_pos[1])
                        )
                        pygame.draw.rect(canvas, color, rect, 2)
                    
                    elif tool == 'circle':
                        center_x = (start_pos[0] + end_pos[0]) // 2
                        center_y = (start_pos[1] + end_pos[1]) // 2
                        circle_radius = max(5, abs(end_pos[0] - start_pos[0]) // 2)
                        pygame.draw.circle(canvas, color, (center_x, center_y), circle_radius, 2)
                    
                    elif tool == 'square':
                        draw_square(canvas, start_pos, end_pos, color, 2)
                    
                    elif tool == 'right_triangle':
                        draw_right_triangle(canvas, start_pos, end_pos, color, 2)
                    
                    elif tool == 'equilateral_triangle':
                        draw_equilateral_triangle(canvas, start_pos, end_pos, color, 2)
                    
                    elif tool == 'rhombus':
                        draw_rhombus(canvas, start_pos, end_pos, color, 2)
                    
                    drawing_shape = False
                    start_pos = None
                    end_pos = None
            
            if event.type == pygame.MOUSEMOTION:
                if tool == 'pencil':
                    position = event.pos
                    points = points + [position]
                    points = points[-256:]
                elif tool == 'eraser':
                    erase_pos = event.pos
                    pygame.draw.circle(canvas, (0, 0, 0), erase_pos, radius)
                
        screen.blit(canvas, (0, 0))
        
        if drawing_shape and start_pos:
            current_pos = pygame.mouse.get_pos()
            if tool == 'rectangle':
                rect_preview = pygame.Rect(
                    min(start_pos[0], current_pos[0]),
                    min(start_pos[1], current_pos[1]),
                    abs(current_pos[0] - start_pos[0]),
                    abs(current_pos[1] - start_pos[1])
                )
                pygame.draw.rect(screen, color, rect_preview, 2)
            elif tool == 'circle':
                center_x = (start_pos[0] + current_pos[0]) // 2
                center_y = (start_pos[1] + current_pos[1]) // 2
                circle_radius = max(5, abs(current_pos[0] - start_pos[0]) // 2)
                pygame.draw.circle(screen, color, (center_x, center_y), circle_radius, 2)
            elif tool='square':
                draw_square(screen, start_pos, current_pos, color, 2)
            elif tool=='right_triangle':
                draw_right_triangle(screen, start_pos, current_pos, color, 2)
            elif tool=='equilateral_triangle':
                draw_equilateral_triangle(screen, start_pos, current_pos, color, 2)
            elif tool=='rhombus':
                draw_rhombus(screen, start_pos, current_pos, color, 2)
        
        if tool=='pencil':
            i=0
            while i <len(points)-1:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
                i+=1
        
        font = pygame.font.Font(None, 36)
        tool_text=font.render(f"Tool: {tool}", True, (255, 255, 255))
        color_text=font.render(f"Color: {mode if mode in ['red','green','blue'] else 'custom'}", True, (255, 255, 255))
        radius_text=font.render(f"Radius: {radius}", True, (255, 255, 255))
        
        screen.blit(tool_text, (10, 10))
        screen.blit(color_text, (10, 40))
        screen.blit(radius_text, (10, 70))
        
        help_text=[
            "P-Pencil R-Rectangle C-Circle E-Eraser S-Square",
            "T-Right Triangle Q-Equilateral Triangle D-Rhombus",
            "1-Red 2-Green 3-Blue 4-Yellow 5-Purple 6-Cyan",
            "7-White 8-Black Ctrl+C-Clear"
        ]
        
        for i, text in enumerate(help_text):
            help_surface=pygame.font.Font(None, 24).render(text, True, (200, 200, 200))
            screen.blit(help_surface, (10, 430+i*20))
        
        pygame.display.flip()
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1=max(0, min(255, 2*index-256))
    c2=max(0, min(255, 2*index))
    
    if color_mode=='blue':
        color=(c1, c1, c2)
    elif color_mode=='red':
        color=(c2, c1, c1)
    elif color_mode=='green':
        color =(c1, c2, c1)
    else:
        if color_mode== 'red':
            color=(255, 0, 0)
        elif color_mode=='green':
            color=(0, 255, 0)
        elif color_mode=='blue':
            color=(0, 0, 255)
        else:
            color=(255, 255, 255)
    
    dx=start[0]-end[0]
    dy=start[1]-end[1]
    iterations=max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress=1.0*i/iterations
        aprogress=1-progress
        x=int(aprogress*start[0]+progress*end[0])
        y=int(aprogress*start[1]+progress *end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()