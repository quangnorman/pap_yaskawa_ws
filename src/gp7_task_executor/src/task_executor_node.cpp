#include <memory>
#include <string>
#include <vector>
#include <map>
#include <cmath>
#include <thread>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/pose.hpp"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "moveit/planning_scene_interface/planning_scene_interface.h"
#include "yaml-cpp/yaml.h"

#include "gp7_task_executor_msgs/srv/move_to_named_target.hpp"
#include "gp7_task_executor_msgs/srv/move_to_joint_target.hpp"
#include "gp7_task_executor_msgs/srv/move_to_pose_target.hpp"
#include "gp7_task_executor_msgs/srv/move_sequence.hpp"

class TaskExecutorNode : public rclcpp::Node
{
public:
  TaskExecutorNode()
  : Node("task_executor_node")
  {
    tf_buffer_ = std::make_shared<tf2_ros::Buffer>(get_clock());
    tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

    init_parameters();
    init_named_joint_targets();
    create_services();

    RCLCPP_INFO(this->get_logger(), "Task executor node constructed.");
    RCLCPP_INFO(this->get_logger(), "  move_group:           '%s'", move_group_name_.c_str());
    RCLCPP_INFO(this->get_logger(), "  base_frame:           '%s'", base_frame_.c_str());
    RCLCPP_INFO(this->get_logger(), "  ee_link:              '%s'", ee_link_.c_str());
    RCLCPP_INFO(this->get_logger(), "  planning_time:        %.2f s", planning_time_);
    RCLCPP_INFO(this->get_logger(), "  planning_attempts:    %d", num_planning_attempts_);
    RCLCPP_INFO(this->get_logger(), "  max_velocity_scale:  %.2f", max_velocity_scaling_factor_);
    RCLCPP_INFO(this->get_logger(), "  max_accel_scale:    %.2f", max_acceleration_scaling_factor_);
    RCLCPP_INFO(this->get_logger(), "Call init_move_group() after shared_ptr creation to enable planning.");
  }

  void init_move_group()
  {
    move_group_ = std::make_shared<moveit::planning_interface::MoveGroupInterface>(
        shared_from_this(), move_group_name_);

    move_group_->setMaxVelocityScalingFactor(max_velocity_scaling_factor_);
    move_group_->setMaxAccelerationScalingFactor(max_acceleration_scaling_factor_);

    RCLCPP_INFO(this->get_logger(), "MoveGroupInterface ready for group '%s'", move_group_name_.c_str());
  }

  static constexpr double DEG2RAD = M_PI / 180.0;
  static constexpr size_t EXPECTED_JOINT_COUNT = 6;

  void init_named_joint_targets()
  {
    if (waypoints_config_path_.empty())
    {
      RCLCPP_WARN(this->get_logger(),
                  "[Waypoints] waypoints_config_path is empty — no joint waypoints loaded.");
      return;
    }

    RCLCPP_INFO(this->get_logger(), "[Waypoints] Loading waypoints from: '%s'",
                waypoints_config_path_.c_str());

    try
    {
      YAML::Node root = YAML::LoadFile(waypoints_config_path_);
      if (!root["waypoints"] || !root["waypoints"].IsMap())
      {
        RCLCPP_ERROR(this->get_logger(),
                     "[Waypoints] YAML file '%s' is missing or has invalid 'waypoints:' map.",
                     waypoints_config_path_.c_str());
        return;
      }

      const YAML::Node& waypoints = root["waypoints"];
      static const std::vector<std::string> joint_order = {
          "joint_s", "joint_l", "joint_u", "joint_r", "joint_b", "joint_t"};

      named_joint_targets_.clear();

      for (const auto& wp : waypoints)
      {
        const std::string name = wp.first.as<std::string>();
        const YAML::Node& node = wp.second;

        if (!node["joints"] || !node["joints"].IsSequence())
        {
          RCLCPP_ERROR(this->get_logger(),
                       "[Waypoints] Skipping '%s': 'joints' field is missing or not a sequence.",
                       name.c_str());
          continue;
        }

        const YAML::Node& joints_node = node["joints"];
        if (joints_node.size() != EXPECTED_JOINT_COUNT)
        {
          RCLCPP_ERROR(this->get_logger(),
                       "[Waypoints] Skipping '%s': expected %lu joints but got %zu.",
                       name.c_str(), EXPECTED_JOINT_COUNT, joints_node.size());
          continue;
        }

        std::vector<double> rad_values;
        rad_values.reserve(EXPECTED_JOINT_COUNT);
        for (size_t i = 0; i < EXPECTED_JOINT_COUNT; ++i)
        {
          rad_values.push_back(joints_node[i].as<double>() * DEG2RAD);
        }

        named_joint_targets_[name] = rad_values;
      }

      RCLCPP_INFO(this->get_logger(), "[Waypoints] Loaded %zu named joint waypoints:", named_joint_targets_.size());
      for (const auto& [name, values] : named_joint_targets_)
      {
        std::string msg = "  " + name + ": [";
        for (size_t i = 0; i < values.size(); ++i)
        {
          msg += std::to_string(values[i]) + " rad";
          if (i < values.size() - 1) msg += ", ";
        }
        msg += "]  (" + joint_order[0];
        for (size_t i = 1; i < joint_order.size(); ++i) msg += ", " + joint_order[i];
        msg += ")";
        RCLCPP_INFO(this->get_logger(), "%s", msg.c_str());
      }
    }
    catch (const YAML::Exception& ex)
    {
      RCLCPP_ERROR(this->get_logger(),
                   "[Waypoints] Failed to parse '%s': %s",
                   waypoints_config_path_.c_str(), ex.what());
    }
    catch (const std::exception& ex)
    {
      RCLCPP_ERROR(this->get_logger(),
                   "[Waypoints] Unexpected error loading '%s': %s",
                   waypoints_config_path_.c_str(), ex.what());
    }
  }

  bool move_to_named_joint_target(const std::string& name, bool execute)
  {
    auto it = named_joint_targets_.find(name);
    if (it == named_joint_targets_.end())
    {
      RCLCPP_ERROR(this->get_logger(), "Unknown named joint target: '%s'", name.c_str());
      return false;
    }

    static const std::vector<std::string> joint_order = {
        "joint_s", "joint_l", "joint_u", "joint_r", "joint_b", "joint_t"};
    const std::vector<double>& values = it->second;

    std::string values_msg;
    for (size_t i = 0; i < joint_order.size(); ++i)
    {
      values_msg += joint_order[i] + "=" + std::to_string(values[i]) + " rad";
      if (i < joint_order.size() - 1) values_msg += ", ";
    }
    RCLCPP_INFO(this->get_logger(), "[JointTarget] Named target '%s': %s",
                name.c_str(), values_msg.c_str());

    move_group_->setStartStateToCurrentState();

    std::map<std::string, double> target_map;
    for (size_t i = 0; i < joint_order.size(); ++i)
    {
      target_map[joint_order[i]] = values[i];
    }

    if (!move_group_->setJointValueTarget(target_map))
    {
      RCLCPP_ERROR(this->get_logger(), "[JointTarget] setJointValueTarget() returned false for '%s'",
                   name.c_str());
      return false;
    }

    move_group_->setPlanningTime(planning_time_);
    move_group_->setNumPlanningAttempts(num_planning_attempts_);

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    auto result = move_group_->plan(plan);

    if (result != moveit::core::MoveItErrorCode::SUCCESS)
    {
      RCLCPP_ERROR(this->get_logger(), "[JointTarget] plan() failed for '%s' (error code: %d)",
                   name.c_str(), result.val);
      return false;
    }

    RCLCPP_INFO(this->get_logger(), "[JointTarget] plan() succeeded for '%s' (%lu waypoints).",
                name.c_str(), plan.trajectory_.joint_trajectory.points.size());

    if (execute)
    {
      RCLCPP_INFO(this->get_logger(), "[JointTarget] Executing '%s'...", name.c_str());
      auto exec_result = move_group_->execute(plan.trajectory_);
      if (exec_result != moveit::core::MoveItErrorCode::SUCCESS)
      {
        RCLCPP_ERROR(this->get_logger(), "[JointTarget] execute() failed for '%s' (error code: %d)",
                     name.c_str(), exec_result.val);
        return false;
      }
      RCLCPP_INFO(this->get_logger(), "[JointTarget] Execution of '%s' completed successfully.",
                  name.c_str());
    }
    else
    {
      RCLCPP_INFO(this->get_logger(), "[JointTarget] Plan-only for '%s': trajectory not executed.",
                  name.c_str());
    }

    return true;
  }

private:
  void init_parameters()
  {
    this->declare_parameter<std::string>("move_group_name", "arm");
    this->declare_parameter<std::string>("base_frame", "world");
    this->declare_parameter<std::string>("ee_link", "tool0");
    this->declare_parameter<std::string>("waypoints_config_path", "");
    this->declare_parameter<double>("planning_time", 2.0);
    this->declare_parameter<int>("num_planning_attempts", 5);
    this->declare_parameter<double>("max_velocity_scaling_factor", 0.5);
    this->declare_parameter<double>("max_acceleration_scaling_factor", 0.5);

    this->get_parameter("move_group_name", move_group_name_);
    this->get_parameter("base_frame", base_frame_);
    this->get_parameter("ee_link", ee_link_);
    this->get_parameter("waypoints_config_path", waypoints_config_path_);
    this->get_parameter("planning_time", planning_time_);
    this->get_parameter("num_planning_attempts", num_planning_attempts_);
    this->get_parameter("max_velocity_scaling_factor", max_velocity_scaling_factor_);
    this->get_parameter("max_acceleration_scaling_factor", max_acceleration_scaling_factor_);
  }

  void create_services()
  {
    service_named_target_ = create_service<gp7_task_executor_msgs::srv::MoveToNamedTarget>(
      "/move_to_named_target",
      [this](
        const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedTarget::Request> request,
        std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedTarget::Response> response)
      {
        handle_named_target(request, response);
      });

    service_joint_target_ = create_service<gp7_task_executor_msgs::srv::MoveToJointTarget>(
      "/move_to_joint_target",
      [this](
        const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToJointTarget::Request> request,
        std::shared_ptr<gp7_task_executor_msgs::srv::MoveToJointTarget::Response> response)
      {
        handle_joint_target(request, response);
      });

    service_pose_target_ = create_service<gp7_task_executor_msgs::srv::MoveToPoseTarget>(
      "/move_to_pose_target",
      [this](
        const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget::Request> request,
        std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget::Response> response)
      {
        handle_pose_target(request, response);
      });

    service_move_sequence_ = create_service<gp7_task_executor_msgs::srv::MoveSequence>(
      "/move_sequence",
      [this](
        const std::shared_ptr<gp7_task_executor_msgs::srv::MoveSequence::Request> request,
        std::shared_ptr<gp7_task_executor_msgs::srv::MoveSequence::Response> response)
      {
        handle_move_sequence(request, response);
      });

    RCLCPP_INFO(this->get_logger(), "Services created: /move_to_named_target, /move_to_joint_target, /move_to_pose_target, /move_sequence");
  }

  bool plan_and_maybe_execute(bool should_execute)
  {
    move_group_->setStartStateToCurrentState();

    move_group_->setPlanningTime(planning_time_);
    move_group_->setNumPlanningAttempts(num_planning_attempts_);

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    auto result = move_group_->plan(plan);

    if (result != moveit::core::MoveItErrorCode::SUCCESS)
    {
      RCLCPP_ERROR(this->get_logger(), "Planning failed with error code: %d", result.val);
      return false;
    }

    RCLCPP_INFO(this->get_logger(), "Plan succeeded (%lu waypoints).",
                plan.trajectory_.joint_trajectory.points.size());

    if (should_execute)
    {
      RCLCPP_INFO(this->get_logger(), "Executing trajectory...");
      auto exec_result = move_group_->execute(plan.trajectory_);
      if (exec_result != moveit::core::MoveItErrorCode::SUCCESS)
      {
        RCLCPP_ERROR(this->get_logger(), "Execution failed with error code: %d", exec_result.val);
        return false;
      }
      RCLCPP_INFO(this->get_logger(), "Execution completed successfully.");
    }
    else
    {
      RCLCPP_INFO(this->get_logger(), "Plan-only mode: trajectory not executed.");
    }

    return true;
  }

  void handle_named_target(
    const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedTarget::Request> request,
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedTarget::Response> response)
  {
    const std::string& target_name = request->target_name;
    bool execute = request->execute;

    if (target_name.empty())
    {
      response->success = false;
      response->message = "target_name is empty";
      RCLCPP_WARN(this->get_logger(), "%s", response->message.c_str());
      return;
    }

    if (named_joint_targets_.count(target_name) > 0)
    {
      bool ok = move_to_named_joint_target(target_name, execute);
      response->success = ok;
      response->message = ok
        ? "Named joint target '" + target_name + "' " + (execute ? "executed" : "planned") + " successfully"
        : "Failed to " + std::string(execute ? "plan/execute" : "plan") + " named joint target '" + target_name + "'";
      return;
    }

    RCLCPP_INFO(this->get_logger(), "SRDF named target: '%s', execute=%d", target_name.c_str(), execute);
    move_group_->setStartStateToCurrentState();
    move_group_->setNamedTarget(target_name);

    bool ok = plan_and_maybe_execute(execute);
    response->success = ok;
    response->message = ok
      ? "Named target '" + target_name + "' " + (execute ? "executed" : "planned") + " successfully"
      : "Failed to " + std::string(execute ? "plan/execute" : "plan") + " named target '" + target_name + "'";
  }

  void handle_move_sequence(
    const std::shared_ptr<gp7_task_executor_msgs::srv::MoveSequence::Request> request,
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveSequence::Response> response)
  {
    const auto& waypoint_names = request->waypoint_names;
    bool execute = request->execute;

    if (waypoint_names.empty())
    {
      response->success = false;
      response->message = "Empty sequence: waypoint_names must not be empty";
      RCLCPP_WARN(this->get_logger(), "[MoveSequence] %s", response->message.c_str());
      return;
    }

    RCLCPP_INFO(this->get_logger(),
                "[MoveSequence] Starting sequence of %lu waypoints (execute=%d):",
                waypoint_names.size(), execute);
    for (size_t i = 0; i < waypoint_names.size(); ++i)
    {
      RCLCPP_INFO(this->get_logger(), "  step %zu: '%s'", i + 1, waypoint_names[i].c_str());
    }

    for (size_t i = 0; i < waypoint_names.size(); ++i)
    {
      const std::string& name = waypoint_names[i];

      if (named_joint_targets_.find(name) == named_joint_targets_.end())
      {
        response->success = false;
        response->message = "Unknown waypoint name '" + name +
                            "' at step " + std::to_string(i + 1) + " of " +
                            std::to_string(waypoint_names.size());
        RCLCPP_ERROR(this->get_logger(), "[MoveSequence] %s", response->message.c_str());
        return;
      }

      RCLCPP_INFO(this->get_logger(),
                  "[MoveSequence] Step %zu/%zu: moving to waypoint '%s'...",
                  i + 1, waypoint_names.size(), name.c_str());

      bool ok = move_to_named_joint_target(name, execute);
      if (!ok)
      {
        response->success = false;
        response->message = "Failed at step " + std::to_string(i + 1) +
                            " / waypoint '" + name + "'";
        RCLCPP_ERROR(this->get_logger(), "[MoveSequence] %s", response->message.c_str());
        return;
      }

      if (i < waypoint_names.size() - 1)
      {
        RCLCPP_INFO(this->get_logger(),
                    "[MoveSequence] Step %zu/%zu: waypoint '%s' reached, pausing 0.5s before next move.",
                    i + 1, waypoint_names.size(), name.c_str());
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
      }
    }

    RCLCPP_INFO(this->get_logger(),
                "[MoveSequence] All %lu waypoints completed successfully.",
                waypoint_names.size());
    response->success = true;
    response->message = "MoveSequence completed successfully (" +
                        std::to_string(waypoint_names.size()) + " waypoints)";
  }

  void handle_joint_target(
    const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToJointTarget::Request> request,
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToJointTarget::Response> response)
  {
    const std::vector<std::string>& joint_names = request->joint_names;
    const std::vector<double>& positions = request->positions;
    bool execute = request->execute;

    RCLCPP_INFO(this->get_logger(), "Joint target: %lu joints, execute=%d", joint_names.size(), execute);

    if (joint_names.empty() || positions.empty())
    {
      response->success = false;
      response->message = "joint_names and positions must not be empty";
      RCLCPP_WARN(this->get_logger(), "%s", response->message.c_str());
      return;
    }

    if (joint_names.size() != positions.size())
    {
      response->success = false;
      response->message = "joint_names size (" + std::to_string(joint_names.size()) +
                          ") must match positions size (" + std::to_string(positions.size()) + ")";
      RCLCPP_WARN(this->get_logger(), "%s", response->message.c_str());
      return;
    }

    move_group_->setStartStateToCurrentState();

    std::map<std::string, double> target_map;
    for (size_t i = 0; i < joint_names.size(); ++i)
    {
      target_map[joint_names[i]] = positions[i];
    }

    if (!move_group_->setJointValueTarget(target_map))
    {
      response->success = false;
      response->message = "setJointValueTarget() returned false for the given joint map";
      RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
      return;
    }

    bool ok = plan_and_maybe_execute(execute);
    response->success = ok;
    response->message = ok
      ? "Joint target " + std::string(execute ? "executed" : "planned") + " successfully"
      : "Failed to " + std::string(execute ? "plan/execute" : "plan") + " joint target";
  }

  void handle_pose_target(
    const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget::Request> request,
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToPoseTarget::Response> response)
  {
    const geometry_msgs::msg::Pose& pose = request->pose;
    const std::string& requested_frame = request->frame_id;
    bool execute = request->execute;

    const std::string& mg_name = move_group_->getName();
    const std::string planning_frame = move_group_->getPlanningFrame();
    const std::string pose_ref_frame = move_group_->getPoseReferenceFrame();
    const std::string ee_link = move_group_->getEndEffectorLink();

    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget] === INCOMING REQUEST ===");
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   move_group:            '%s'", mg_name.c_str());
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   planning_frame:         '%s'", planning_frame.c_str());
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   pose_reference_frame:   '%s'", pose_ref_frame.c_str());
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   end_effector_link:      '%s'", ee_link.c_str());
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   requested frame_id:     '%s'", requested_frame.c_str());
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   input pose xyz:         (%.4f, %.4f, %.4f)",
                pose.position.x, pose.position.y, pose.position.z);
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   input quaternion xyzw:  (%.4f, %.4f, %.4f, %.4f)",
                pose.orientation.x, pose.orientation.y,
                pose.orientation.z, pose.orientation.w);

    if (requested_frame.empty())
    {
      response->success = false;
      response->message = "frame_id must not be empty";
      RCLCPP_WARN(this->get_logger(), "%s", response->message.c_str());
      return;
    }

    double q_norm = std::sqrt(
        pose.orientation.x * pose.orientation.x +
        pose.orientation.y * pose.orientation.y +
        pose.orientation.z * pose.orientation.z +
        pose.orientation.w * pose.orientation.w);

    if (q_norm < 1e-9)
    {
      response->success = false;
      response->message = "Invalid target frame '" + requested_frame +
                          "': quaternion has zero norm (must be non-zero)";
      RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
      return;
    }

    geometry_msgs::msg::Pose transformed_pose = pose;
    std::string planning_frame_used;

    if (requested_frame == planning_frame)
    {
      transformed_pose = pose;
      planning_frame_used = planning_frame;
      RCLCPP_INFO(this->get_logger(),
                  "[PoseTarget]   frame_id matches planning_frame '%s' — no TF transform needed.",
                  planning_frame.c_str());
    }
    else
    {
      try
      {
        geometry_msgs::msg::TransformStamped tf_msg = tf_buffer_->lookupTransform(
            planning_frame, requested_frame, rclcpp::Time(0),
            rclcpp::Duration::from_seconds(1.0));

        geometry_msgs::msg::PoseStamped pose_stamped_in;
        pose_stamped_in.header.stamp = tf_msg.header.stamp;
        pose_stamped_in.header.frame_id = requested_frame;
        pose_stamped_in.pose = pose;

        geometry_msgs::msg::PoseStamped pose_stamped_out =
            tf_buffer_->transform(pose_stamped_in, planning_frame);

        transformed_pose = pose_stamped_out.pose;
        planning_frame_used = planning_frame;

        RCLCPP_INFO(this->get_logger(),
                    "[PoseTarget]   TF transform '%s' -> '%s' succeeded.",
                    requested_frame.c_str(), planning_frame.c_str());
        RCLCPP_INFO(this->get_logger(),
                    "[PoseTarget]   transformed pose xyz:     (%.4f, %.4f, %.4f)",
                    transformed_pose.position.x,
                    transformed_pose.position.y,
                    transformed_pose.position.z);
        RCLCPP_INFO(this->get_logger(),
                    "[PoseTarget]   transformed quat xyzw:    (%.4f, %.4f, %.4f, %.4f)",
                    transformed_pose.orientation.x,
                    transformed_pose.orientation.y,
                    transformed_pose.orientation.z,
                    transformed_pose.orientation.w);
      }
      catch (const tf2::TransformException& ex)
      {
        response->success = false;
        response->message = "Invalid target frame '" + requested_frame +
                            "': TF transform failed — " + ex.what();
        RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
        return;
      }
    }

    move_group_->setStartStateToCurrentState();

    move_group_->setPoseReferenceFrame(planning_frame_used);
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   setPoseReferenceFrame('%s')", planning_frame_used.c_str());

    move_group_->setPlanningTime(planning_time_);
    move_group_->setNumPlanningAttempts(num_planning_attempts_);

    bool set_ok = move_group_->setPoseTarget(transformed_pose, ee_link);
    if (!set_ok)
    {
      response->success = false;
      response->message = "Failed to set pose target for ee link '" + ee_link + "'";
      RCLCPP_ERROR(this->get_logger(), "%s", response->message.c_str());
      move_group_->clearPoseTargets();
      return;
    }
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   setPoseTarget(pose, '%s') → true", ee_link.c_str());

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    auto plan_result = move_group_->plan(plan);

    if (plan_result != moveit::core::MoveItErrorCode::SUCCESS)
    {
      response->success = false;
      response->message = "Failed to plan pose target for group '" + mg_name + "'";
      RCLCPP_ERROR(this->get_logger(),
                   "[PoseTarget]   plan() failed with error code: %d", plan_result.val);
      move_group_->clearPoseTargets();
      return;
    }
    RCLCPP_INFO(this->get_logger(),
                "[PoseTarget]   plan() succeeded (%lu waypoints).",
                plan.trajectory_.joint_trajectory.points.size());

    if (execute)
    {
      RCLCPP_INFO(this->get_logger(), "[PoseTarget]   Executing trajectory...");
      auto exec_result = move_group_->execute(plan.trajectory_);
      if (exec_result != moveit::core::MoveItErrorCode::SUCCESS)
      {
        response->success = false;
        response->message = "Failed to execute pose target";
        RCLCPP_ERROR(this->get_logger(),
                     "[PoseTarget]   execute() failed with error code: %d", exec_result.val);
        move_group_->clearPoseTargets();
        return;
      }
      RCLCPP_INFO(this->get_logger(), "[PoseTarget]   Execution completed successfully.");
    }
    else
    {
      RCLCPP_INFO(this->get_logger(), "[PoseTarget]   Plan-only mode: trajectory not executed.");
    }

    move_group_->clearPoseTargets();

    response->success = true;
    response->message = "Pose target " + std::string(execute ? "executed" : "planned") + " successfully";
  }

  std::string move_group_name_;
  std::string base_frame_;
  std::string ee_link_;
  std::string waypoints_config_path_;
  double planning_time_;
  int num_planning_attempts_;
  double max_velocity_scaling_factor_;
  double max_acceleration_scaling_factor_;

  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_;

  rclcpp::Service<gp7_task_executor_msgs::srv::MoveToNamedTarget>::SharedPtr service_named_target_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveToJointTarget>::SharedPtr service_joint_target_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveToPoseTarget>::SharedPtr service_pose_target_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveSequence>::SharedPtr service_move_sequence_;

  std::map<std::string, std::vector<double>> named_joint_targets_;
};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);

  auto node = std::make_shared<TaskExecutorNode>();

  node->init_move_group();

  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
