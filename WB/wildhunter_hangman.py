import pygame
import requests
import random
import sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
GRAY = (128, 128, 128)
DARK_RED = (100, 20, 20)

class WildHuntHangman:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.background_music = "elkking.mp3"
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Wild Hunt: Wordbound")

        self.wild_hunt_image = pygame.image.load("Wildhunter.png").convert_alpha()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Wild Hunt: Wordbound")
        self.clock = pygame.time.Clock()

        # 폰트 설정
        self.title_font = pygame.font.Font(None, 72)
        self.main_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.feedback_font = pygame.font.Font(None, 40)

        # 게임 상태
        self.game_state = "welcome"  # welcome, playing, game_over, win
        self.current_word = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 7
        self.hint_used = False

        self.feedback_text = ""
        self.feedback_color = WHITE
        self.feedback_timer = 0

        self.shake_timer = 0
        self.shake_intensity = 0

        pygame.mixer.music.load(self.background_music)
        self.wild_hunt_alpha = 0

        print("Let's start!")

    def fetch_random_word(self):
        word_lengths = [7, 7, 7, 6, 8] #Because 7-letter words are more common, they appear multiple times; lengths vary from 6 to 8.
        target_length = random.choice(word_lengths)
        url = f"https://api.datamuse.com/words?sp={'?' * target_length}&max=50"
        response = requests.get(url, timeout=5)
        words = response.json()
        suitable_words = [word['word'].upper() for word in words
                          if word['word'].isalpha() and len(word['word']) == target_length]
        selected = random.choice(suitable_words)
        print(f"bring {len(selected)}: {selected}")
        return selected

    def start_new_game(self):
        self.current_word = self.fetch_random_word()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.game_state = "playing"
        self.hint_used = False
        self.feedback_text = ""
        self.feedback_timer = 0
        self.shake_timer = 0
        self.wild_hunt_alpha = 0
        print(f"new game start! word: {self.current_word}")

    def get_display_word(self):
        return " ".join([letter if letter in self.guessed_letters else "_"
                         for letter in self.current_word])

    def use_hint(self):
        if self.hint_used:
            return False

        unguessed = [letter for letter in self.current_word
                     if letter not in self.guessed_letters]

        if unguessed:
            hint_letter = random.choice(unguessed)
            self.guessed_letters.add(hint_letter)
            self.hint_used = True
            self.show_fb(f"Hint revealed: {hint_letter}", GREEN)

            if all(letter in self.guessed_letters for letter in self.current_word):
                self.game_state = "win"

            return True
        return False

    def show_fb(self, text, color):
        self.feedback_text = text
        self.feedback_color = color
        self.feedback_timer = 120

    def start_shake(self, intensity=10):
        """shake it! shake it!"""
        self.shake_timer = 30
        self.shake_intensity = intensity

    def guess_letter(self, letter):
        letter = letter.upper()

        if letter in self.guessed_letters:
            self.show_fb(f"Already guessed: {letter}", GRAY)
            return False

        if not letter.isalpha() or len(letter) != 1:
            return False

        self.guessed_letters.add(letter)

        if letter in self.current_word:
            count = self.current_word.count(letter)
            if count == 1:
                self.show_fb(f"Good! '{letter}' is in the word!", GREEN)
            else:
                self.show_fb(f"Excellent! '{letter}' appears {count} times!", GREEN)
        else:
            self.wrong_guesses += 1
            self.wild_hunt_alpha = min(255, (self.wrong_guesses / self.max_wrong_guesses) * 255)
            self.show_fb(f"Wrong! '{letter}' is not in the word.", RED)
            self.start_shake(15)

        if self.wrong_guesses >= self.max_wrong_guesses:
            self.game_state = "game_over"
        elif all(letter in self.guessed_letters for letter in self.current_word):
            self.game_state = "win"

        return True

    def get_shake_offset(self):
        if self.shake_timer <= 0:
            return 0, 0

        intensity = self.shake_intensity * (self.shake_timer / 30)
        shake_x = random.randint(-int(intensity), int(intensity))
        shake_y = random.randint(-int(intensity), int(intensity))
        return shake_x, shake_y

    def draw_wild_hunt_silhouette(self, x, y):
        if self.wild_hunt_alpha <= 0:
            return

        temp_surface = pygame.Surface((300, 200), pygame.SRCALPHA)

        pygame.draw.ellipse(temp_surface, (*BLACK, self.wild_hunt_alpha), (50, 120, 120, 60))
        pygame.draw.ellipse(temp_surface, (*BLACK, self.wild_hunt_alpha), (150, 100, 40, 50))
        pygame.draw.ellipse(temp_surface, (*BLACK, self.wild_hunt_alpha), (170, 80, 30, 40))
        for leg_x in [60, 80, 130, 150]:
            pygame.draw.rect(temp_surface, (*BLACK, self.wild_hunt_alpha), (leg_x, 160, 8, 30))

        pygame.draw.ellipse(temp_surface, (*BLACK, self.wild_hunt_alpha), (70, 80, 30, 60))
        pygame.draw.ellipse(temp_surface, (*BLACK, self.wild_hunt_alpha), (75, 60, 20, 25))
        pygame.draw.polygon(temp_surface, (*BLACK, self.wild_hunt_alpha),
                            [(85, 60), (87, 45), (83, 45)])

        pygame.draw.line(temp_surface, (*BLACK, self.wild_hunt_alpha), (85, 90), (110, 70), 5)
        pygame.draw.line(temp_surface, (*BLACK, self.wild_hunt_alpha), (110, 70), (125, 50), 3)

        pygame.draw.polygon(temp_surface, (*BLACK, self.wild_hunt_alpha),
                            [(75, 85), (60, 90), (45, 110), (55, 130), (75, 120)])

        if self.wild_hunt_alpha > 100:
            eye_alpha = min(255, self.wild_hunt_alpha + 50)
            pygame.draw.circle(temp_surface, (*BLUE, eye_alpha), (80, 67), 2)
            pygame.draw.circle(temp_surface, (*BLUE, eye_alpha), (190, 95), 3)  # 말의 눈

        self.screen.blit(temp_surface, (x, y))

    def draw_welcome_screen(self):
        self.screen.fill(BLACK)

        title_text = self.title_font.render("The Wild Hunt: Wordbound", True, BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)

        story_lines = [
            "With the sound of trumpets separating the night sky,",
            "wild hunters were resurrected.",
            "They hunt the souls of the living,",
            "trying to reclaim the forgotten word.",
            "",
            "If you don't get it right, you'll join their procession.",
            "",
            "Press SPACE to start your fate..."
        ]

        y_offset = 250
        for line in story_lines:
            if line:
                text = self.small_font.render(line, True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text, text_rect)
            y_offset += 40

    def draw_game_screen(self):
        shake_x, shake_y = self.get_shake_offset()

        self.screen.fill(BLACK)

        self.draw_wild_hunt_silhouette(400 + shake_x, 150 + shake_y)

        word_display = self.get_display_word()
        word_text = self.main_font.render(word_display, True, WHITE)
        word_rect = word_text.get_rect(center=(SCREEN_WIDTH // 2 + shake_x, 400 + shake_y))
        self.screen.blit(word_text, word_rect)

        length_text = f"Word length: {len(self.current_word)} letters"
        length_surface = self.small_font.render(length_text, True, GRAY)
        self.screen.blit(length_surface, (50 + shake_x, 450 + shake_y))

        guessed_text = f"Guessed: {' '.join(sorted(self.guessed_letters))}"
        guessed_surface = self.small_font.render(guessed_text, True, GRAY)
        self.screen.blit(guessed_surface, (50 + shake_x, 500 + shake_y))

        remaining = self.max_wrong_guesses - self.wrong_guesses
        remaining_text = f"Lives remaining: {remaining}"
        color = RED if remaining <= 2 else WHITE
        remaining_surface = self.small_font.render(remaining_text, True, color)
        self.screen.blit(remaining_surface, (50 + shake_x, 540 + shake_y))

        hint_text = "Hint: USED" if self.hint_used else "Hint: Press H to reveal a letter"
        hint_color = GRAY if self.hint_used else GREEN
        hint_surface = self.small_font.render(hint_text, True, hint_color)
        self.screen.blit(hint_surface, (50 + shake_x, 580 + shake_y))

        hint_text = "Enter a letter and press ENTER"
        hint_surface = self.small_font.render(hint_text, True, BLUE)
        hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH // 2 + shake_x, 650 + shake_y))
        self.screen.blit(hint_surface, hint_rect)

        if self.feedback_timer > 0:
            feedback_surface = self.feedback_font.render(self.feedback_text, True, self.feedback_color)
            feedback_rect = feedback_surface.get_rect(center=(SCREEN_WIDTH // 2 + shake_x, 320 + shake_y))
            self.screen.blit(feedback_surface, feedback_rect)

    def draw_wild_hunt_silhouette(self, x, y):
        image = pygame.transform.scale(self.wild_hunt_image, (300, 300))
        image.set_alpha(self.wild_hunt_alpha)
        self.screen.blit(image, (x, y))

    def draw_end_screen(self):
        self.screen.fill(BLACK)

        if self.game_state == "win":
            title = "The rays of the sun drive out the night"
            subtitle = "& destroy the power of false hood."
            result = "You have banished the Wild Hunt!"
            result2 = f"The word was: {self.current_word}"
            color = BLUE
        else:
            self.wild_hunt_alpha = 255
            self.draw_wild_hunt_silhouette(350, 100)

            title = "Your time is ended."
            subtitle = "Your soul is now taken by the Hunt."
            result = f"The word was: {self.current_word}"
            result2 = "You now march among the riders..."
            color = RED

        title_text = self.main_font.render(title, True, color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(title_text, title_rect)

        subtitle_text = self.small_font.render(subtitle, True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 390))
        self.screen.blit(subtitle_text, subtitle_rect)

        result_text = self.main_font.render(result, True, WHITE)
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
        self.screen.blit(result_text, result_rect)

        result2_text = self.small_font.render(result2, True, GRAY)
        result2_rect = result2_text.get_rect(center=(SCREEN_WIDTH // 2, 490))
        self.screen.blit(result2_text, result2_rect)

        restart_text = "Press SPACE to hunt again..."
        restart_surface = self.small_font.render(restart_text, True, GRAY)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, 550))
        self.screen.blit(restart_surface, restart_rect)

    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1

        if self.shake_timer > 0:
            self.shake_timer -= 1

    def run(self):
        """main game loop"""
        running = True
        input_text = ""

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if self.game_state == "welcome":
                        if event.key == pygame.K_SPACE:
                            self.start_new_game()

                    elif self.game_state == "playing":
                        if event.key == pygame.K_RETURN and input_text:
                            self.guess_letter(input_text)
                            input_text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        elif event.key == pygame.K_h:  # 힌트 사용
                            if not self.hint_used:
                                self.use_hint()
                        elif event.unicode.isalpha() and len(input_text) == 0:
                            input_text = event.unicode.upper()

                    elif self.game_state in ["win", "game_over"]:
                        if event.key == pygame.K_SPACE:
                            self.game_state = "welcome"

            self.update()

            if self.game_state == "welcome":
                self.draw_welcome_screen()
            elif self.game_state == "playing":
                self.draw_game_screen()
                if input_text:
                    shake_x, shake_y = self.get_shake_offset()
                    input_surface = self.main_font.render(f"Input: {input_text}", True, BLUE)
                    input_rect = input_surface.get_rect(center=(SCREEN_WIDTH // 2 + shake_x, 700 + shake_y))
                    self.screen.blit(input_surface, input_rect)
            else:
                self.draw_end_screen()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = WildHuntHangman()
    game.run()
