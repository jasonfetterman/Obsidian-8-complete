import time
import math


class SensorFusion:
    def __init__(self):
        # State vector
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0  # heading (rad)

        self.vx = 0.0
        self.vy = 0.0

        self.last_time = time.time()

        # Sensor inputs (latest)
        self.imu_data = None
        self.gps_data = None
        self.encoder_data = None

        # Tuning
        self.alpha_pos = 0.6
        self.alpha_vel = 0.5
        self.alpha_heading = 0.7

    # =========================
    # SENSOR INPUT METHODS
    # =========================
    def update_imu(self, imu):
        """
        imu = {
            'ax': float,
            'ay': float,
            'gyro_z': float
        }
        """
        self.imu_data = imu

    def update_gps(self, gps):
        """
        gps = {
            'x': float,
            'y': float
        }
        """
        self.gps_data = gps

    def update_encoders(self, enc):
        """
        enc = {
            'vx': float,
            'vy': float
        }
        """
        self.encoder_data = enc

    # =========================
    # MAIN UPDATE LOOP
    # =========================
    def update(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        if dt <= 0:
            return

        # ---- IMU INTEGRATION ----
        if self.imu_data:
            ax = self.imu_data.get('ax', 0)
            ay = self.imu_data.get('ay', 0)
            gyro = self.imu_data.get('gyro_z', 0)

            # integrate velocity
            self.vx += ax * dt
            self.vy += ay * dt

            # integrate heading
            self.theta += gyro * dt

        # ---- ENCODER FUSION ----
        if self.encoder_data:
            evx = self.encoder_data.get('vx', 0)
            evy = self.encoder_data.get('vy', 0)

            self.vx = self.alpha_vel * evx + (1 - self.alpha_vel) * self.vx
            self.vy = self.alpha_vel * evy + (1 - self.alpha_vel) * self.vy

        # ---- POSITION PREDICTION ----
        self.x += self.vx * dt
        self.y += self.vy * dt

        # ---- GPS CORRECTION ----
        if self.gps_data:
            gx = self.gps_data.get('x', self.x)
            gy = self.gps_data.get('y', self.y)

            self.x = self.alpha_pos * gx + (1 - self.alpha_pos) * self.x
            self.y = self.alpha_pos * gy + (1 - self.alpha_pos) * self.y

        # Normalize heading
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))

    # =========================
    # OUTPUT STATE
    # =========================
    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
            "theta": self.theta,
            "vx": self.vx,
            "vy": self.vy,
            "timestamp": time.time()
        }
