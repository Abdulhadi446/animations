from manim import *
import random

# Generate a fully random RGB color
def random_rgb_color():
    r = random.random()
    g = random.random()
    b = random.random()
    return rgb_to_color([r, g, b])

class UprightRGBPipeSort(Scene):
    def construct(self):
        anim_speed = 4.0  # 👈 Higher = faster and more bars

        # Adjust settings based on anim_speed
        base_num_pipes = 10
        base_max_height = 5
        base_pipe_width = 0.4
        base_sort_speed = 0.4  # slowest animation time

        num_pipes = int(base_num_pipes * anim_speed)
        max_height = base_max_height
        pipe_width = base_pipe_width / anim_speed
        sort_speed = base_sort_speed / anim_speed

        # Add title text
        title = Text("Bubble Sort", font_size=36)
        title.to_edge(UP)
        self.play(FadeIn(title))
        self.wait(0.5)

        # Generate pipes
        heights = [random.uniform(1, max_height) for _ in range(num_pipes)]
        colors = [random_rgb_color() for _ in range(num_pipes)]
        pipes = []

        for i, (h, color) in enumerate(zip(heights, colors)):
            pipe = Rectangle(width=pipe_width, height=h, color=color, fill_color=color, fill_opacity=1)
            spacing = pipe_width + 0.05
            x_pos = i * spacing - num_pipes * spacing / 2
            pipe.move_to([x_pos, h / 2 - 3, 0])
            pipes.append(pipe)

        self.play(*[FadeIn(p) for p in pipes], run_time=0.5)
        self.wait(0.5)

        # Bubble Sort animation
        for i in range(num_pipes):
            for j in range(num_pipes - i - 1):
                if pipes[j].height > pipes[j + 1].height:
                    self.play(
                        pipes[j].animate.shift((pipe_width + 0.05) * RIGHT),
                        pipes[j + 1].animate.shift((pipe_width + 0.05) * LEFT),
                        run_time=sort_speed
                    )
                    pipes[j], pipes[j + 1] = pipes[j + 1], pipes[j]

        self.wait(1)
        # Finalize the scene
if __name__ == "__main__":
    import os
    os.system("python -m manim -pql app.py")