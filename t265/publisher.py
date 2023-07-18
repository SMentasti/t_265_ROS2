import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from nav_msgs.msg import Odometry

from rclpy.clock import Clock

import pyrealsense2 as rs

from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('t_265_publisher')
        self.publisher_ = self.create_publisher(Odometry, 't265/odom', 1)
        self.tf_broadcaster = TransformBroadcaster(self)
        
        #realsense init
        pipe = rs.pipeline()

        # Build config object and request pose data
        cfg = rs.config()
        cfg.enable_stream(rs.stream.pose)

        # Start streaming with requested config
        pipe.start(cfg)
        msg = Odometry()
        t = TransformStamped()
        while (rclpy.ok()):
          frames = pipe.wait_for_frames()
          pose = frames.get_pose_frame()
          if (pose):
            data = pose.get_pose_data()
            msg.header.stamp = Clock().now().to_msg()
            t.header.stamp = msg.header.stamp
            msg.header.frame_id = "t265"
            t.header.frame_id = 'odom'
            t.child_frame_id = "t265"
            msg.pose.pose.position.x = -data.translation.z
            t.transform.translation.x = -data.translation.z
            msg.pose.pose.position.y = -data.translation.x
            t.transform.translation.y = -data.translation.x
            msg.pose.pose.position.z = data.translation.y
            t.transform.translation.z = data.translation.y
            msg.pose.pose.orientation.x = -data.rotation.z
            t.transform.rotation.x = -data.rotation.z
            msg.pose.pose.orientation.y = -data.rotation.x
            t.transform.rotation.y = -data.rotation.x
            msg.pose.pose.orientation.z = data.rotation.y
            t.transform.rotation.z = data.rotation.y
            msg.pose.pose.orientation.w = data.rotation.w
            t.transform.rotation.w = data.rotation.w
            
            self.publisher_.publish(msg)
            self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)


    publisher = MinimalPublisher()

    rclpy.spin(publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
