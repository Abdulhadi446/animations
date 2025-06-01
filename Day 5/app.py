import numpy as np
from manim import *
import os

class RollerCoasterSmooth(MovingCameraScene):
    def construct(self):
        # ───────────────────────────────
        # Track Size Setting
        # ───────────────────────────────
        track_size = 4.0  # ← Bigger value = longer & faster track
        t_start = 0.0
        t_end = track_size * 6 * np.pi
        num_points = int(200 * track_size)
        ts = np.linspace(t_start, t_end, num_points)

        scale_factor = 1.5 * track_size

        num_bumps = int(8 * track_size)
        bump_centers = np.random.uniform(t_start, t_end, size=num_bumps)
        bump_heights = np.random.uniform(0.2, 0.4, size=num_bumps)
        bump_sigmas = np.random.uniform(0.5, 1.0, size=num_bumps)

        base_wave = np.zeros_like(ts)
        for center, height, sigma in zip(bump_centers, bump_heights, bump_sigmas):
            base_wave += height * np.exp(-((ts - center) ** 2) / (2 * sigma ** 2))
        base_wave -= np.mean(base_wave)
        base_wave *= scale_factor

        noise_amplitude = 0.05
        raw_noise = noise_amplitude * (np.random.rand(num_points) - 0.5)

        def smooth_noise(noise, window_size=11):
            kernel = np.ones(window_size) / window_size
            return np.convolve(noise, kernel, mode="same")

        noise = smooth_noise(raw_noise, window_size=11)
        noisy_wave = base_wave + noise * scale_factor

        def noisy_wave_func(t):
            t_clamped = np.clip(t, t_start, t_end)
            y_interp = np.interp(t_clamped, ts, noisy_wave)
            return np.array([t_clamped * scale_factor, y_interp, 0.0])

        def safe_tangent(t, delta=1e-3):
            t_fwd = np.clip(t + delta, t_start, t_end)
            t_bwd = np.clip(t - delta, t_start, t_end)
            p_fwd = noisy_wave_func(t_fwd)
            p_bwd = noisy_wave_func(t_bwd)
            vec = p_fwd - p_bwd
            norm = np.linalg.norm(vec)
            if norm <= 1e-8:
                return np.array([1.0, 0.0, 0.0])
            return vec / norm

        def create_rail(offset):
            def param(t):
                center_pt = noisy_wave_func(t)
                tangent = safe_tangent(t)
                normal = np.array([-tangent[1], tangent[0], 0.0])
                return center_pt + offset * normal
            return ParametricFunction(
                param, t_range=[t_start, t_end], color=GRAY, stroke_width=2
            )

        left_rail = create_rail(0.05 * scale_factor)
        right_rail = create_rail(-0.05 * scale_factor)
        self.add(left_rail, right_rail)

        sleepers = VGroup()
        num_sleepers = int(60 * track_size)
        for i in range(num_sleepers + 1):
            t_i = t_start + (t_end - t_start) * i / num_sleepers
            center_pt = noisy_wave_func(t_i)
            tangent = safe_tangent(t_i)
            normal = np.array([-tangent[1], tangent[0], 0.0])

            sleeper_length = 0.12 * scale_factor
            start_pt = center_pt - normal * (sleeper_length / 2)
            end_pt = center_pt + normal * (sleeper_length / 2)
            sleeper = Line(start=start_pt, end=end_pt, color=BLUE, stroke_width=3)
            sleepers.add(sleeper)
        self.add(sleepers)

        try:
            cart = SVGMobject("cart.svg").scale(0.5 * scale_factor)
        except Exception:
            cart = Square(color=RED).scale(0.5 * scale_factor)

        cart.move_to(noisy_wave_func(t_start))
        cart.current_angle = 0.0
        self.add(cart)

        self.add(self.camera.frame)
        self.camera.frame.add_updater(lambda cam: cam.move_to(cart.get_center()))

        def update_cart(mob, alpha):
            t = t_start + alpha * (t_end - t_start)
            pt = noisy_wave_func(t)
            tangent = safe_tangent(t)
            normal = np.array([-tangent[1], tangent[0], 0.0])

            height_offset = 0.55 * scale_factor
            mob.move_to(pt + height_offset * normal)

            angle = np.arctan2(tangent[1], tangent[0])
            rotation_amount = angle - mob.current_angle
            mob.rotate(rotation_amount)
            mob.current_angle = angle

        # ───────────────────────────────
        # Play Sound on Loop (Repeated)
        # ───────────────────────────────
        sound_file = "cavesound.wav"
        sound_duration = 10  # seconds (adjust to real length of your sound)
        total_runtime = 59

        overlap = 0.1  # seconds, increase for more seamless playback
        for i in np.arange(0, total_runtime, sound_duration - overlap):
            self.add_sound(sound_file, time_offset=i)

        self.play(

            UpdateFromAlphaFunc(cart, update_cart),
            run_time=total_runtime,
            rate_func=linear,
        )

        self.camera.frame.clear_updaters()
        self.wait(0.7)

if __name__ == "__main__":
    os.system("manim -pql app.py RollerCoasterSmooth")