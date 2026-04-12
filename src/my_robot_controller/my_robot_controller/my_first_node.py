#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty


class TeleopSimple(Node):

    def __init__(self):
        super().__init__('teleop_simple')

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.get_logger().info("🚀 Teleop started (w/a/s/d/x)")

    def get_key(self):
        """Đọc 1 ký tự từ bàn phím (Linux)"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return key

    def run(self):
        twist = Twist()

        while rclpy.ok():
            key = self.get_key()

            # reset
            twist.linear.x = 0.0
            twist.angular.z = 0.0

            if key == 'w':
                twist.linear.x = 0.3
            elif key == 's':
                twist.linear.x = -0.3
            elif key == 'a':
                twist.angular.z = 0.8
            elif key == 'd':
                twist.angular.z = -0.8
            elif key == 'x':
                twist.linear.x = 0.0
                twist.angular.z = 0.0
            elif key == '\x03':  # Ctrl+C
                break

            self.publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)

    node = TeleopSimple()
    node.run()

    rclpy.shutdown()


if __name__ == '__main__':
    main()