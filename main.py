import pygame
import random
import math
import os
import json
import array
import hashlib
import datetime

# 初始化Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
PURPLE = (200, 50, 255)
ORANGE = (255, 150, 50)
CYAN = (50, 255, 255)
PINK = (255, 100, 200)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN, PINK]

# 用户数据路径
USER_DATA_PATH = "C:/PlayKey/User"

class UserManager:
    """用户管理类"""
    def __init__(self):
        self.current_user = None
        self.users = {}
        self.ensure_user_directory()
        self.load_users()
    
    def ensure_user_directory(self):
        """确保用户目录存在"""
        if not os.path.exists(USER_DATA_PATH):
            os.makedirs(USER_DATA_PATH)
            print(f"创建用户目录: {USER_DATA_PATH}")
    
    def load_users(self):
        """加载所有用户"""
        self.users = {}
        if os.path.exists(USER_DATA_PATH):
            for filename in os.listdir(USER_DATA_PATH):
                if filename.endswith('.json'):
                    filepath = os.path.join(USER_DATA_PATH, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            user_data = json.load(f)
                            self.users[user_data['username']] = user_data
                    except:
                        print(f"无法加载用户文件: {filename}")
    
    def hash_password(self, password):
        """密码加密"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password):
        """注册新用户"""
        if username in self.users:
            return False, "用户名已存在"
        
        if len(username) < 3 or len(username) > 20:
            return False, "用户名长度必须在3-20个字符之间"
        
        if len(password) < 6:
            return False, "密码长度至少6个字符"
        
        # 创建用户数据
        user_data = {
            'username': username,
            'password': self.hash_password(password),
            'register_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_login': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_score': 0,
            'highest_level': 0,
            'games_played': 0,
            'history': []
        }
        
        # 保存用户数据
        filepath = os.path.join(USER_DATA_PATH, f"{username}.json")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=4)
            self.users[username] = user_data
            return True, "注册成功"
        except:
            return False, "保存用户数据失败"
    
    def login_user(self, username, password):
        """用户登录"""
        if username not in self.users:
            return False, "用户名不存在"
        
        user_data = self.users[username]
        if user_data['password'] != self.hash_password(password):
            return False, "密码错误"
        
        # 更新登录时间
        user_data['last_login'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_user_data(username)
        
        self.current_user = user_data
        return True, "登录成功"
    
    def save_user_data(self, username):
        """保存用户数据"""
        if username in self.users:
            filepath = os.path.join(USER_DATA_PATH, f"{username}.json")
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.users[username], f, ensure_ascii=False, indent=4)
            except:
                print(f"保存用户数据失败: {username}")
    
    def update_game_record(self, score, level):
        """更新游戏记录"""
        if self.current_user:
            self.current_user['total_score'] += score
            self.current_user['highest_level'] = max(self.current_user['highest_level'], level)
            self.current_user['games_played'] += 1
            
            # 添加游戏历史
            game_record = {
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'score': score,
                'level': level
            }
            self.current_user['history'].append(game_record)
            
            # 只保留最近10条记录
            if len(self.current_user['history']) > 10:
                self.current_user['history'] = self.current_user['history'][-10:]
            
            self.save_user_data(self.current_user['username'])

class SoundGenerator:
    """自建音效生成器"""
    def __init__(self):
        self.sample_rate = 22050
        
    def generate_beep(self, frequency, duration, volume=0.3):
        """生成简单的蜂鸣声"""
        samples = int(self.sample_rate * duration)
        sound_array = array.array('h', [0]) * (samples * 2)
        
        for i in range(samples):
            t = i / self.sample_rate
            value = int(volume * 32767 * math.sin(2 * math.pi * frequency * t))
            fade = 1.0 - (i / samples)
            value = int(value * fade)
            value = max(-32767, min(32767, value))
            
            sound_array[i * 2] = value
            sound_array[i * 2 + 1] = value
        
        return pygame.sndarray.make_sound(sound_array)
    
    def generate_collect_sound(self):
        """收集正确数字的音效"""
        duration = 0.2
        samples = int(self.sample_rate * duration)
        sound_array = array.array('h', [0]) * (samples * 2)
        
        for i in range(samples):
            t = i / self.sample_rate
            freq = 440 + (440 * t / duration)
            value = int(0.3 * 32767 * math.sin(2 * math.pi * freq * t))
            fade = 1.0 - (i / samples)
            value = int(value * fade)
            value = max(-32767, min(32767, value))
            
            sound_array[i * 2] = value
            sound_array[i * 2 + 1] = value
        
        return pygame.sndarray.make_sound(sound_array)
    
    def generate_level_up_sound(self):
        """升级音效"""
        duration = 0.3
        samples = int(self.sample_rate * duration)
        sound_array = array.array('h', [0]) * (samples * 2)
        
        freqs = [523.25, 659.25, 783.99]
        
        for i in range(samples):
            t = i / self.sample_rate
            value = 0
            for freq in freqs:
                value += int(0.15 * 32767 * math.sin(2 * math.pi * freq * t))
            fade = 1.0 - (i / samples)
            value = int(value * fade / len(freqs))
            value = max(-32767, min(32767, value))
            
            sound_array[i * 2] = value
            sound_array[i * 2 + 1] = value
        
        return pygame.sndarray.make_sound(sound_array)
    
    def generate_place_sound(self):
        """放置球的音效"""
        duration = 0.1
        samples = int(self.sample_rate * duration)
        sound_array = array.array('h', [0]) * (samples * 2)
        
        for i in range(samples):
            t = i / self.sample_rate
            value = int(0.2 * 32767 * math.sin(2 * math.pi * 1000 * t) * math.exp(-t * 20))
            value = max(-32767, min(32767, value))
            
            sound_array[i * 2] = value
            sound_array[i * 2 + 1] = value
        
        return pygame.sndarray.make_sound(sound_array)
    
    def generate_error_sound(self):
        """错误音效"""
        duration = 0.2
        samples = int(self.sample_rate * duration)
        sound_array = array.array('h', [0]) * (samples * 2)
        
        for i in range(samples):
            t = i / self.sample_rate
            freq = 440 - (330 * t / duration)
            value = int(0.25 * 32767 * math.sin(2 * math.pi * freq * t) * math.exp(-t * 10))
            value = max(-32767, min(32767, value))
            
            sound_array[i * 2] = value
            sound_array[i * 2 + 1] = value
        
        return pygame.sndarray.make_sound(sound_array)

class FontManager:
    """字体管理器"""
    def __init__(self):
        self.fonts = {}
        self.load_fonts()
    
    def load_fonts(self):
        """加载字体"""
        yahei_paths = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/msyh.ttf",
            "msyh.ttc",
            "msyh.ttf",
        ]
        
        self.yahei_font = None
        for path in yahei_paths:
            try:
                if os.path.exists(path):
                    test_font = pygame.font.Font(path, 12)
                    self.yahei_font = path
                    break
            except:
                continue
    
    def get_font(self, size, bold=False):
        """获取指定大小的字体"""
        cache_key = f"{size}_{bold}"
        
        if cache_key in self.fonts:
            return self.fonts[cache_key]
        
        try:
            if self.yahei_font:
                font = pygame.font.Font(self.yahei_font, size)
                if bold:
                    font.set_bold(True)
            else:
                font = pygame.font.Font(None, size)
                if bold:
                    font.set_bold(True)
        except:
            font = pygame.font.Font(None, size)
            if bold:
                font.set_bold(True)
        
        self.fonts[cache_key] = font
        return font

class Ball:
    def __init__(self, x, y, radius, color, speed_x=0, speed_y=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.selected = False
        
    def move(self):
        if hasattr(self, 'speed_x'):
            self.x += self.speed_x
            self.y += self.speed_y
            
            if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
                self.speed_x *= -1
            if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
                self.speed_y *= -1
                
    def draw(self, screen):
        if self.selected:
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius + 3, 3)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
    def collides_with(self, other_ball):
        distance = math.sqrt((self.x - other_ball.x)**2 + (self.y - other_ball.y)**2)
        return distance <= self.radius + other_ball.radius
    
    def is_point_inside(self, point_x, point_y):
        distance = math.sqrt((self.x - point_x)**2 + (self.y - point_y)**2)
        return distance <= self.radius

class NumberBall(Ball):
    def __init__(self, x, y, number, speed_x=0, speed_y=0, is_placed=False):
        super().__init__(x, y, 20, COLORS[number % len(COLORS)], speed_x, speed_y)
        self.number = number
        self.is_placed = is_placed
        if not is_placed:
            self.speed_x = speed_x if speed_x != 0 else random.uniform(-2, 2)
            self.speed_y = speed_y if speed_y != 0 else random.uniform(-2, 2)
        
    def draw(self, screen, font_manager):
        super().draw(screen)
        
        font = font_manager.get_font(20, bold=True)
        
        text = font.render(str(self.number), True, WHITE)
        shadow_text = font.render(str(self.number), True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(self.x + 2, self.y + 2))
        screen.blit(shadow_text, shadow_rect)
        
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
        
        if self.is_placed:
            pygame.draw.circle(screen, GOLD, (int(self.x), int(self.y)), self.radius + 2, 2)

class PlayerBall(Ball):
    def __init__(self, x, y):
        super().__init__(x, y, 25, WHITE)
        self.level = 1
        self.score = 0
        self.placed_balls = []
        self.mouse_control = True
        self.target_x = x
        self.target_y = y
        self.speed = 8
        
    def update_with_mouse(self, mouse_x, mouse_y):
        if self.mouse_control:
            self.target_x = max(self.radius, min(SCREEN_WIDTH - self.radius, mouse_x))
            self.target_y = max(self.radius, min(SCREEN_HEIGHT - self.radius, mouse_y))
            
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > self.speed:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
            else:
                self.x = self.target_x
                self.y = self.target_y
        
    def draw(self, screen, font_manager):
        if self.level < 256:
            glow_radius = self.radius + 5 + int(self.level / 10)
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            
            for i in range(3):
                alpha = 100 - i * 30
                if alpha > 0:
                    color = COLORS[(self.level // 3) % len(COLORS)]
                    pygame.draw.circle(glow_surface, color, 
                                     (glow_radius, glow_radius), glow_radius - i*3)
            
            screen.blit(glow_surface, (int(self.x - glow_radius), int(self.y - glow_radius)))
        
        if self.mouse_control:
            pygame.draw.line(screen, GRAY, (int(self.x), int(self.y)), 
                           (int(self.target_x), int(self.target_y)), 2)
            pygame.draw.circle(screen, GRAY, (int(self.target_x), int(self.target_y)), 5)
            pygame.draw.circle(screen, WHITE, (int(self.target_x), int(self.target_y)), 3)
            
        super().draw(screen)
        
        font = font_manager.get_font(24, bold=True)
        
        level_shadow = font.render(str(self.level), True, BLACK)
        level_text = font.render(str(self.level), True, WHITE)
        
        shadow_rect = level_shadow.get_rect(center=(self.x + 2, self.y + 2))
        text_rect = level_text.get_rect(center=(self.x, self.y))
        
        screen.blit(level_shadow, shadow_rect)
        screen.blit(level_text, text_rect)

class LoginScreen:
    """登录界面"""
    def __init__(self, screen, font_manager):
        self.screen = screen
        self.font_manager = font_manager
        self.user_manager = UserManager()
        self.input_boxes = []
        self.active_box = 0
        self.message = ""
        self.message_color = RED
        self.setup_input_boxes()
    
    def setup_input_boxes(self):
        """设置输入框"""
        center_x = SCREEN_WIDTH // 2
        self.input_boxes = [
            {
                'rect': pygame.Rect(center_x - 150, 250, 300, 40),
                'text': '',
                'label': '用户名:',
                'placeholder': '输入用户名',
                'password': False
            },
            {
                'rect': pygame.Rect(center_x - 150, 320, 300, 40),
                'text': '',
                'label': '密码:',
                'placeholder': '输入密码',
                'password': True
            }
        ]
    
    def draw(self):
        """绘制登录界面"""
        self.screen.fill(BLACK)
        
        # 绘制标题
        title_font = self.font_manager.get_font(48, bold=True)
        title = title_font.render("PlayKey", True, GOLD)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle_font = self.font_manager.get_font(24)
        subtitle = subtitle_font.render("请登录或注册", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 绘制输入框
        for i, box in enumerate(self.input_boxes):
            # 绘制标签
            label_font = self.font_manager.get_font(20)
            label = label_font.render(box['label'], True, WHITE)
            self.screen.blit(label, (box['rect'].x - 70, box['rect'].y + 10))
            
            # 绘制输入框背景
            pygame.draw.rect(self.screen, DARK_GRAY, box['rect'])
            pygame.draw.rect(self.screen, CYAN if i == self.active_box else GRAY, box['rect'], 2)
            
            # 绘制文本
            if box['text']:
                display_text = '*' * len(box['text']) if box['password'] else box['text']
                text_surface = self.font_manager.get_font(20).render(display_text, True, WHITE)
                self.screen.blit(text_surface, (box['rect'].x + 10, box['rect'].y + 10))
            else:
                placeholder = self.font_manager.get_font(20).render(box['placeholder'], True, GRAY)
                self.screen.blit(placeholder, (box['rect'].x + 10, box['rect'].y + 10))
        
        # 绘制按钮
        button_y = 400
        login_btn = pygame.Rect(SCREEN_WIDTH//2 - 160, button_y, 150, 40)
        register_btn = pygame.Rect(SCREEN_WIDTH//2 + 10, button_y, 150, 40)
        
        pygame.draw.rect(self.screen, GREEN, login_btn)
        pygame.draw.rect(self.screen, BLUE, register_btn)
        
        login_text = self.font_manager.get_font(20, bold=True).render("登录", True, BLACK)
        register_text = self.font_manager.get_font(20, bold=True).render("注册", True, BLACK)
        
        login_text_rect = login_text.get_rect(center=login_btn.center)
        register_text_rect = register_text.get_rect(center=register_btn.center)
        
        self.screen.blit(login_text, login_text_rect)
        self.screen.blit(register_text, register_text_rect)
        
        # 绘制消息
        if self.message:
            msg_font = self.font_manager.get_font(18)
            msg_text = msg_font.render(self.message, True, self.message_color)
            msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH//2, 460))
            self.screen.blit(msg_text, msg_rect)
        
        pygame.display.flip()
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # 检查输入框点击
                for i, box in enumerate(self.input_boxes):
                    if box['rect'].collidepoint(mouse_pos):
                        self.active_box = i
                
                # 检查按钮点击
                login_btn = pygame.Rect(SCREEN_WIDTH//2 - 160, 400, 150, 40)
                register_btn = pygame.Rect(SCREEN_WIDTH//2 + 10, 400, 150, 40)
                
                if login_btn.collidepoint(mouse_pos):
                    return self.handle_login()
                elif register_btn.collidepoint(mouse_pos):
                    return self.handle_register()
            
            elif event.type == pygame.KEYDOWN:
                if self.active_box < len(self.input_boxes):
                    box = self.input_boxes[self.active_box]
                    
                    if event.key == pygame.K_RETURN:
                        return self.handle_login()
                    elif event.key == pygame.K_TAB:
                        self.active_box = (self.active_box + 1) % len(self.input_boxes)
                    elif event.key == pygame.K_BACKSPACE:
                        box['text'] = box['text'][:-1]
                    else:
                        if len(box['text']) < 20 and event.unicode.isprintable():
                            box['text'] += event.unicode
        
        return None
    
    def handle_login(self):
        """处理登录"""
        username = self.input_boxes[0]['text']
        password = self.input_boxes[1]['text']
        
        if not username or not password:
            self.message = "请输入用户名和密码"
            self.message_color = RED
            return None
        
        success, msg = self.user_manager.login_user(username, password)
        if success:
            return 'game'
        else:
            self.message = msg
            self.message_color = RED
            return None
    
    def handle_register(self):
        """处理注册"""
        username = self.input_boxes[0]['text']
        password = self.input_boxes[1]['text']
        
        if not username or not password:
            self.message = "请输入用户名和密码"
            self.message_color = RED
            return None
        
        success, msg = self.user_manager.register_user(username, password)
        if success:
            self.message = msg
            self.message_color = GREEN
            # 清空输入框
            self.input_boxes[0]['text'] = ''
            self.input_boxes[1]['text'] = ''
        else:
            self.message = msg
            self.message_color = RED
        
        return None

class Game:
    def __init__(self, user_manager):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PlayKey - 数字球收集游戏")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = True
        self.user_manager = user_manager
        
        # 初始化字体管理器
        self.font_manager = FontManager()
        
        # 初始化音效
        self.sound_gen = SoundGenerator()
        self.collect_sound = self.sound_gen.generate_collect_sound()
        self.level_up_sound = self.sound_gen.generate_level_up_sound()
        self.place_sound = self.sound_gen.generate_place_sound()
        self.error_sound = self.sound_gen.generate_error_sound()
        
        # 创建玩家球
        self.player = PlayerBall(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # 创建数字球
        self.number_balls = []
        self.spawn_balls(10)
        
        # 游戏时间
        self.start_time = pygame.time.get_ticks()
        self.game_duration = 60000
        
        # 放置球相关
        self.place_mode = False
        self.placed_count = 0
        self.max_place_balls = 10
        self.selected_number = 1
        
        # 鼠标拖动相关
        self.dragging = False
        self.dragged_ball = None
    
    def spawn_balls(self, count):
        """生成自动移动的数字球"""
        for _ in range(count):
            attempts = 0
            while attempts < 100:
                x = random.randint(40, SCREEN_WIDTH - 40)
                y = random.randint(40, SCREEN_HEIGHT - 40)
                
                distance_to_player = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
                if distance_to_player > 50:
                    overlap = False
                    for ball in self.number_balls:
                        distance = math.sqrt((x - ball.x)**2 + (y - ball.y)**2)
                        if distance < 50:
                            overlap = True
                            break
                    
                    if not overlap:
                        break
                attempts += 1
            
            number = random.randint(1, 256)
            self.number_balls.append(NumberBall(x, y, number))
    
    def place_ball(self, x, y):
        """放置数字球"""
        if self.placed_count >= self.max_place_balls:
            self.error_sound.play()
            return False
        
        for ball in self.number_balls:
            distance = math.sqrt((x - ball.x)**2 + (y - ball.y)**2)
            if distance < 50:
                self.error_sound.play()
                return False
        
        distance_to_player = math.sqrt((x - self.player.x)**2 + (y - self.player.y)**2)
        if distance_to_player < 50:
            self.error_sound.play()
            return False
        
        new_ball = NumberBall(x, y, self.selected_number, is_placed=True)
        self.number_balls.append(new_ball)
        self.player.placed_balls.append(new_ball)
        self.placed_count += 1
        
        self.place_sound.play()
        return True
    
    def calculate_target_level(self):
        """计算目标等级"""
        segment = (self.player.level - 1) // 3
        base = segment * 3 + 1
        return base + random.randint(0, 2)
    
    def handle_collisions(self):
        """处理碰撞检测"""
        target_level = self.calculate_target_level()
        balls_to_remove = []
        
        for ball in self.number_balls[:]:
            if self.player.collides_with(ball):
                if ball.number == target_level:
                    self.player.score += ball.number
                    balls_to_remove.append(ball)
                    self.collect_sound.play()
                    
                    self.player.level += 1
                    
                    if ball in self.player.placed_balls:
                        self.player.placed_balls.remove(ball)
                        self.placed_count -= 1
                    
                    if self.player.level % 10 == 0:
                        self.level_up_sound.play()
                    
                    if self.player.level >= 256:
                        self.game_active = False
                else:
                    self.player.score -= ball.number // 2
                    self.error_sound.play()
        
        for ball in balls_to_remove:
            self.number_balls.remove(ball)
        
        auto_balls = [b for b in self.number_balls if not b.is_placed]
        if len(auto_balls) < 8:
            self.spawn_balls(4)
    
    def draw_text_with_outline(self, text, x, y, color, size=24, bold=False, center=False):
        """绘制带描边的文字"""
        font = self.font_manager.get_font(size, bold)
        
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, BLACK)
        
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
            outline_rect = outline_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
            outline_rect = outline_surface.get_rect(topleft=(x, y))
        
        offsets = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        for dx, dy in offsets:
            self.screen.blit(outline_surface, (outline_rect.x + dx, outline_rect.y + dy))
        
        self.screen.blit(text_surface, text_rect)
        
        return text_rect
    
    def draw_ui(self):
        """绘制UI界面"""
        target = self.calculate_target_level()
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        remaining_time = max(0, 60 - elapsed_time)
        
        # 绘制半透明背景面板
        panel_surface = pygame.Surface((300, 240), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 180))
        self.screen.blit(panel_surface, (10, 10))
        
        # 绘制用户信息
        if self.user_manager.current_user:
            self.draw_text_with_outline(f"用户: {self.user_manager.current_user['username']}", 
                                       20, 20, CYAN, 18)
        
        # 绘制游戏信息
        self.draw_text_with_outline(f"得分: {self.player.score}", 20, 50, WHITE, 24)
        self.draw_text_with_outline(f"等级: LV{self.player.level}/256", 20, 80, CYAN, 24)
        self.draw_text_with_outline(f"目标: {target}", 20, 110, GREEN, 28, bold=True)
        self.draw_text_with_outline(f"时间: {remaining_time}s", 20, 140, YELLOW, 24)
        self.draw_text_with_outline(f"放置球: {self.placed_count}/{self.max_place_balls}", 
                                   20, 170, PINK, 20)
        
        # 绘制最高纪录
        if self.user_manager.current_user:
            self.draw_text_with_outline(f"最高等级: LV{self.user_manager.current_user['highest_level']}", 
                                       20, 200, GOLD, 18)
        
        # 绘制控制面板
        control_surface = pygame.Surface((320, 160), pygame.SRCALPHA)
        control_surface.fill((0, 0, 0, 180))
        self.screen.blit(control_surface, (10, SCREEN_HEIGHT - 170))
        
        controls = [
            ("鼠标移动", "控制玩家球"),
            ("空格键", f"{'关闭' if self.place_mode else '开启'}放置模式"),
            ("1-9数字键", f"选择数字 [{self.selected_number}]"),
            ("点击拖动", "移动放置球"),
        ]
        
        y_offset = SCREEN_HEIGHT - 160
        for i, (action, desc) in enumerate(controls):
            if i == 1 and self.place_mode:
                color = GREEN
            else:
                color = WHITE
            self.draw_text_with_outline(f"{action}:", 20, y_offset + i*30, color, 18)
            self.draw_text_with_outline(desc, 130, y_offset + i*30, LIGHT_GRAY, 18)
        
        if self.place_mode:
            mode_text = f"放置模式 ON - 数字: {self.selected_number}"
            self.draw_text_with_outline(mode_text, SCREEN_WIDTH//2, 50, GREEN, 28, bold=True, center=True)
    
    def handle_input(self):
        """处理玩家输入"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        self.player.update_with_mouse(mouse_x, mouse_y)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.place_mode = not self.place_mode
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    self.selected_number = event.key - pygame.K_0
                elif event.key == pygame.K_0:
                    self.selected_number = 10
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.place_mode:
                        self.place_ball(mouse_x, mouse_y)
                    else:
                        for ball in self.number_balls:
                            if ball.is_placed and ball.is_point_inside(mouse_x, mouse_y):
                                self.dragging = True
                                self.dragged_ball = ball
                                ball.selected = True
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging:
                    self.dragging = False
                    if self.dragged_ball:
                        self.dragged_ball.selected = False
                        self.dragged_ball = None
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging and self.dragged_ball:
                    new_x = max(self.dragged_ball.radius, min(SCREEN_WIDTH - self.dragged_ball.radius, mouse_x))
                    new_y = max(self.dragged_ball.radius, min(SCREEN_HEIGHT - self.dragged_ball.radius, mouse_y))
                    
                    can_move = True
                    for ball in self.number_balls:
                        if ball != self.dragged_ball:
                            distance = math.sqrt((new_x - ball.x)**2 + (new_y - ball.y)**2)
                            if distance < 50:
                                can_move = False
                                break
                    
                    distance_to_player = math.sqrt((new_x - self.player.x)**2 + (new_y - self.player.y)**2)
                    if distance_to_player < 50:
                        can_move = False
                    
                    if can_move:
                        self.dragged_ball.x = new_x
                        self.dragged_ball.y = new_y
    
    def show_game_over(self):
        """显示游戏结束界面"""
        # 更新用户游戏记录
        if self.user_manager.current_user:
            self.user_manager.update_game_record(self.player.score, self.player.level)
        
        # 创建半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        if self.player.level >= 256:
            title = "恭喜！达到最高等级256！"
            title_color = GOLD
        else:
            title = "游戏结束"
            title_color = RED
        
        self.draw_text_with_outline(title, SCREEN_WIDTH//2, 200, title_color, 48, bold=True, center=True)
        self.draw_text_with_outline(f"最终得分: {self.player.score}", SCREEN_WIDTH//2, 280, WHITE, 36, center=True)
        self.draw_text_with_outline(f"最终等级: LV{self.player.level}", SCREEN_WIDTH//2, 330, CYAN, 36, center=True)
        
        if self.user_manager.current_user:
            self.draw_text_with_outline(f"历史最高: LV{self.user_manager.current_user['highest_level']}", 
                                      SCREEN_WIDTH//2, 380, GOLD, 30, center=True)
        
        self.draw_text_with_outline("按空格键重新开始", SCREEN_WIDTH//2, 440, GREEN, 30, center=True)
        self.draw_text_with_outline("按ESC退出", SCREEN_WIDTH//2, 490, RED, 30, center=True)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False
    
    def reset_game(self):
        """重置游戏"""
        self.player = PlayerBall(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.number_balls = []
        self.spawn_balls(10)
        self.start_time = pygame.time.get_ticks()
        self.game_active = True
        self.place_mode = False
        self.placed_count = 0
        self.selected_number = 1
        self.dragging = False
        self.dragged_ball = None
    
    def run(self):
        """游戏主循环"""
        while self.running:
            if self.game_active:
                self.handle_input()
                
                for ball in self.number_balls:
                    if ball != self.dragged_ball:
                        ball.move()
                
                self.handle_collisions()
                
                elapsed_time = pygame.time.get_ticks() - self.start_time
                if elapsed_time >= self.game_duration or self.player.level >= 256:
                    self.game_active = False
                
                self.screen.fill(BLACK)
                
                # 绘制网格背景
                for i in range(0, SCREEN_WIDTH, 50):
                    pygame.draw.line(self.screen, DARK_GRAY, (i, 0), (i, SCREEN_HEIGHT), 1)
                for i in range(0, SCREEN_HEIGHT, 50):
                    pygame.draw.line(self.screen, DARK_GRAY, (0, i), (SCREEN_WIDTH, i), 1)
                
                for ball in self.number_balls:
                    ball.draw(self.screen, self.font_manager)
                
                self.player.draw(self.screen, self.font_manager)
                self.draw_ui()
            else:
                self.show_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

def main():
    """主函数"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PlayKey - 登录")
    
    font_manager = FontManager()
    login_screen = LoginScreen(screen, font_manager)
    
    running = True
    while running:
        result = login_screen.handle_events()
        
        if result == 'quit':
            running = False
        elif result == 'game':
            # 进入游戏
            game = Game(login_screen.user_manager)
            game.run()
            # 游戏结束后返回登录界面
            login_screen = LoginScreen(screen, font_manager)
        
        login_screen.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()