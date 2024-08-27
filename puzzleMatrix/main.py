from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import time
from PIL import Image, ImageEnhance, ImageFilter
import heapq


def MoveToTile(pos):
    match pos:
        case '1':
            img1 = pyautogui.locateOnScreen(r"Poze\1.PNG", confidence=0.8)
            pyautogui.moveTo(pyautogui.center(img1), duration=0.5)
            print("1")
        case '2':
            img1 = pyautogui.locateOnScreen(r"Poze\2.PNG", confidence=0.68, grayscale=True)
            pyautogui.moveTo(pyautogui.center(img1), duration=0.5)
            print("2")
        case '3':
            img1 = pyautogui.locateOnScreen(r"Poze\3.PNG", confidence=0.78, grayscale=True)
            pyautogui.moveTo(pyautogui.center(img1), duration=0.5)
            print("3")
        case '4':
            img1 = pyautogui.locateOnScreen(r"Poze\4.PNG", confidence=0.8)
            pyautogui.moveTo(pyautogui.center(img1), duration=0.5)
            print("4")
        case '5':
            img1 = pyautogui.locateOnScreen(r"Poze\5.PNG", confidence=0.78, grayscale=True)
            pyautogui.moveTo(pyautogui.center(img1), duration=0.5)
            print("5")
        case '6':
            img1 = pyautogui.locateOnScreen(r"Poze\6.PNG", confidence=0.70, grayscale=True)
            pyautogui.moveTo(pyautogui.center(img1), duration=0.5)
            print("6")
        case '7':
            img1 = pyautogui.locateOnScreen(r"Poze\7.PNG", confidence=0.76)
            pyautogui.moveTo(pyautogui.center(img1), duration=0.5)
            print("7")
        case '8':
            img1 = pyautogui.locateOnScreen(r"Poze\8.PNG", confidence=0.75, grayscale=True)
            pyautogui.moveTo(pyautogui.center(img1), duration=0.5)
            print("8")

def modifice_lista(lst):
    result = []
    i = 0
    n = len(lst)

    while i < n:
        # Verificăm dacă 'x' este la început sau la sfârșit
        if lst[i] == 'x':
            if i == 0 or i == n - 1:
                # Ignorăm 'x' la început sau la sfârșit
                i += 1
                continue

            # Verificăm dacă 'x' este între două numere
            if i > 0 and i < n - 1 and lst[i - 1].isdigit() and lst[i + 1].isdigit():
                # Ignorăm acest 'x'
                i += 1
                continue

            # Verificăm dacă 'x' este consecutiv cu alt 'x'
            elif i > 0 and lst[i - 1] == 'x':
                # Ignorăm acest 'x' și continuăm
                i += 1
                continue
            else:
                # Dacă 'x' nu este între două numere și nu este consecutiv, îl adăugăm în rezultat
                result.append(lst[i])
        else:
            # Adăugăm numerele în rezultat
            result.append(lst[i])
        i += 1

    return result

def lista_in_matrice(lista):
    if len(lista) != 9:
        raise ValueError("Lista trebuie să conțină exact 9 elemente.")

    matrice = [lista[i:i + 3] for i in range(0, 9, 3)]
    return matrice

# Funcția care calculează distanța Manhattan
def manhattan_distance(state):
    distance = 0
    goal = {'1': (0, 0), '2': (0, 1), '3': (0, 2), '4': (1, 0), '5': (1, 1), '6': (1, 2), '7': (2, 0), '8': (2, 1),
            'x': (2, 2)}
    for r, row in enumerate(state):
        for c, val in enumerate(row):
            if val != 'x':
                goal_r, goal_c = goal[val]
                distance += abs(goal_r - r) + abs(goal_c - c)
    return distance

# Funcția pentru a genera toate mișcările posibile
def get_neighbors(state):
    neighbors = []
    rows, cols = len(state), len(state[0])
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    # Găsește poziția spațiului liber
    empty_r, empty_c = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 'x')

    for direction, (dr, dc) in directions.items():
        new_r, new_c = empty_r + dr, empty_c + dc
        if 0 <= new_r < rows and 0 <= new_c < cols:
            new_state = [row[:] for row in state]
            new_state[empty_r][empty_c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[empty_r][empty_c]
            neighbors.append((new_state, direction))

    return neighbors

# Algoritmul A*
def astar(start):
    goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', 'x']]
    if start == goal:
        return []

    open_list = []
    heapq.heappush(open_list, (0 + manhattan_distance(start), 0, start, []))
    closed_set = set()

    while open_list:
        _, g, current, path = heapq.heappop(open_list)

        if current == goal:
            return path

        # Convert current state to tuple for immutability in the closed set
        current_tuple = tuple(tuple(row) for row in current)
        closed_set.add(current_tuple)

        for neighbor, move in get_neighbors(current):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            if neighbor_tuple not in closed_set:
                heapq.heappush(open_list, (g + 1 + manhattan_distance(neighbor), g + 1, neighbor, path + [move]))

    return None

def apply_moves(initial_state, moves):
    state = [row[:] for row in initial_state]
    rows, cols = len(state), len(state[0])

    # Găsește poziția inițială a spațiului liber
    empty_r, empty_c = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 'x')

    for move in moves:
        if move == 'up':
            new_r, new_c = empty_r - 1, empty_c
            print("new r:",new_r,"new_c:",new_c)
            print(state[new_r][new_c])
            MoveToTile(state[new_r][new_c])
            pyautogui.click()
        elif move == 'down':
            new_r, new_c = empty_r + 1, empty_c
            print("new r:", new_r, "new_c:", new_c)
            print(state[new_r][new_c])
            MoveToTile(state[new_r][new_c])
            pyautogui.click()

        elif move == 'left':
            new_r, new_c = empty_r, empty_c - 1
            print("new r:", new_r, "new_c:", new_c)
            print(state[new_r][new_c])
            MoveToTile(state[new_r][new_c])
            pyautogui.click()

        elif move == 'right':
            new_r, new_c = empty_r, empty_c + 1
            print("new r:", new_r, "new_c:", new_c)
            print(state[new_r][new_c])
            MoveToTile(state[new_r][new_c])
            pyautogui.click()



        # Aplică mișcarea
        if 0 <= new_r < rows and 0 <= new_c < cols:
            # Swap spațiul liber cu piesa la noua poziție
            state[empty_r][empty_c], state[new_r][new_c] = state[new_r][new_c], state[empty_r][empty_c]
            empty_r, empty_c = new_r, new_c

        # Afișează starea curentă
        for row in state:
            print(row)
        print("------------------------------")

    return state


def MoveTo_1():
    img1 = pyautogui.locateOnScreen(r"Poze\1.PNG", confidence=0.8)
    pyautogui.moveTo(pyautogui.center(img1), duration=0.5)

def MoveTo_2():
    img1 = pyautogui.locateOnScreen(r"Poze\2.PNG", confidence=0.68,grayscale=True)
    pyautogui.moveTo(pyautogui.center(img1), duration=0.5)

def MoveTo_3():
    # Deschide și preprocesează imaginea pentru a îmbunătăți OCR-ul
    img = Image.open(r"Poze\3.PNG")
    img = img.convert('L')  # Conversie la alb-negru
    img = img.filter(ImageFilter.SHARPEN)  # Mărește claritatea
    img.save(r"Poze\3p.PNG")

    img1 = pyautogui.locateOnScreen(r"Poze\3.PNG", confidence=0.78,grayscale=True)
    pyautogui.moveTo(pyautogui.center(img1), duration=0.5)

def MoveTo_4():
    img1 = pyautogui.locateOnScreen(r"Poze\4.PNG", confidence=0.8)
    pyautogui.moveTo(pyautogui.center(img1), duration=0.5)

def MoveTo_5():
    # Deschide și preprocesează imaginea pentru a îmbunătăți OCR-ul
    img = Image.open(r"Poze\5.PNG")
    img = img.convert('L')  # Conversie la alb-negru
    img = img.filter(ImageFilter.SHARPEN)  # Mărește claritatea
    img.save(r"Poze\5p.PNG")

    img1 = pyautogui.locateOnScreen(r"Poze\5.PNG", confidence=0.78,grayscale=True)
    pyautogui.moveTo(pyautogui.center(img1), duration=0.5)

def MoveTo_6():
    # Deschide și preprocesează imaginea pentru a îmbunătăți OCR-ul
    img = Image.open(r"Poze\6.PNG")
    img = img.convert('L')  # Conversie la alb-negru
    img = img.filter(ImageFilter.SHARPEN)  # Mărește claritatea
    img.save(r"Poze\6p.PNG")

    img1 = pyautogui.locateOnScreen(r"Poze\6.PNG", confidence=0.70, grayscale=True)
    pyautogui.moveTo(pyautogui.center(img1), duration=0.5)

def MoveTo_7():
    img1 = pyautogui.locateOnScreen(r"Poze\7.PNG", confidence=0.76)
    pyautogui.moveTo(pyautogui.center(img1), duration=0.5)

def MoveTo_8():
    # Deschide și preprocesează imaginea pentru a îmbunătăți OCR-ul
    img = Image.open(r"Poze\8.PNG")
    img = img.convert('L')  # Conversie la alb-negru
    img = img.filter(ImageFilter.SHARPEN)  # Mărește claritatea
    img.save(r"Poze\8p.PNG")

    img1 = pyautogui.locateOnScreen(r"Poze\8.PNG", confidence=0.75,grayscale=True)
    pyautogui.moveTo(pyautogui.center(img1), duration=0.5)


# Inițializează WebDriver (Chrome în acest caz)
driver = webdriver.Chrome()

# Deschide pagina URL
url = 'https://bing.com/spotlight/imagepuzzle'
driver.get(url)

# Așteaptă puțin pentru a te asigura că pagina și scripturile s-au încărcat complet
time.sleep(3)  # Poți ajusta timpul în funcție de viteza conexiunii

# setgoogle as default
ggl_sel = pyautogui.locateOnScreen(r"Poze\Google_logo.png", confidence=0.7)
pyautogui.click(pyautogui.moveTo(pyautogui.center(ggl_sel), duration=1))
setDef = pyautogui.locateOnScreen(r"Poze\SetAsDefault.png")
pyautogui.click(pyautogui.moveTo(pyautogui.center(setDef), duration=1))
pyautogui.hotkey('winleft', 'up') #fullscreen
pyautogui.hotkey('ctrl', '+') #zoom in
time.sleep(5) #nu stiu inca daca sa il tin

# Găsește toate elementele tile
tiles = driver.find_elements(By.CLASS_NAME, 'tile')
board = driver.find_elements(By.ID, 'board')

# Inițializează o listă pentru a stoca datele extrase
tile_data = []

# Iterează prin fiecare element tile
for tile in tiles:
    try:
        # Găsește elementul tileNumber care este un copil al tile-ului curent
        tile_number_elements = tile.find_elements(By.CSS_SELECTOR, '.parentTile .tileNumber')

        if tile_number_elements:
            for tile_number_element in tile_number_elements:
                tile_number = tile_number_element.text.strip()
                tile_data.append(tile_number)
        else:
            # Dacă tileNumber nu există în acest tile, adaugă 'x'
            tile_data.append('x')

    except Exception as e:
        print(f"Eroare la procesarea tile-ului: {e}")
        tile_data.append('x')

tile_data = modifice_lista(tile_data)

tile_matrix = lista_in_matrice(tile_data)


print("Matrice initiala:")
for row in tile_matrix:
    print(row)

solutie = astar(tile_matrix)
print(solutie)
final_state = apply_moves(tile_matrix, solutie)



# Închide browser-ul
driver.quit()
