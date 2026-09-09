#!/usr/bin/env python3
"""
Guanxin Road Simulation - Teleop Vehicle Node
Controls Tesla Model Y driving, camera view switching, and origin teleportation.
"""

import os
import sys
import select
import subprocess
import termios
import tty
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

KEY_MAP = {
    'w': (1.5, 0.0),    # 前進加速
    's': (-1.5, 0.0),   # 倒車/減速
    'a': (0.0, 0.15),   # 左轉
    'd': (0.0, -0.15),  # 右轉
}

VIEW_CONFIGS = [
    {
        'name': '3rd Person (Chase Cam)',
        'topic': '/model_y/view_chase',
        'desc': '跟車俯角第三人稱視角'
    },
    {
        'name': '1st Person (Driver Seat)',
        'topic': '/model_y/view_driver',
        'desc': '駕駛座車內第一人稱視角'
    },
    {
        'name': '1st Person (Front Hood)',
        'topic': '/model_y/view_hood',
        'desc': '車鼻保桿前視視角'
    }
]

class TeleopVehicle(Node):
    def __init__(self):
        super().__init__('teleop_vehicle')
        self.pub_cmd = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()

        self.cur_view_idx = 0
        self.sub_img = None
        self.setup_camera_subscription()

        self.speed = 0.0
        self.steer = 0.0

        # 定時發布控制指令，確保模擬器物理連續運作
        self.timer = self.create_timer(0.05, self.publish_twist)  # 20 Hz

        self.get_logger().info("=" * 60)
        self.get_logger().info("Tesla Model Y Teleop Controller Initialized")
        self.get_logger().info("控制按鍵說明：")
        self.get_logger().info("  [W] 前進加速       [S] 倒車 / 減速")
        self.get_logger().info("  [A] 方向盤向左     [D] 方向盤向右")
        self.get_logger().info("  [Space] 緊急煞車   [V] 切換相機視角 (3種)")
        self.get_logger().info("  [O] 瞬移重設回原點 (光復關新路口)")
        self.get_logger().info("  [Q] 退出節點")
        self.get_logger().info("=" * 60)

    def setup_camera_subscription(self):
        if self.sub_img is not None:
            self.destroy_subscription(self.sub_img)
        cur_topic = VIEW_CONFIGS[self.cur_view_idx]['topic']
        self.sub_img = self.create_subscription(
            Image,
            cur_topic,
            self.on_image,
            1
        )

    def switch_view(self):
        self.cur_view_idx = (self.cur_view_idx + 1) % len(VIEW_CONFIGS)
        self.setup_camera_subscription()
        view_info = VIEW_CONFIGS[self.cur_view_idx]
        print(f"\n[視角切換] >> {view_info['name']} ({view_info['desc']})")

    def reset_origin(self):
        print("\n[原點重設] 正在瞬移 Model Y 回光復關新路口起點右側車道 (5, -5, 0.38)...")
        self.speed = 0.0
        self.steer = 0.0
        self.publish_twist()

        cmd = [
            "gz", "service", "-s", "/world/guanxin_world/set_pose",
            "--reqtype", "gz.msgs.Pose",
            "--reptype", "gz.msgs.Boolean",
            "--timeout", "1500",
            "--req",
            'name: "model_y", position: {x: 5.0, y: -5.0, z: 0.38}, orientation: {x: 0, y: 0, z: 0, w: 1}'
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=2.0)
            if res.returncode == 0 and "data: true" in res.stdout:
                print("[原點重設] 瞬移成功！車輛已回到光復路關新路口起點，速度已歸零。")
            else:
                print(f"[原點重設] 回傳資訊: {res.stdout.strip() if res.stdout else res.stderr.strip()}")
        except Exception as e:
            print(f"[原點重設] 呼叫 set_pose 服務異常: {e}")

    def on_image(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"Image conversion error: {e}")
            return

        h, w, _ = frame.shape
        # 繪製頂部半透明 HUD 黑色背景條
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, 75), (20, 20, 20), -1)
        # 繪製底部半透明 HUD 說明條
        cv2.rectangle(overlay, (0, h - 35), (w, h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

        # 頂部資訊顯示
        view_name = VIEW_CONFIGS[self.cur_view_idx]['name']
        cv2.putText(frame, f"CAM: {view_name}", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 180), 2)

        status_text = f"Speed: {self.speed:5.1f} m/s  |  Steer: {self.steer:5.2f} rad"
        cv2.putText(frame, status_text, (15, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 底部控制提示
        ctrl_hint = "[W/S] Throttle/Rev   [A/D] Steer   [Space] Brake   [V] View   [O] Reset   [Q] Quit"
        cv2.putText(frame, ctrl_hint, (15, h - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (200, 200, 200), 1)

        cv2.imshow("Tesla Model Y - Camera HUD", frame)
        cv2.waitKey(1)

    def publish_twist(self):
        t = Twist()
        t.linear.x = float(self.speed)
        t.angular.z = float(self.steer)
        self.pub_cmd.publish(t)

def main(args=None):
    rclpy.init(args=args)
    node = TeleopVehicle()

    is_tty = sys.stdin.isatty()
    old_attr = None
    if is_tty:
        old_attr = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.03)

            if is_tty and select.select([sys.stdin], [], [], 0)[0]:
                c = sys.stdin.read(1)
                if c in KEY_MAP:
                    dv, dw = KEY_MAP[c]
                    if dv != 0:
                        node.speed = max(min(node.speed + dv, 22.0), -6.0)
                    if dw != 0:
                        node.steer = max(min(node.steer + dw, 0.7), -0.7)
                    print(f"\r[驅動指令] 車速: {node.speed:5.1f} m/s | 轉角: {node.steer:5.2f} rad", end="", flush=True)
                elif c == ' ':
                    node.speed = 0.0
                    node.steer = 0.0
                    print("\r[緊急煞車] 車速與轉角已歸零 (0.0)", end="", flush=True)
                elif c == 'v':
                    node.switch_view()
                elif c == 'o':
                    node.reset_origin()
                elif c == 'q':
                    print("\n正在關閉控制節點...")
                    break
    except KeyboardInterrupt:
        pass
    finally:
        if is_tty and old_attr is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
