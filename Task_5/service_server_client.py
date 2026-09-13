"""
Task 5: ROS 2 Service Communication (Server & Client)
Demonstrates synchronous Request/Response interaction between nodes.
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class WaypointServiceServer(Node):
    def _init_(self):
        super()._init_('waypoint_service_server')
        # Create service 'calculate_waypoint'
        self.srv = self.create_service(
            AddTwoInts, 
            'calculate_waypoint', 
            self.calculate_callback
        )
        self.get_logger().info('Waypoint Service Server is Ready.')

    def calculate_callback(self, request, response):
        # Adds coordinates (A + B) to calculate total target displacement
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming Request: A={request.a}, B={request.b}')
        self.get_logger().info(f'Sending Response: Sum={response.sum}')
        return response


class WaypointServiceClient(Node):
    def _init_(self):
        super()._init_('waypoint_service_client')
        self.cli = self.create_client(AddTwoInts, 'calculate_waypoint')
        
    def send_request(self, a, b):
        req = AddTwoInts.Request()
        req.a = a
        req.b = b
        return req


def main(args=None):
    rclpy.init(args=args)
    server = WaypointServiceServer()
    client = WaypointServiceClient()
    
    print("--- ROS 2 Service Server & Client Initialized ---")
    
    server.destroy_node()
    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()