#include <rclcpp/rclcpp.hpp>
#include <trajectory_msgs/msg/joint_trajectory.hpp>
#include <trajectory_msgs/msg/joint_trajectory_point.hpp>

#include <iostream>
#include <sstream>
#include <iomanip>

using TrajMsg = trajectory_msgs::msg::JointTrajectory;
using TrajPoint = trajectory_msgs::msg::JointTrajectoryPoint;

class TrajectoryDebugNode : public rclcpp::Node
{
public:
    TrajectoryDebugNode()
    : Node("trajectory_debug_node")
    {
        // The execute_trajectory topic is the internal MoveIt -> controller bus.
        // In real mode, move_group publishes the planned trajectory here before
        // the SimpleControllerManager forwards it to /robot1/follow_joint_trajectory.
        sub_ = create_subscription<TrajMsg>(
            "/execute_trajectory",
            rclcpp::SystemDefaultsQoS(),
            [this](const TrajMsg::SharedPtr msg) { onTrajectory(msg); }
        );

        RCLCPP_INFO(get_logger(), "[trajectory_debug] Listening on /execute_trajectory");
    }

private:
    void onTrajectory(const TrajMsg::SharedPtr msg)
    {
        std::ostringstream oss;
        oss << "\n========== TRAJECTORY DEBUG ==========\n";
        oss << "  joint_names: " << msg->joint_names.size() << " joints: [";
        for (size_t i = 0; i < msg->joint_names.size(); ++i) {
            oss << msg->joint_names[i];
            if (i + 1 < msg->joint_names.size()) oss << ", ";
        }
        oss << "]\n";
        oss << "  points: " << msg->points.size() << " trajectory points\n";

        bool all_have_velocities = true;
        bool all_have_time = true;

        for (size_t i = 0; i < msg->points.size(); ++i) {
            const auto& pt = msg->points[i];
            oss << "  point[" << i << "]: "
                << "positions=" << pt.positions.size()
                << " velocities=" << pt.velocities.size()
                << " accelerations=" << pt.accelerations.size()
                << " time_from_start=" << pt.time_from_start.sec << "."
                << std::setfill('0') << std::setw(9) << pt.time_from_start.nanosec << "s";

            if (pt.positions.empty()) {
                oss << " [EMPTY POSITIONS!]";
            }
            if (pt.velocities.empty()) {
                oss << " [NO VELOCITIES!]";
                all_have_velocities = false;
            } else {
                oss << " [";
                for (size_t v = 0; v < pt.velocities.size(); ++v) {
                    oss << pt.velocities[v];
                    if (v + 1 < pt.velocities.size()) oss << ", ";
                }
                oss << "]";
            }
            if (pt.time_from_start.sec == 0 && pt.time_from_start.nanosec == 0) {
                oss << " [NO TIME_FROM_START!]";
                all_have_time = false;
            }
            oss << "\n";
        }

        oss << "----------------------------------\n";
        if (all_have_velocities) {
            oss << "  [OK] All " << msg->points.size() << " points have velocity data\n";
        } else {
            oss << "  [FAIL] Some points MISSING velocity data!\n";
        }
        if (all_have_time) {
            oss << "  [OK] All points have time_from_start\n";
        } else {
            oss << "  [FAIL] Some points MISSING time_from_start!\n";
        }
        oss << "====================================\n";

        RCLCPP_WARN(get_logger(), "%s", oss.str().c_str());
    }

    rclcpp::Subscription<TrajMsg>::SharedPtr sub_;
};

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<TrajectoryDebugNode>());
    rclcpp::shutdown();
    return 0;
}
