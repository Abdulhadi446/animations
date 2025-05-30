from manim import *
import numpy as np
import colorsys
import random
import os

class BouncingBallInCircle(Scene):
    def construct(self):
        radius = 3
        ball_radius = 0.05

        # Create circular boundary
        boundary = Circle(radius=radius, color=RED)
        self.add(boundary)

        # Create the ball using a small Circle with fill for visibility
        ball = Circle(radius=ball_radius, color=RED, fill_opacity=1)
        ball.move_to(RIGHT * 2)
        self.add(ball)

        # Initial velocity vector
        velocity = np.array([2.0, 1.5, 0.0])  # x, y, z

        # Initial hue for color cycling
        hue = random.random()

        # Trail dots group
        trail_dots = VGroup()
        self.add(trail_dots)

        # Sound file path
        bounce_sound_path = "bounce.wav"

        # Track the current radius for scaling and collision detection
        current_radius = ball_radius

        def update_ball(mob, dt):
            nonlocal velocity, hue, current_radius

            pos = mob.get_center()
            new_pos = pos + velocity * dt

            dist = np.linalg.norm(new_pos)
            if dist + current_radius >= radius:
                normal = new_pos / dist
                velocity -= 2 * np.dot(velocity, normal) * normal

                # Scale up the ball size by 10%
                scale_factor = 1.1
                mob.scale(scale_factor)
                current_radius *= scale_factor

                # Increase speed proportional to size increase
                velocity *= scale_factor

                # Correct position to be inside the boundary
                new_pos = normal * (radius - current_radius)

                if os.path.exists(bounce_sound_path):
                    self.add_sound(bounce_sound_path)

            # Update color cycling
            hue = (hue + dt * 0.5) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 1.0)
            color = rgb_to_color([r, g, b])
            mob.set_fill(color, opacity=1)

            # Move ball to updated position
            mob.move_to(new_pos)

            # Add trail dot at previous position with current color
            trail_dot = Circle(radius=current_radius * 0.7, fill_opacity=0.4, stroke_opacity=0)
            trail_dot.set_fill(color, opacity=0.4)
            trail_dot.move_to(pos)
            trail_dots.add(trail_dot)

            # Limit number of trail dots to keep scene manageable
            if len(trail_dots) > 150:
                oldest = trail_dots[0]
                trail_dots.remove(oldest)
                self.remove(oldest)

        ball.add_updater(update_ball)

        self.wait(59)
        ball.remove_updater(update_ball)


if __name__ == "__main__":
    import os
    os.system("manim -pql app.py BouncingBallInCircle")