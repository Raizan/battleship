__author__ = "Reisuke"

# pygame imported via GameObjects
from scripts.DialogBox import *
from scripts.GameObjects import *


class Game:
    def __init__(self):
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 400
        self.FPS = 30
        pygame.init()
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        icon = pygame.image.load("./assets/image/icon.png").convert_alpha()
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Initializing...")
        self.clock = pygame.time.Clock()
        self.running = 1
        self.phase = "idle"
        self.state_enemy_board = {(i, j): 0 for i in range(10) for j in range(10)}
        self.state_player_board = {(i, j): 0 for i in range(10) for j in range(10)}
        self.my_ship_count = 0
        self.enemy_ship_count = 0

    def init_board(self):
        board = pygame.Surface(self.window.get_size())
        board = board.convert()

        return board

    def draw_board(self, board):

        self.window.blit(board, (0, 0))
        pygame.display.flip()

    def draw_terrain(self):
        self.window.fill((255, 255, 255))
        # Grid 10 x 10
        col_size = 10
        row_size = 10

        global row_now, col_now
        row_now = 0
        col_now = 0
        terrain = []

        # Generate enemy board
        x_now = 0
        y_now = 0
        for x in range(col_size):
            for y in range(row_size):
                terrain.append(Water(self.window, col_now, row_now, x_now, y_now, 0))
                x_now += 32
                col_now += 1
            y_now += 32
            x_now = 0
            row_now += 1
            col_now = 0

        # Assign global value
        col_now = 10
        row_now = 0

        # Generate player board
        x_now = 320
        y_now = 0
        for x in range(col_size):
            for y in range(row_size):
                terrain.append(Water(self.window, col_now, row_now, x_now, y_now, 0))
                x_now += 32
                col_now += 1
            y_now += 32
            x_now = 320
            row_now += 1
            col_now = 10

        return terrain

    def draw_line_grid(self):
        col_size = 20
        row_size = 10
        x_now = 0
        y_now = 0
        lines = []
        for x in range(col_size):
            lines.append(Line(self.window, x_now, y_now, "vertical"))
            x_now += 32

        x_now = 640 / 2
        lines.append(Line(self.window, x_now, y_now, "separator"))

        x_now = 0
        for y in range(row_size):
            lines.append(Line(self.window, x_now, y_now, "horizontal"))
            y_now += 32

        return lines

    def show_menu(self):
        rects = {}
        info_decor_image = pygame.image.load("./assets/image/info_decor.png")
        rects["decor"] = self.window.blit(info_decor_image, (0, 320))

        info_help_image = pygame.image.load("./assets/image/info_help.png")
        rects["help"] = self.window.blit(info_help_image, (148, 320))

        info_about_image = pygame.image.load("./assets/image/info_about.png")
        rects["about"] = self.window.blit(info_about_image, (148, 339))

        info_status_image = pygame.image.load("./assets/image/info_status.png")
        rects["status"] = self.window.blit(info_status_image, (207, 320))

        button_horizontal_image = pygame.image.load("./assets/image/button_horizontal.png")
        rects["button_horizontal"] = self.window.blit(button_horizontal_image, (0, 360))

        button_vertical_image = pygame.image.load("./assets/image/button_vertical.png")
        rects["button_vertical"] = self.window.blit(button_vertical_image, (160, 360))

        ready_image = pygame.image.load("./assets/image/ready.png")
        rects["ready"] = self.window.blit(ready_image, (320, 320))

        return rects

    def board_position(self, mouseX, mouseY):
        if mouseY < 32:
            row = 0
        elif mouseY < 64:
            row = 1
        elif mouseY < 96:
            row = 2
        elif mouseY < 128:
            row = 3
        elif mouseY < 160:
            row = 4
        elif mouseY < 192:
            row = 5
        elif mouseY < 224:
            row = 6
        elif mouseY < 256:
            row = 7
        elif mouseY < 288:
            row = 8
        elif mouseY < 320:
            row = 9
        elif mouseY < 352:
            row = 10
        elif mouseY < 384:
            row = 11
        elif mouseY < 416:
            row = 12
        elif mouseY < 448:
            row = 13
        elif mouseY < 480:
            row = 14
        elif mouseY < 512:
            row = 15
        elif mouseY < 544:
            row = 16
        elif mouseY < 576:
            row = 17
        elif mouseY < 608:
            row = 18
        elif mouseY < 640:
            row = 19
        elif mouseY < 672:
            row = 20

        if mouseX < 32:
            col = 0
        elif mouseX < 64:
            col = 1
        elif mouseX < 96:
            col = 2
        elif mouseX < 128:
            col = 3
        elif mouseX < 160:
            col = 4
        elif mouseX < 192:
            col = 5
        elif mouseX < 224:
            col = 6
        elif mouseX < 256:
            col = 7
        elif mouseX < 288:
            col = 8
        elif mouseX < 320:
            col = 9
        elif mouseX < 352:
            col = 10
        elif mouseX < 384:
            col = 11
        elif mouseX < 416:
            col = 12
        elif mouseX < 448:
            col = 13
        elif mouseX < 480:
            col = 14
        elif mouseX < 512:
            col = 15
        elif mouseX < 544:
            col = 16
        elif mouseX < 576:
            col = 17
        elif mouseX < 608:
            col = 18
        elif mouseX < 640:
            col = 19
        elif mouseX < 672:
            col = 20

        return col, row

    def click_board(self, terrain):
        mouseX, mouseY = pygame.mouse.get_pos()
        col, row = self.board_position(mouseX, mouseY)
        temp = None
        for i in terrain:
            if i.col == col and i.row == row:
                temp = i

        image = pygame.image.load("./assets/image/clicked.png")
        # temp.image_clicked = image
        # temp.flag = 1
        terrain_rect = self.window.blit(image, (temp.x, temp.y))
        pygame.display.flip()

        return terrain_rect

    def safe_end(self):
        pygame.quit()

    def condition_check(self, terrain_rect):
        x = terrain_rect[0]
        y = terrain_rect[1]
        col, row = self.board_position(x, y)

        if self.my_ship_count == 8:
            flag = "err"
            title = "ERROR! SHIP_DEPLOY_LIMIT\t"
            message = "Ship deploy limit reached.\t"
            dialog_box(flag, title, message)
            return 0

        elif col > 9:
            flag = "err"
            title = "ERROR! SHIP_OUT_OF_RANGE\t"
            message = "You are trying to deploy outside your own area.\nPlease choose one grid on the left side of yellow line."
            dialog_box(flag, title, message)
            return 0

        elif self.phase == "deploy_horizontal":
            if col > 7:
                flag = "err"
                title = "ERROR! SHIP_NOT_FULLY_DEPLOYED\t"
                message = "Your ship is not fully on your area.\t\nPlease select other grid!\t\t"
                dialog_box(flag, title, message)

                return 0

            else:
                check = [0 for i in range(3)]
                for i in range(3):
                    if self.state_player_board[(col + i, row)] == 1:
                        check[i] = 1
                for i in check:
                    if i == 1:
                        flag = "err"
                        title = "ERROR! SHIP_UNIT_OVERLAP\t"
                        message = "Your new ship will overlap with other unit.\nPlease select other grid!"
                        dialog_box(flag, title, message)
                        return 0

        elif self.phase == "deploy_vertical":
            if row > 7:
                flag = "err"
                title = "ERROR! SHIP_NOT_FULLY_DEPLOYED\t"
                message = "Your ship is not fully on your area.\t\nPlease select other grid!"
                dialog_box(flag, title, message)
                return 0

            else:
                check = [0 for i in range(3)]
                for i in range(3):
                    if self.state_player_board[(col, row + i)] == 1:
                        check[i] = 1
                for i in check:
                    if i == 1:
                        flag = "err"
                        title = "ERROR! SHIP_UNIT_OVERLAP\t"
                        message = "Your new ship will overlap with other unit.\nPlease select other grid!"
                        dialog_box(flag, title, message)
                        return 0

        # Clear, sir! Ready to deploy, sir!
        return 1

    def deploy_my_ship(self, terrain_rect, ships):
        x = terrain_rect[0]
        y = terrain_rect[1]
        col, row = self.board_position(x, y)

        if self.phase == "deploy_horizontal":
            ships.append(Battleship(self.window, col, row, x, y, "horizontal"))
            for i in range(3):
                self.state_player_board[(col + i, row)] = 1

        elif self.phase == "deploy_vertical":
            ships.append(Battleship(self.window, col, row, x, y, "vertical"))
            for i in range(3):
                self.state_player_board[(col, row + i)] = 1

        self.my_ship_count += 1
        return ships
        # Update player board state

    def menu_action(self, action):
        if action == "button_horizontal":
            self.phase = "deploy_horizontal"

        elif action == "button_vertical":
            self.phase = "deploy_vertical"

        elif action == "ready":
            self.phase = "ready"

        elif action == "help":
            # Create dialog box for help
            pass

        elif action == "about":
            flag = "info"
            title = "ABOUT BATTLESHIP GAME"
            part1 = "\t\tBATTLESHIP GAME\n\n"
            part2 = "Network Programming Final Project\n"
            part3 = "Informatics Department\nInstitut Teknologi Sepuluh Nopember\nSurabaya, Indonesia\n\n"
            part4 = "Written by:\n\tAndrew Joshua N.\t(5112100149)\n"
            part5 = "\tReyhan Arief\t(5112100175)\n\n\n"
            part6 = "Icon, terrain and ship sprite downloaded from OpenGameArt.org\n"
            part7 = "which are licensed under Creative Commons."
            message = part1 + part2 + part3 + part4 + part5 + part6 + part7
            dialog_box(flag, title, message)

    def switch_phase(self):
        pass

    def run(self):
        board = self.init_board()
        self.draw_board(board)
        terrain = self.draw_terrain()
        lines = self.draw_line_grid()
        terrain_rect = None
        ships = []
        while self.running:
            rects = self.show_menu()
            if self.phase == "idle":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = 0

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if rects["button_horizontal"].collidepoint(pos):
                            self.menu_action("button_horizontal")

                        elif rects["button_vertical"].collidepoint(pos):
                            self.menu_action("button_vertical")

                        elif rects["status"].collidepoint(pos):
                            self.menu_action("status")

                        elif rects["about"].collidepoint(pos):
                            self.menu_action("about")

                        elif rects["help"].collidepoint(pos):
                            self.menu_action("help")

                        elif rects["decor"].collidepoint(pos):
                            self.menu_action("decor")

                        elif rects["ready"].collidepoint(pos):
                            self.menu_action("ready")


                        else:
                            pass

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                        # Flip ship
                        continue

                    elif event.type == pygame.MOUSEMOTION:
                        continue

            elif self.phase == "deploy_horizontal":
                clicked = pygame.image.load("./assets/image/button_horizontal_p.png")
                self.window.blit(clicked, (0, 360))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = 0

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pos = pygame.mouse.get_pos()

                        if rects["button_horizontal"].collidepoint(pos):
                            self.menu_action("button_horizontal")

                        elif rects["button_vertical"].collidepoint(pos):
                            self.menu_action("button_vertical")

                        elif rects["status"].collidepoint(pos):
                            self.menu_action("status")

                        elif rects["about"].collidepoint(pos):
                            self.menu_action("about")

                        elif rects["help"].collidepoint(pos):
                            self.menu_action("help")

                        elif rects["decor"].collidepoint(pos):
                            self.menu_action("decor")

                        elif rects["ready"].collidepoint(pos):
                            self.menu_action("ready")

                        else:
                            terrain_rect = self.click_board(terrain)
                            flag = self.condition_check(terrain_rect)

                            if flag == 1:
                                ships = self.deploy_my_ship(terrain_rect, ships)
                                self.phase = "idle"

                            else:
                                self.phase = "deploy_horizontal"
                            # mouseX, mouseY = pygame.mouse.get_pos()
                            # col, row = self.board_position(mouseX, mouseY)
                            # temp = None
                            # for i in terrain:
                            #     if i.col == col and i.row == row:
                            #         temp = i
                            # # If on player's view
                            # terrain_rect = self.click_board(terrain)
                            # self.deploy_my_ship(terrain_rect, temp.col, temp.row)
                            # # If on enemy's view

                            # Render terrain sprites

            elif self.phase == "deploy_vertical":
                clicked = pygame.image.load("./assets/image/button_vertical_p.png")
                self.window.blit(clicked, (160, 360))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = 0

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pos = pygame.mouse.get_pos()

                        if rects["button_horizontal"].collidepoint(pos):
                            self.menu_action("button_horizontal")

                        elif rects["button_vertical"].collidepoint(pos):
                            self.menu_action("button_vertical")

                        elif rects["status"].collidepoint(pos):
                            self.menu_action("status")

                        elif rects["about"].collidepoint(pos):
                            self.menu_action("about")

                        elif rects["help"].collidepoint(pos):
                            self.menu_action("help")

                        elif rects["decor"].collidepoint(pos):
                            self.menu_action("decor")

                        elif rects["ready"].collidepoint(pos):
                            self.menu_action("ready")

                        else:
                            terrain_rect = self.click_board(terrain)
                            flag = self.condition_check(terrain_rect)

                            if flag == 1:
                                ships = self.deploy_my_ship(terrain_rect, ships)
                                self.phase = "idle"

                            else:
                                self.phase = "deploy_vertical"

                            # mouseX, mouseY = pygame.mouse.get_pos()
                            # col, row = self.board_position(mouseX, mouseY)
                            # temp = None
                            # for i in terrain:
                            #     if i.col == col and i.row == row:
                            #         temp = i
                            # # If on player's view
                            # terrain_rect = self.click_board(terrain)
                            # self.deploy_my_ship(terrain_rect, temp.col, temp.row)
                            # # If on enemy's view

                            # Render terrain sprites

            elif self.phase == "start":
                pass

            elif self.phase == "player":
                pass

            elif self.phase == "enemy":
                pass

            # Render sprites
            for water in terrain:
                water.update()

            for line in lines:
                line.render()

            if len(ships) != 0:
                for ship in ships:
                    ship.render()

            # FPS 30
            get_fps = self.clock.tick(self.FPS)
            caption = "Battleship Game | FPS " + str(get_fps)
            pygame.display.set_caption(caption)
            pygame.display.flip()

        self.safe_end()

if __name__ == "__main__":
    g = Game()
    g.run()