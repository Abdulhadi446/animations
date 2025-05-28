from manim import *
import random

class FallingSandGridWithSoundNoOverlap(Scene):
    def construct(self):
        title = Text(f"Falling{" "*15}Sand.", font_size=48).to_edge(UP)
        self.add(title)

        width = 80
        height = 60
        grain_radius = 0.07
        cell_size = grain_radius * 2
        max_grains = 2000

        grid = [[False for _ in range(height)] for _ in range(width)]
        grains_group = VGroup()
        self.add(grains_group)

        def grid_to_coord(x, y):
            return np.array([
                (x - width / 2) * cell_size,
                (y - height / 2) * cell_size,
                0
            ])

        def move_grain(x, y):
            if y == 0:
                return x, y
            if not grid[x][y-1]:
                return x, y-1
            if x > 0 and not grid[x-1][y-1]:
                return x-1, y-1
            if x < width - 1 and not grid[x+1][y-1]:
                return x+1, y-1
            return x, y

        grains = []

        def add_grain():
            x = random.randint(width//2 - 5, width//2 + 5)
            y = height - 1
            if grid[x][y]:
                return False
            dot = Dot(radius=grain_radius, color=YELLOW)
            dot.move_to(grid_to_coord(x, y))
            grains.append({'x': x, 'y': y, 'dot': dot})
            grains_group.add(dot)
            grid[x][y] = True
            return True

        # Sound control variables
        sound_path = "sandfall.wav"
        sound_duration = 2  # duration in seconds of sandfall.wav (adjust to your file)
        time_since_last_sound = sound_duration  # start ready to play immediately

        def update_grains(mob, dt):
            nonlocal time_since_last_sound
            grains_added_this_frame = 0

            for _ in range(10):
                if len(grains) < max_grains and add_grain():
                    grains_added_this_frame += 1

            time_since_last_sound += dt

            if grains_added_this_frame > 0 and time_since_last_sound >= sound_duration:
                self.add_sound(sound_path, time_offset=0)
                time_since_last_sound = 0

            for grain in grains:
                x, y = grain['x'], grain['y']
                new_x, new_y = move_grain(x, y)
                if (new_x, new_y) != (x, y):
                    grid[x][y] = False
                    grid[new_x][new_y] = True
                    grain['x'], grain['y'] = new_x, new_y
                    grain['dot'].move_to(grid_to_coord(new_x, new_y))

        grains_group.add_updater(update_grains)
        self.wait(10)
        grains_group.remove_updater(update_grains)
            
if __name__ == "__main__":
    import os
    os.system("python -m manim -pql app.py")