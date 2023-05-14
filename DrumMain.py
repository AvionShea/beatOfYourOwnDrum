import pygame
from pygame import mixer
# intilizing imports
pygame.init()

# ------ VARIABLE LIBRARY ------

# window dimension
WIDTH = 1400
HEIGHT = 800

# preset app colors
background = pygame.Color("#4D6D9A")
active_box = pygame.Color("#EDB5BF")
lines = pygame.Color("#99CED3")
standard_box = pygame.Color("#86b3d1")
active_play = pygame.Color("#439F76")
white = (255, 255, 255)
black = (0, 0, 0)
grey = (50, 50, 50)


# screen creation
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Drummer's Dream")
label_font = pygame.font.Font("ArianaVioleta.ttf", 50)  # number is font size
secondary_font = pygame.font.Font("Cabal.ttf", 28)
medium_font = pygame.font.Font("Cabal.ttf", 19)

index = 100
# framerate
fps = 60
# timer for game
timer = pygame.time.Clock()
# beats
beats = 8
# instruments rows
instruments = 6
# boxes
boxes = []
# clicked list
# -1 not selected, 1 is selected
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_instruments = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True
save_menu = False
load_menu = False
saved_beats = []
file = open("saved_beats.txt", "r")  # open and stores files
for line in file:
    saved_beats.append(line)

beat_name = ""
typing = False

# Sound Kit
hi_hat = mixer.Sound("sounds\hi hat.wav")
snare = mixer.Sound("sounds\snare.wav")
kick = mixer.Sound("sounds\kick.wav")
crash = mixer.Sound("sounds\crash.wav")
clap = mixer.Sound("sounds\clap.wav")
tom = mixer.Sound("sounds\\tom.wav")
pygame.mixer.set_num_channels(instruments * 10)

# --- END OF VARIABLE LIBRARY ---


# plays sounds kit
def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_instruments[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_grid(clicks, beat, actives):
    boxes = []
    left_box = pygame.draw.rect(
        screen, standard_box, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(
        screen, standard_box, [0, HEIGHT - 200, WIDTH, 200], 5)  # user options
    # drawing lines to seperate text in left_box
    for i in range(instruments):
        pygame.draw.line(screen, standard_box, (0, (i * 100) +
                         100), (200, (i * 100) + 100), 3)
    colors = [black, lines, black]
    hi_hat_text = label_font.render(
        "Hi Hat", True, colors[actives[0]])  # hi hat option
    screen.blit(hi_hat_text, (30, 30))  # drawing on screen
    snare_text = label_font.render(
        "Snare ", True, colors[actives[1]])  # Snare option
    screen.blit(snare_text, (30, 130))  # drawing on screen
    kick_text = label_font.render(
        "Bass Drum", True, colors[actives[2]])  # kick option
    screen.blit(kick_text, (30, 230))  # drawing on screen
    crash_text = label_font.render(
        "Crash", True, colors[actives[3]])  # crash option
    screen.blit(crash_text, (30, 330))  # drawing on screen
    clap_text = label_font.render(
        "Clap", True, colors[actives[4]])  # clap option
    screen.blit(clap_text, (30, 430))  # drawing on screen
    floor_text = label_font.render(
        "Floor Tom", True, colors[actives[5]])  # floor tom option
    screen.blit(floor_text, (30, 530))  # drawing on screen

    # boxes for beats
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = standard_box
            else:
                if actives[j] == 1:
                    color = active_box
                else:
                    color = grey
            # floor division makes sure it's an int
            rect = pygame.draw.rect(screen, color, [
                                    i * ((WIDTH - 200) // beats) + 200, (j * 100) + 5, ((WIDTH - 200) // beats) - 10, ((HEIGHT - 200) // instruments) - 10], 0, 3)
            pygame.draw.rect(screen, standard_box, [
                i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, lines, [
                i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))
        active = pygame.draw.rect(screen, active_play, [
                                  beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100], 5, 3)

    return boxes


def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, background, [0, 0, WIDTH, HEIGHT])
    menu_text = secondary_font.render(
        "SAVE MENU: Enter Title for Current Beat", True, grey)
    screen.blit(menu_text, (455, 40))

    saving_button = pygame.draw.rect(
        screen, standard_box, [WIDTH // 2 - 200, HEIGHT * 0.75, 400, 100])
    saving_text = secondary_font.render("SAVE CURRENT BEAT", True, grey)
    screen.blit(saving_text, (WIDTH // 2 - 140, HEIGHT * 0.72 + 60))

    exit_control = pygame.draw.rect(
        screen, standard_box, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = secondary_font.render("Close", True, grey)
    screen.blit(exit_text, (WIDTH - 150, HEIGHT - 70))
    if typing:
        pygame.draw.rect(screen, active_box, [400, 200, 600, 200], 0, 5)
    entry_box = pygame.draw.rect(screen, lines, [400, 200, 600, 200], 5, 5)
    entry_text = secondary_font.render(f"{beat_name}", True, grey)
    screen.blit(entry_text, (430, 250))

    return exit_control, saving_button, entry_box


def draw_load_menu(index):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, background, [0, 0, WIDTH, HEIGHT])
    menu_text = secondary_font.render(
        "LOAD MENU: Select a Beat Title to Load", True, grey)
    screen.blit(menu_text, (455, 40))

    loading_button = pygame.draw.rect(
        screen, standard_box, [WIDTH // 2 - 200, HEIGHT * 0.85, 400, 100])
    loading_text = secondary_font.render("LOAD A BEAT", True, grey)
    screen.blit(loading_text, (WIDTH // 2 - 100, HEIGHT * 0.82 + 60))

    delete_button = pygame.draw.rect(
        screen, standard_box, [(WIDTH // 2) - 500, HEIGHT * 0.85, 200, 100], 0, 5)
    delete_text = secondary_font.render("Delete", True, grey)
    screen.blit(delete_text, ((WIDTH // 2) - 455, HEIGHT * 0.85 + 30))

    exit_control = pygame.draw.rect(
        screen, standard_box, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = secondary_font.render("Close", True, grey)
    screen.blit(exit_text, (WIDTH - 150, HEIGHT - 70))
    loaded_box = pygame.draw.rect(screen, lines, [190, 75, 1000, 600], 5, 5)
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, lines, [190, 100 + index * 50, 1000, 50])

    # shows saved beats on screen
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f"{beat + 1}", True, grey)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index("name: ") + 6
            name_index_end = saved_beats[beat].index(", beats:")
            name_text = medium_font.render(
                saved_beats[beat][name_index_start:name_index_end], True, grey)
            screen.blit(name_text, (240, 100 + beat * 50))
        # checks to see if actively selected beat
        if 0 <= index < len(saved_beats) and beat == index:
            beat_index_end = saved_beats[beat].index(", bpm:")
            loaded_beats = int(
                saved_beats[beat][name_index_end + 8: beat_index_end])
            bpm_index_end = saved_beats[beat].index(", selected:")
            loaded_bpm = int(
                saved_beats[beat][beat_index_end + 6: bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: - 3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(", "))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == "1" or loaded_clicks_row[item] == "-1":
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    return exit_control, loading_button, delete_button, loaded_box, loaded_info


# Main Game Loop
run = True
while run:
    timer.tick(fps)
    screen.fill(background)
    boxes = draw_grid(clicked, active_beat, active_instruments)
    # bottom menu buttons
    play_pause = pygame.draw.rect(
        screen, standard_box, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = secondary_font.render("Play/Pause", True, black)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render("Playing", True, grey)
    else:
        play_text2 = medium_font.render("Paused", True, grey)
    screen.blit(play_text2, (70, HEIGHT - 100))

    # BPM Rendering
    bpm_rect = pygame.draw.rect(screen, standard_box, [
                                300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render("Beats Per Minute", True, grey)
    screen.blit(bpm_text, (308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, grey)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(
        screen, standard_box, [510, HEIGHT - 150, 48, 48], 0, 5)  # adds bpm
    bpm_sub_rect = pygame.draw.rect(
        screen, standard_box, [510, HEIGHT - 100, 48, 48], 0, 5)  # subtact bpm
    add_text = medium_font.render("+10", True, grey)
    sub_text = medium_font.render("-10", True, grey)
    screen.blit(add_text, (520, HEIGHT - 140))
    screen.blit(sub_text, (520, HEIGHT - 90))

    # Beats Rendering
    beats_rect = pygame.draw.rect(screen, standard_box, [
        600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render("Beats In Loop", True, grey)
    screen.blit(beats_text, (628, HEIGHT - 130))
    beats_text2 = label_font.render(f'{beats}', True, grey)
    screen.blit(beats_text2, (690, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(
        screen, standard_box, [810, HEIGHT - 150, 48, 48], 0, 5)  # adds beats
    beats_sub_rect = pygame.draw.rect(
        screen, standard_box, [810, HEIGHT - 100, 48, 48], 0, 5)  # subtact beats
    add_text_beats = medium_font.render("+1", True, grey)
    sub_text_beats = medium_font.render("-1", True, grey)
    screen.blit(add_text_beats, (820, HEIGHT - 140))
    screen.blit(sub_text_beats, (820, HEIGHT - 90))

    # Turning off instruments
    instruments_rect = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instruments_rect.append(rect)

    # Save/Load Buttons
    save_button = pygame.draw.rect(
        screen, standard_box, [900, HEIGHT - 150, 200, 48], 0, 5)
    save_text = secondary_font.render(f'Save Beat', True, grey)
    load_button = pygame.draw.rect(
        screen, standard_box, [900, HEIGHT - 100, 200, 48], 0, 5)
    load_text = secondary_font.render(f'Load Beat', True, grey)
    screen.blit(save_text, (920, HEIGHT - 145))
    screen.blit(load_text, (920, HEIGHT - 95))

    # Clear Board Button
    clear_button = pygame.draw.rect(
        screen, standard_box, [1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = secondary_font.render(f"Clear Board", True, grey)
    screen.blit(clear_text, (1160, HEIGHT - 120))

    # Save and Load Menu
    if save_menu:
        exit_button, saving_button, entry_box = draw_save_menu(
            beat_name, typing)
    if load_menu:
        exit_button, loading_button, delete_button, loaded_box, loaded_info = draw_load_menu(
            index)

    if beat_changed:
        play_notes()
        beat_changed = False

    # Event Handeling - check movement of mouse, inputs, etc.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # checking for collison
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                # position mouse was when clicked
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            # add/subtract bpm intervals
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 10
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 10
            # add/subtract beats
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)  # adds item to clicked list

            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    # removing last item in clicked list(list function for removal) -- negative counts back from end of list
                    clicked[i].pop(-1)

            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)]
                           for _ in range(instruments)]

            elif save_button.collidepoint(event.pos):
                save_menu = True
                playing = False
            elif load_button.collidepoint(event.pos):
                load_menu = True
                playing = False

            for i in range(len(instruments_rect)):
                if instruments_rect[i].collidepoint(event.pos):
                    active_instruments[i] *= -1

        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ""
                typing = False
            if load_menu:
                if loaded_box.collidepoint(event.pos):
                    index = (event.pos[1] - 100) // 50
                if delete_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        beats = loaded_info[0]
                        bpm = loaded_info[1]
                        clicked = loaded_info[2]
                        index = 100
                        load_menu = False
            if save_menu:
                if entry_box.collidepoint(event.pos):
                    if typing:
                        typing = False
                    elif not typing:
                        typing = True
                if saving_button.collidepoint(event.pos):
                    file = open("saved_beats.txt", "w")
                    saved_beats.append(
                        f"\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}")
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    typing = False
                    beat_name = ""

        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]

    beat_length = (fps * 60) // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()
