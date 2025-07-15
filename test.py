import pygame
import random
import time
import threading

# Constants
WIN_WIDTH, WIN_HEIGHT = 1000, 600
NUM_COLUMNS = 5
PANEL_WIDTH = WIN_WIDTH // NUM_COLUMNS
PANEL_HEIGHT = WIN_HEIGHT // 2
BAR_COUNT = 100
FONT_SIZE = 16

algo_names = [
    "Bubble", "Selection", "Insertion", "Merge", "Quick",
    "Heap", "Radix", "Shell", "Tim", "Counting"
]

sort_times = [0] * 10  # time taken by each algorithm

# Generate a shared input array
def get_input_array():
    return [random.randint(10, 1000) for _ in range(BAR_COUNT)]

# Draw bars in each panel
def draw_bars_panel(surface, arr, x_offset, y_offset, width, height, name, highlight_indices=None):
    pygame.draw.rect(surface, (20, 20, 20), (0, 0, width, height))
    max_height = max(arr)
    num_bars = min(len(arr), width // 4)
    step = len(arr) // num_bars
    display_arr = arr[::step][:num_bars]
    bar_width = width // num_bars
    spacing = 1

    for i, h in enumerate(display_arr):
        norm_height = int((h / max_height) * (height - 30))
        x = i * bar_width + spacing
        y = height - norm_height - 20
        color = (255, 255, 255) if highlight_indices and i in highlight_indices else (0, 255, 0)
        pygame.draw.rect(surface, color, (x, y, bar_width - spacing, norm_height))

    font = pygame.font.SysFont(None, FONT_SIZE)
    idx = algo_names.index(name)
    label = f"{name} ({sort_times[idx]:.2f}s)" if sort_times[idx] > 0 else name
    text = font.render(label, True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height - 10))
    surface.blit(text, text_rect)


# Sorting functions with visualization and timing
def timed_sort(sort_fn, arr, update_fn, idx):
    start = time.time()
    sort_fn(arr, update_fn)
    sort_times[idx] = time.time() - start

# Sorting algorithm definitions

def bubble_sort(arr, update):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                update(j, j + 1)

def selection_sort(arr, update):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        update(i, min_idx)

def insertion_sort(arr, update):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            update(j + 1, j)
            j -= 1
        arr[j + 1] = key
        update(j + 1, i)

def merge_sort(arr, update):
    def merge(l, r, left, right):
        i = j = 0
        for k in range(left, right):
            if j >= len(r) or (i < len(l) and l[i] < r[j]):
                arr[k] = l[i]
                update(k, k)
                i += 1
            else:
                arr[k] = r[j]
                update(k, k)
                j += 1

    def merge_rec(left, right):
        if left < right:
            mid = (left + right) // 2
            merge_rec(left, mid)
            merge_rec(mid + 1, right)
            merge(arr[left:mid + 1], arr[mid + 1:right + 1], left, right + 1)

    merge_rec(0, len(arr) - 1)

def quick_sort(arr, update):
    def quick(low, high):
        if low < high:
            pi = partition(low, high)
            quick(low, pi - 1)
            quick(pi + 1, high)

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                update(i, j)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        update(i + 1, high)
        return i + 1

    quick(0, len(arr) - 1)

def heap_sort(arr, update):
    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            update(i, largest)
            heapify(n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        update(0, i)
        heapify(i, 0)

def radix_sort(arr, update):
    def counting_sort(exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        for i in range(n):
            idx = (arr[i] // exp) % 10
            count[idx] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in range(n - 1, -1, -1):
            idx = (arr[i] // exp) % 10
            output[count[idx] - 1] = arr[i]
            count[idx] -= 1
        for i in range(n):
            arr[i] = output[i]
            update(i, i)

    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort(exp)
        exp *= 10

def shell_sort(arr, update):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                update(j, j - gap)
                j -= gap
            arr[j] = temp
            update(j, i)
        gap //= 2

def tim_sort(arr, update):
    arr.sort()
    for i in range(len(arr)):
        update(i, i)

def counting_sort(arr, update):
    if not arr:
        return
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    idx = 0
    for i, c in enumerate(count):
        while c > 0:
            arr[idx] = i
            update(idx, idx)
            idx += 1
            c -= 1

# Main Function
def main():
    base_array = get_input_array()
    arrays = [base_array.copy() for _ in range(10)]
    sort_funcs = [
        bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort,
        heap_sort, radix_sort, shell_sort, tim_sort, counting_sort
    ]

    pygame.init()
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Sorting Visualizer.")
    running = True
    sorting_started = False
    threads = []

    # Pre-create surfaces for each panel
    panels = [pygame.Surface((PANEL_WIDTH, PANEL_HEIGHT)) for _ in range(10)]

    def make_update(arr, idx):
        def update(i, j):
            draw_bars_panel(
                panels[idx], arr,
                0, 0,
                PANEL_WIDTH, PANEL_HEIGHT,
                algo_names[idx],
                highlight_indices=[i % len(arr)]
            )
            window.blit(panels[idx], ((idx % 5) * PANEL_WIDTH, (idx // 5) * PANEL_HEIGHT))
            draw_separators(window)
            pygame.display.update(pygame.Rect((idx % 5) * PANEL_WIDTH, (idx // 5) * PANEL_HEIGHT, PANEL_WIDTH, PANEL_HEIGHT))
            pygame.time.delay(5)
        return update

    def draw_separators(surface):
        for i in range(1, 5):
            pygame.draw.line(surface, (255, 255, 255), (i * PANEL_WIDTH, 0), (i * PANEL_WIDTH, WIN_HEIGHT), 2)
        pygame.draw.line(surface, (255, 255, 255), (0, PANEL_HEIGHT), (WIN_WIDTH, PANEL_HEIGHT), 2)
    sorting_completed = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and not sorting_started:
                    sorting_started = True
                    for i in range(10):
                        update_fn = make_update(arrays[i], i)
                        t = threading.Thread(target=timed_sort, args=(sort_funcs[i], arrays[i], update_fn, i))
                        threads.append(t)
                        t.start()

        if  sorting_started and all(not t.is_alive() for t in threads)and not sorting_completed:
            for i in range(10):
                draw_bars_panel(panels[i], arrays[i], 0, 0, PANEL_WIDTH, PANEL_HEIGHT, algo_names[i])
                window.blit(panels[i], ((i % 5) * PANEL_WIDTH, (i // 5) * PANEL_HEIGHT))
            draw_separators(window)
            pygame.display.update() 
            sorting_completed = True

    pygame.quit()

if __name__ == "__main__":
    main()
