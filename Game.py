__author__ = "Reisuke"

from scripts.DialogBox import *
from scripts.GameObjects import *
from Client import *
from time import sleep


class Game:
    def __init__(self):
        # Init game
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

        # Initialize client networking
        self.client_network = Client()

        # Game data
        self.phase = "idle"
        self.state_enemy_board = [[0 for x in range(10)] for y in range(10)]
        self.state_player_board = [[0 for x in range(10)] for y in range(10)]
        self.counter_my_ship = 0
        self.counter_enemy_ship = 0
        self.maximum_ship = 1
        self.ready_sent = 0
        self.my_turn = None
        # Contains image object to be rendered
        self.ships = []
        self.hit = []
        self.terrain = []

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

        # Generate enemy board
        x_now = 0
        y_now = 0
        for x in range(col_size):
            for y in range(row_size):
                self.terrain.append(Water(self.window, col_now, row_now, x_now, y_now, 0))
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
                self.terrain.append(Water(self.window, col_now, row_now, x_now, y_now, 0))
                x_now += 32
                col_now += 1
            y_now += 32
            x_now = 320
            row_now += 1
            col_now = 10

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

    def click_board(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        col, row = self.board_position(mouseX, mouseY)
        temp = None
        for i in range(len(self.terrain)):
            if self.terrain[i].col == col and self.terrain[i].row == row:
                if (self.phase == "my_turn" or self.phase == "enemy_turn") and col > 9:
                    self.terrain[i].flag = "clicked"
                temp = self.terrain[i]
                break

        image = pygame.image.load("./assets/image/clicked.png")
        terrain_rect = self.window.blit(image, (temp.x, temp.y))

        pygame.display.flip()

        return terrain_rect

    def condition_check(self, terrain_rect):
        x = terrain_rect[0]
        y = terrain_rect[1]
        col, row = self.board_position(x, y)

        if self.phase == "deploy_horizontal":
            if self.counter_my_ship == self.maximum_ship:
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

            elif col > 7:
                flag = "err"
                title = "ERROR! SHIP_NOT_FULLY_DEPLOYED\t"
                message = "Your ship is not fully on your area.\t\nPlease select other grid!\t\t"
                dialog_box(flag, title, message)
                return 0

            else:
                check = [0 for i in range(3)]
                for i in range(3):
                    if self.state_player_board[row][col + i] == 1:
                        check[i] = 1
                for i in check:
                    if i == 1:
                        flag = "err"
                        title = "ERROR! SHIP_UNIT_OVERLAP\t"
                        message = "Your new ship will overlap with other unit.\nPlease select other grid!"
                        dialog_box(flag, title, message)
                        return 0

        elif self.phase == "deploy_vertical":
            if self.counter_my_ship == self.maximum_ship:
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

            elif row > 7:
                flag = "err"
                title = "ERROR! SHIP_NOT_FULLY_DEPLOYED\t"
                message = "Your ship is not fully on your area.\t\nPlease select other grid!"
                dialog_box(flag, title, message)
                return 0

            else:
                check = [0 for i in range(3)]
                for i in range(3):
                    if self.state_player_board[row + i][col] == 1:
                        check[i] = 1
                for i in check:
                    if i == 1:
                        flag = "err"
                        title = "ERROR! SHIP_UNIT_OVERLAP\t"
                        message = "Your new ship will overlap with other unit.\nPlease select other grid!"
                        dialog_box(flag, title, message)
                        return 0

        elif self.phase == "my_turn":
            if col < 10:
                flag = "err"
                title = "ERROR! ATTACKING_YOUR_AREA\t"
                message = "You are trying to attack your own area.\nPlease choose one grid on the right side of yellow line."
                dialog_box(flag, title, message)
                return 0

        return 1

    def deploy_my_ship(self, terrain_rect):
        x = terrain_rect[0]
        y = terrain_rect[1]
        col, row = self.board_position(x, y)

        if self.phase == "deploy_horizontal":
            self.ships.append(Battleship(self.window, col, row, x, y, "horizontal"))
            for i in range(3):
                self.state_player_board[row][col + i] = 1

        elif self.phase == "deploy_vertical":
            self.ships.append(Battleship(self.window, col, row, x, y, "vertical"))
            for i in range(3):
                self.state_player_board[row + i][col] = 1
        self.counter_my_ship += 1

    def menu_action(self, action):
        if action == "button_horizontal":
            self.phase = "deploy_horizontal"

        elif action == "button_vertical":
            self.phase = "deploy_vertical"

        elif action == "ready":
            if self.ready_sent == 0:
                temp_data = {"action": "ready", "my_board": self.state_player_board}
                self.client_network.Send(temp_data)
                self.ready_sent = 1
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

    def show_menu(self):
        rects = {}

        if self.phase == "deploy_phase" or self.phase == "deploy_horizontal" or self.phase == "deploy_vertical":
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

        elif self.phase == "ready":
            info_decor_image = pygame.image.load("./assets/image/info_decor.png")
            rects["decor"] = self.window.blit(info_decor_image, (0, 320))

            info_help_image = pygame.image.load("./assets/image/info_help.png")
            rects["help"] = self.window.blit(info_help_image, (148, 320))

            info_about_image = pygame.image.load("./assets/image/info_about.png")
            rects["about"] = self.window.blit(info_about_image, (148, 339))

            info_status_image = pygame.image.load("./assets/image/info_status.png")
            rects["status"] = self.window.blit(info_status_image, (207, 320))

            button_horizontal_image = pygame.image.load("./assets/image/your_enemy_is_still_deploying.png")
            rects["announcement"] = self.window.blit(button_horizontal_image, (0, 360))

            ready_image = pygame.image.load("./assets/image/please_wait.png")
            rects["please_wait"] = self.window.blit(ready_image, (320, 320))

        elif self.phase == "my_turn":
            info_decor_image = pygame.image.load("./assets/image/info_decor.png")
            rects["decor"] = self.window.blit(info_decor_image, (0, 320))

            info_help_image = pygame.image.load("./assets/image/info_help.png")
            rects["help"] = self.window.blit(info_help_image, (148, 320))

            info_about_image = pygame.image.load("./assets/image/info_about.png")
            rects["about"] = self.window.blit(info_about_image, (148, 339))

            info_status_image = pygame.image.load("./assets/image/info_status.png")
            rects["status"] = self.window.blit(info_status_image, (207, 320))

            button_horizontal_image = pygame.image.load("./assets/image/its_your_turn.png")
            rects["announcement"] = self.window.blit(button_horizontal_image, (0, 360))

            ready_image = pygame.image.load("./assets/image/your_turn.png")
            rects["your_turn"] = self.window.blit(ready_image, (320, 320))

        elif self.phase == "enemy_turn":
            info_decor_image = pygame.image.load("./assets/image/info_decor.png")
            rects["decor"] = self.window.blit(info_decor_image, (0, 320))
            pygame.display.flip()

            info_help_image = pygame.image.load("./assets/image/info_help.png")
            rects["help"] = self.window.blit(info_help_image, (148, 320))
            pygame.display.flip()

            info_about_image = pygame.image.load("./assets/image/info_about.png")
            rects["about"] = self.window.blit(info_about_image, (148, 339))
            pygame.display.flip()

            info_status_image = pygame.image.load("./assets/image/info_status.png")
            rects["status"] = self.window.blit(info_status_image, (207, 320))
            pygame.display.flip()

            button_horizontal_image = pygame.image.load("./assets/image/your_enemy_is_thinking.png")
            rects["announcement"] = self.window.blit(button_horizontal_image, (0, 360))
            pygame.display.flip()

            ready_image = pygame.image.load("./assets/image/enemy_turn.png")
            rects["enemy_turn"] = self.window.blit(ready_image, (320, 320))
            pygame.display.flip()

        elif self.phase == "waiting":
            info_decor_image = pygame.image.load("./assets/image/info_decor.png")
            rects["decor"] = self.window.blit(info_decor_image, (0, 320))
            pygame.display.flip()

            info_help_image = pygame.image.load("./assets/image/info_help.png")
            rects["help"] = self.window.blit(info_help_image, (148, 320))
            pygame.display.flip()

            info_about_image = pygame.image.load("./assets/image/info_about.png")
            rects["about"] = self.window.blit(info_about_image, (148, 339))
            pygame.display.flip()

            info_status_image = pygame.image.load("./assets/image/info_status.png")
            rects["status"] = self.window.blit(info_status_image, (207, 320))
            pygame.display.flip()

            button_horizontal_image = pygame.image.load("./assets/image/waiting_server.png")
            rects["announcement"] = self.window.blit(button_horizontal_image, (0, 360))
            pygame.display.flip()

            ready_image = pygame.image.load("./assets/image/please_wait.png")
            rects["please_wait"] = self.window.blit(ready_image, (320, 320))
            pygame.display.flip()

        return rects

    def menu_switch(self, pos, rects):
        if self.phase == "deploy_phase":
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

        elif self.phase == "deploy_horizontal":
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
                terrain_rect = self.click_board()
                flag = self.condition_check(terrain_rect)

                if flag == 1:
                    self.deploy_my_ship(terrain_rect)
                    self.phase = "deploy_phase"

                else:
                    self.phase = "deploy_horizontal"

        elif self.phase == "deploy_vertical":
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
                terrain_rect = self.click_board()
                flag = self.condition_check(terrain_rect)

                if flag == 1:
                    self.deploy_my_ship(terrain_rect)
                    self.phase = "deploy_phase"

                else:
                    self.phase = "deploy_vertical"

        elif self.phase == "ready":
            if rects["status"].collidepoint(pos):
                self.menu_action("status")

            elif rects["about"].collidepoint(pos):
                self.menu_action("about")

            elif rects["help"].collidepoint(pos):
                self.menu_action("help")

            elif rects["decor"].collidepoint(pos):
                self.menu_action("decor")

            elif rects["please_wait"].collidepoint(pos):
                pass

            elif rects["announcement"].collidepoint(pos):
                pass

        elif self.phase == "my_turn":
            if rects["status"].collidepoint(pos):
                self.menu_action("status")

            elif rects["about"].collidepoint(pos):
                self.menu_action("about")

            elif rects["help"].collidepoint(pos):
                self.menu_action("help")

            elif rects["decor"].collidepoint(pos):
                self.menu_action("decor")

            elif rects["your_turn"].collidepoint(pos):
                pass

            elif rects["announcement"].collidepoint(pos):
                pass

            else:
                terrain_rect = self.click_board()
                flag = self.condition_check(terrain_rect)

                if flag == 1:
                    self.attack_ship(terrain_rect)

        elif self.phase == "enemy_turn":
            if rects["status"].collidepoint(pos):
                self.menu_action("status")

            elif rects["about"].collidepoint(pos):
                self.menu_action("about")

            elif rects["help"].collidepoint(pos):
                self.menu_action("help")

            elif rects["decor"].collidepoint(pos):
                self.menu_action("decor")

            elif rects["enemy_turn"].collidepoint(pos):
                pass

            elif rects["announcement"].collidepoint(pos):
                pass

        elif self.phase == "waiting":
            if rects["status"].collidepoint(pos):
                self.menu_action("status")

            elif rects["about"].collidepoint(pos):
                self.menu_action("about")

            elif rects["help"].collidepoint(pos):
                self.menu_action("help")

            elif rects["decor"].collidepoint(pos):
                self.menu_action("decor")

            elif rects["please_wait"].collidepoint(pos):
                pass

            elif rects["announcement"].collidepoint(pos):
                pass

    def attack_ship(self, terrain_rect):
        x = terrain_rect[0]
        y = terrain_rect[1]
        flag = self.condition_check(terrain_rect)

        if flag == 1:
            col, row = self.board_position(x, y)
            attack_data = {"action": "attack", "col": col, "row": row}
            self.client_network.Send(attack_data)
            self.phase = "waiting"
            # Change col row coordinate to player grid coordinate on server
            # Send col row with flag "action : attack"

    def update_board(self, board_state, board_counter):
        if self.my_turn == "player_1":
            self.state_player_board = board_state[0]
            self.state_enemy_board = board_state[1]

            if board_counter[0] == 0 and board_counter[0] is not None:
                flag = "info"
                title = "INFO: LOSE"
                message = "You lose.\t\nGame will exit."
                dialog_box(flag, title, message)
                return "exit"

            elif board_counter[1] == 0 and board_counter[1] is not None:
                flag = "info"
                title = "INFO: WIN"
                message = "You win.\t\nGame will exit."
                dialog_box(flag, title, message)
                return "exit"

        elif self.my_turn == "player_2":
            self.state_player_board = board_state[1]
            self.state_enemy_board = board_state[0]

            if board_counter[0] == 0 and board_counter[0] is not None:
                flag = "info"
                title = "INFO: WIN"
                message = "Congratulations! You win.\t\nGame will exit."
                dialog_box(flag, title, message)
                return "exit"

            elif board_counter[1] == 0 and board_counter[1] is not None:
                flag = "info"
                title = "INFO: LOSE"
                message = "Sorry. You lose.\t\nGame will exit."
                dialog_box(flag, title, message)
                return "exit"

        return "continue"

    def run(self):
        # The game
        board = self.init_board()
        self.draw_board(board)
        self.draw_terrain()
        lines = self.draw_line_grid()
        deploy_phase_announcement = 0

        while self.running:
            pygame.display.flip()
            # Networking loop
            self.client_network.Loop()

            # Maintaining game status here
            to_server = {"action": "broadcast_request"}
            self.client_network.Send(to_server)        # Send request here
            # self.client_network.Loop()
            # self.client_network.Loop()
            data = self.client_network.PassData()    # get data here

            # self.client_network.Loop()
            print "Data: ", data
            print "Phase: ", self.phase
            print "my_turn: ", self.my_turn
            # Checking game status

            if not data or data["action"] == "disconnected":
                flag = "err"
                title = "ERROR! SERVER_OFFLINE"
                message = "Server is offline.\nContact server administrator for further information.\nGame will close."
                dialog_box(flag, title, message)
                break

            if data["action"] == "matchmaking":
                self.phase = "matchmaking"

            if data["action"] == "broadcast":
                if data["status"] == "opponent_disconnected":
                    flag = "err"
                    title = "ERROR! OPPONENT_DISCONNECTED"
                    message = "Your opponent has been disconnected.\t\nGame will close."
                    dialog_box(flag, title, message)
                    break

                # Determine player order
                if "order" in data:
                    if data["order"] == "player_1":
                        self.my_turn = "player_1"

                    elif data["order"] == "player_2":
                        self.my_turn = "player_2"

                # Turn switch
                if data["status"] == "player_1":
                    if self.my_turn == "player_1":
                        self.phase = "my_turn"
                    elif self.my_turn == "player_2":
                        self.phase = "enemy_turn"

                if data["status"] == "player_2":
                    if self.my_turn == "player_2":
                        self.phase = "my_turn"
                    elif self.my_turn == "player_1":
                        self.phase = "enemy_turn"

                if data["status"] == "deploy_phase" and deploy_phase_announcement == 0:
                    self.phase = "deploy_phase"
                    deploy_phase_announcement = 1

                if "board_state" in data:
                    win_or_lose = self.update_board(data["board_state"], data["board_counter"])
                    if win_or_lose == "exit":
                        break

            # Game processing
            if self.phase == "ready":
                if self.counter_my_ship < self.maximum_ship:
                    flag = "err"
                    title = "ERROR! NOT_ALL_DEPLOYED"
                    message = "You can't READY because not all ship deployed.\t\nPlease deploy your ship until all deployed."
                    dialog_box(flag, title, message)
                    self.phase = "deploy_phase"

            if self.phase == "matchmaking":
                pygame.display.set_caption("Matchmaking. Please wait...")

            else:
                # FPS 30
                get_fps = self.clock.tick(self.FPS)
                caption = "Battleship Game | FPS " + str(get_fps)
                pygame.display.set_caption(caption)

            rects = self.show_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    to_server = {"action": "quit"}
                    self.client_network.Send(to_server)
                    self.running = 0

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.menu_switch(pos, rects)

            # Render
            if self.phase == "deploy_horizontal":
                clicked = pygame.image.load("./assets/image/button_horizontal_p.png")
                self.window.blit(clicked, (0, 360))

            elif self.phase == "deploy_vertical":
                clicked = pygame.image.load("./assets/image/button_vertical_p.png")
                self.window.blit(clicked, (160, 360))

            for water in self.terrain:
                water.update()

            for line in lines:
                line.render()

            if len(self.hit) != 0:
                for h in self.hit:
                    h.render()

            if len(self.ships) != 0:
                for ship in self.ships:
                    ship.render()

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    g = Game()
    g.run()