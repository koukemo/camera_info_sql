import os
import rclpy
import time
from rclpy.node import Node
import message_filters

from sensor_msgs.msg import CameraInfo
from camera_info_sql.sql_operations.sql_operation import JsonOperation, SqlInsert


class CameraInfoSubscriber(Node):

    def __init__(self):
        super().__init__('camera_info_subscriber')
        camera_info_subscriber = message_filters.Subscriber(self, CameraInfo, '/camera_info')

        self.time_synchronizer = message_filters.TimeSynchronizer([camera_info_subscriber, ], 3000)
        self.time_synchronizer.registerCallback(self.listener_callback)

    def listener_callback(self, camera_info: CameraInfo):
        try:
            i = 1

            workspace_path = os.path.join(os.environ['HOME'], 'ros2_ws/src/')
            json_save_path = os.path.join(workspace_path, 'camera_info_sql/resource/jsons/')
            os.makedirs(json_save_path, exist_ok=True)

            # Write camera_info → camera_info_sql/resource/jsons/camera_info.json
            print(f"Create camera_info_from_msg_{i}.json at {json_save_path}")
            JsonOperation.write_json_from_ros_msg(camera_info, json_save_path, 'camera_info_from_msg_'+str(i))

            # Insert camera_info → json_tables > json_datas column
            print("Write camera_info to SQL")
            SqlInsert.insert_json_tables(camera_info)

            print(f"Create camera_info_from_sql.json at {json_save_path}")
            JsonOperation.create_json_from_sql(json_save_path)

            time.sleep(100)

        except Exception as err:
            self.get_logger().error(err)


def main(args=None):
    rclpy.init(args=args)

    camera_info_subscriber = CameraInfoSubscriber()

    try:
        while rclpy.ok():
            rclpy.spin(camera_info_subscriber)

    except KeyboardInterrupt:
        pass

    finally:
        camera_info_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
