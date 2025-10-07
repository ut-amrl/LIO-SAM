#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs_py.point_cloud2 as pc2

class LivoxToLioSam(Node):
    def __init__(self):
        super().__init__('livox_to_lio_sam')
        self.sub = self.create_subscription(PointCloud2, '/livox/lidar', self.cb, 10)
        self.pub = self.create_publisher(PointCloud2, '/livox/points', 10)

    def cb(self, msg):
        new_fields = []
        for f in msg.fields:
            if f.name == "line":
                new_fields.append(PointField(name="ring", offset=f.offset, datatype=f.datatype, count=f.count))
            elif f.name == "timestamp":
                new_fields.append(PointField(name="time", offset=f.offset, datatype=PointField.FLOAT32, count=1))
            else:
                new_fields.append(f)

        new_msg = PointCloud2()
        new_msg.header = msg.header
        new_msg.height = msg.height
        new_msg.width = msg.width
        new_msg.is_bigendian = msg.is_bigendian
        new_msg.point_step = msg.point_step
        new_msg.row_step = msg.row_step
        new_msg.is_dense = msg.is_dense
        new_msg.fields = new_fields
        new_msg.data = msg.data

        self.pub.publish(new_msg)

def main(args=None):
    rclpy.init(args=args)
    node = LivoxToLioSam()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
