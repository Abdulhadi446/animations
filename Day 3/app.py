from manim import *
import random
import numpy as np

class DroppingBallsWithSound(Scene):
    def construct(self):
        title = Text("Bouncing Balls with Sound", font_size=42).to_edge(UP)
        self.add(title)

        ball_radius = 0.2
        gravity = -10
        elasticity = 0.9

        floor_y = -3.5
        ceiling_y = 3.5
        left_x = -6.8
        right_x = 6.8

        balls = []
        balls_group = VGroup()
        self.add(balls_group)

        class Ball:
            def __init__(self, position):
                color = random_bright_color()
                self.circle = Circle(radius=ball_radius, color=color, fill_opacity=1).set_fill(color)
                self.circle.move_to(position)
                self.velocity = np.array([random.uniform(-1.0, 1.0), 0.0, 0.0])
                self.sound_cooldown = 0 ,  Cooldown timer for sound
                balls.append(self)

        def no_overlap_position():
            attempts = 20
            for _ in range(attempts):
                pos = np.array([
                    random.uniform(left_x + ball_radius, right_x - ball_radius),
                    ceiling_y - ball_radius,
                    0
                ])
                if all(np.linalg.norm(pos - b.circle.get_center()) >= 2 * ball_radius for b in balls):
                    return pos
            return None

        drop_interval = 0.4
        timer = 0.0

        def update_balls(mob, dt):
            nonlocal timer
            timer += dt

            if timer >= drop_interval:
                timer = 0.0
                spawn_pos = no_overlap_position()
                if spawn_pos is not None:
                    new_ball = Ball(spawn_pos)
                    balls_group.add(new_ball.circle)

            for ball in balls:
                ball.velocity[1] += gravity * dt
                pos = ball.circle.get_center()
                new_pos = pos + ball.velocity * dt

                played_sound = False

            ,  Floor bounce
                if new_pos[1] - ball_radius <= floor_y:
                    new_pos[1] = floor_y + ball_radius
                    ball.velocity[1] *= -elasticity
                    ball.velocity[0] += random.uniform(-0.5, 0.5)
                    played_sound = True

            ,  Ceiling bounce
                if new_pos[1] + ball_radius >= ceiling_y:
                    new_pos[1] = ceiling_y - ball_radius
                    ball.velocity[1] *= -elasticity
                    played_sound = True

            ,  Left wall
                if new_pos[0] - ball_radius <= left_x:
                    new_pos[0] = left_x + ball_radius
                    ball.velocity[0] *= -elasticity
                    played_sound = True

            ,  Right wall
                if new_pos[0] + ball_radius >= right_x:
                    new_pos[0] = right_x - ball_radius
                    ball.velocity[0] *= -elasticity
                    played_sound = True

                ball.circle.move_to(new_pos)

                if played_sound and ball.sound_cooldown <= 0:
                    self.add_sound("bounce.wav")
                    ball.sound_cooldown = 0.1 ,  Cooldown in seconds

                ball.sound_cooldown = max(0, ball.sound_cooldown - dt)

        ,  Ball-to-ball collisions
            for i in range(len(balls)):
                for j in range(i + 1, len(balls)):
                    b1 = balls[i]
                    b2 = balls[j]
                    p1 = b1.circle.get_center()
                    p2 = b2.circle.get_center()
                    delta = p1 - p2
                    dist = np.linalg.norm(delta)
                    if dist < 2 * ball_radius and dist != 0:
                        direction = delta / dist
                        overlap = 2 * ball_radius - dist
                        b1.circle.move_to(p1 + 0.5 * overlap * direction)
                        b2.circle.move_to(p2 - 0.5 * overlap * direction)

                        v1n = np.dot(b1.velocity, direction)
                        v2n = np.dot(b2.velocity, direction)
                        b1.velocity += (v2n - v1n) * direction
                        b2.velocity += (v1n - v2n) * direction

        balls_group.add_updater(update_balls)
        self.wait(59)
        balls_group.remove_updater(update_balls)

if __name__ == "__main__":
    import os
    os.system("manim -pql app.py DroppingBallsWithSound")
, , Manim, ManimAnimation, PythonAnimation, PhysicsSimulation, BouncingBalls, BallPhysics, CodingAnimation, Programming, MathAnimation, OpenSource, LearnToCode, PhysicsInPython, SoundEffects, CreativeCoding, ComputerGraphics, GameDev, VisualEffects, Simulation, Shorts