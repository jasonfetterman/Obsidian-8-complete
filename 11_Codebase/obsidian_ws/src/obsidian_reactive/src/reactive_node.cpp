
#include "rclcpp/rclcpp.hpp"

class ReactiveNode : public rclcpp::Node
{
public:
    ReactiveNode() : Node("reactive_node")
    {
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(20),
            std::bind(&ReactiveNode::loop, this));
    }

private:
    void loop()
    {
        RCLCPP_INFO_THROTTLE(this->get_logger(), *this->get_clock(), 2000, "Reactive loop running...");
    }

    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ReactiveNode>());
    rclcpp::shutdown();
    return 0;
}
