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
            #self.get_logger().info('%s' % camera_info, once=True)
            print(camera_info)

            camera_info_shaping = JsonOperation.camera_info_to_json(camera_info)
            f = open('myfile.txt', 'w')
            f.write(str(camera_info))
            f.close()
            f = open('myfile_shaping.json', 'w')
            f.write(str(camera_info_shaping))
            f.close()

            time.sleep(100)

        except Exception as err:
            self.get_logger().error(err)


def main(args=None):
    rclpy.init(args=args)

    camera_info_subscriber = CameraInfoSubscriber()

    try:
        rclpy.spin(camera_info_subscriber)

    except KeyboardInterrupt:
        pass

    finally:
        camera_info_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
