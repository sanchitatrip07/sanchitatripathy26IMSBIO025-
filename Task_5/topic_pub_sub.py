"""
Task 5: ROS 2 Topic Communication (Publisher & Subscriber)
Demonstrates simple asynchronous data sharing between two ROS 2 nodes.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    def _init_(self):
        super()._init_('minimal_publisher')
        # Create a publisher on topic 'ugv_status' with queue size 10
        self.publisher_ = self.create_publisher(String, 'ugv_status', 10)
        timer_period = 1.0  # publish every 1 second
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'UGV Status: Navigating Track - Ping {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')
        self.i += 1


class MinimalSubscriber(Node):
    def _init_(self):
        super()._init_('minimal_subscriber')
        # Subscribe to the 'ugv_status' topic
        self.subscription = self.create_subscription(
            String,
            'ugv_status',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)

    pub_node = MinimalPublisher()
    sub_node = MinimalSubscriber()

    print("--- ROS 2 Publisher & Subscriber Initialized ---")
    # Simulate single spin callback execution
    pub_node.timer_callback()
    
    pub_node.destroy_node()
    sub_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()