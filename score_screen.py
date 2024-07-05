import pygame
import gameconfig as gc


class ScoreScreen:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets
        self.white_nums = self.assets.number_black_white
        self.orange_nums = self.assets.number_black_orange

        self.active = False
        self.timer = pygame.time.get_ticks()
        self.score_timer = 100

        self.images = self.assets.score_sheet_images

        #  Player Score Totals and Score Lists
        self.p1_score = 0
        self.p1_kill_list = []
        self.p2_score = 0
        self.p2_kill_list = []

        self.top_score = 0
        self.stage = 0

        self.scoresheet = self.generate_scoresheet_screen()
        #  Top score and Stage Number Images Creation
        self._create_top_score_and_stage_number_images()
        #  Update the player Score images with the latest score
        self.update_player_score_images()

        #  Line 1 : [Number of Tanks, Tank Score Number]
        self.pl1_score_values = {"line1": [0, 0], "line2": [0, 0], "line3": [0, 0], "line4": [0, 0], "total": 0}
        self.pl2_score_values = {"line1": [0, 0], "line2": [0, 0], "line3": [0, 0], "line4": [0, 0], "total": 0}

        self.p1_tank_num_imgs, self.p1_tank_score_imgs = self.generate_tank_kill_images(14, 7, self.pl1_score_values)
        self.p2_tank_num_imgs, self.p2_tank_score_imgs = self.generate_tank_kill_images(20, 25, self.pl2_score_values)

    def update(self, game_over):
        if not pygame.time.get_ticks() - self.timer >= 3000:
            return

        if len(self.p1_kill_list) > 0:
            if pygame.time.get_ticks() - self.timer >= 100:
                score = self.p1_kill_list.pop(0)
                self.update_score(score, "player1")
                self.assets.score_sound.play()
                self.score_timer = pygame.time.get_ticks()
                return

        if len(self.p2_kill_list) > 0:
            if pygame.time.get_ticks() - self.timer >= 100:
                score = self.p2_kill_list.pop(0)
                self.update_score(score, "player2")
                self.assets.score_sound.play()
                self.score_timer = pygame.time.get_ticks()
                return

        if pygame.time.get_ticks() - self.score_timer >= 3000:
            if game_over:
                self.game.end_game = True
                return
            self.active = False
            self.game.change_level(self.p1_score, self.p2_score)
            self.clear_for_new_stage()

    def draw(self, window):
        window.fill(gc.BLACK)
        window.blit(self.scoresheet, (0, 0))
        window.blit(self.hi_score_nums_total, self.hi_score_nums_rect)
        window.blit(self.stage_num, self.stage_num_rect)

        if self.game.player1_active:
            window.blit(self.pl_1_score, self.pl_1_score_rect)
            for value in self.p1_tank_num_imgs.values():
                window.blit(value[0], value[1])
            for value in self.p1_tank_score_imgs.values():
                window.blit(value[0], value[1])

        if self.game.player2_active:
            window.blit(self.pl_2_score, self.pl_2_score_rect)
            for value in self.p2_tank_num_imgs.values():
                window.blit(value[0], value[1])
            for value in self.p2_tank_score_imgs.values():
                window.blit(value[0], value[1])

    def generate_scoresheet_screen(self):
        """Generate a basic template screen for the score card transition screen"""
        surface = pygame.Surface((gc.SCREENWIDTH, gc.SCREENHEIGHT))
        surface.fill(gc.BLACK)
        new_img = gc.imageSize // 2
        surface.blit(self.images["hiScore"], (new_img * 8, new_img * 4))
        surface.blit(self.images["stage"], (new_img * 12, new_img * 6))

        arrow_left = self.images["arrow"]
        arrow_right = pygame.transform.flip(arrow_left, True, False)

        if self.game.player1_active:
            surface.blit(self.images["player1"], (new_img * 3, new_img * 8))
        if self.game.player2_active:
            surface.blit(self.images["player2"], (new_img * 21, new_img * 8))

        for num, yPos in enumerate([12.5, 15, 17.5, 20]):
            if self.game.player1_active:
                surface.blit(self.images["pts"], (new_img * 8, new_img * yPos))
                surface.blit(arrow_left, (new_img * 14, new_img * yPos))
            if self.game.player2_active:
                surface.blit(self.images["pts"], (new_img * 26, new_img * yPos))
                surface.blit(arrow_right, (new_img * 17, new_img * yPos))
            surface.blit(self.assets.tank_images[f"Tank_{num + 4}"]["Silver"]["Up"][0],
                         (new_img * 15, new_img * (yPos - 0.5)))

        surface.blit(self.images["total"], (new_img * 6, new_img * 22))
        return surface

    def number_image(self, score, number_color):
        """Convert a number into an image"""
        num = str(score)
        length = len(num)
        score_surface = pygame.Surface((gc.imageSize//2 * length, gc.imageSize // 2))
        for index, number in enumerate(num):
            score_surface.blit(number_color[int(number)], (gc.imageSize//2 * index, 0))
        return score_surface

    def update_player_score_images(self):
        self.pl_1_score = self.number_image(self.p1_score, self.orange_nums)
        self.pl_1_score_rect = self.pl_1_score.get_rect(
            topleft=(gc.imageSize//2 * 11 - self.pl_1_score.get_width(), gc.imageSize // 2 * 10))

        self.pl_2_score = self.number_image(self.p2_score, self.orange_nums)
        self.pl_2_score_rect = self.pl_2_score.get_rect(
            topleft=(gc.imageSize // 2 * 29 - self.pl_2_score.get_width(), gc.imageSize // 2 * 10))

    def _create_top_score_and_stage_number_images(self):
        self.hi_score_nums_total = self.number_image(self.top_score, self.orange_nums)
        self.hi_score_nums_rect = self.hi_score_nums_total.get_rect(
            topleft=(gc.imageSize//2 * 19, gc.imageSize // 2 * 4))

        self.stage_num = self.number_image(self.stage, self.white_nums)
        self.stage_num_rect = self.stage_num.get_rect(topleft=(gc.imageSize//2 * 19, gc.imageSize//2 * 6))

    def update_basic_info(self, top_score, stage_number):
        self.top_score = top_score
        self.stage = stage_number
        self._create_top_score_and_stage_number_images()

    def generate_tank_kill_images(self, x1, x2, pl_dict):
        """Generate a dictionary of images and x/y coords for values"""
        yPos = [12.5, 15, 17.5, 20]
        size = gc.imageSize // 2

        #  Generate the number images for the tank numbers
        tank_num_imgs = {}
        for i in range(4):
            tank_num_imgs[f"line{i+1}"] = []
            tank_num_imgs[f"line{i + 1}"].append(self.number_image(pl_dict[f"line{i+1}"][0], self.white_nums))
            tank_num_imgs[f"line{i + 1}"].append(
                (size * x1 - tank_num_imgs[f"line{i + 1}"][0].get_width(), size * yPos[i]))
        tank_num_imgs["total"] = []
        tank_num_imgs["total"].append(self.number_image(pl_dict["total"], self.white_nums))
        tank_num_imgs["total"].append((size * x1 - tank_num_imgs["total"][0].get_width(), size * 22.5))

        # generate Images for tank score per line
        tank_score_imgs = {}
        for i in range(4):
            tank_score_imgs[f"line{i+1}"] = []
            tank_score_imgs[f"line{i + 1}"].append(self.number_image(pl_dict[f"line{i+1}"][0], self.white_nums))
            tank_score_imgs[f"line{i + 1}"].append(
                (size * x2 - tank_score_imgs[f"line{i + 1}"][0].get_width(), size * yPos[i]))
        return tank_num_imgs, tank_score_imgs

    def update_score(self, score, player):
        score_dict = {100: "line1", 200: "line2", 300: "line3", 400: "line4"}
        if player == "player1":
            self.pl1_score_values[score_dict[score]][0] += 1
            self.pl1_score_values[score_dict[score]][1] += score
            self.pl1_score_values["total"] += 1
            self.p1_score += score
            self.p1_tank_num_imgs, self.p1_tank_score_imgs = self.generate_tank_kill_images(
                14, 7, self.pl1_score_values)
        else:
            self.pl2_score_values[score_dict[score]][0] += 1
            self.pl2_score_values[score_dict[score]][1] += score
            self.pl2_score_values["total"] += 1
            self.p2_score += score
            self.p2_tank_num_imgs, self.p2_tank_score_imgs = self.generate_tank_kill_images(
                20, 25, self.pl2_score_values)
        self.update_player_score_images()

    def clear_for_new_stage(self):
        self.p1_kill_list = []
        self.p2_kill_list = []

        self.pl1_score_values = {"line1": [0, 0], "line2": [0, 0], "line3": [0, 0], "line4": [0, 0], "total": 0}
        self.pl2_score_values = {"line1": [0, 0], "line2": [0, 0], "line3": [0, 0], "line4": [0, 0], "total": 0}

        self.p1_tank_num_imgs, self.p1_tank_score_imgs = self.generate_tank_kill_images(14, 7, self.pl1_score_values)
        self.p2_tank_num_imgs, self.p2_tank_score_imgs = self.generate_tank_kill_images(20, 25, self.pl2_score_values)