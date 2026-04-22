#include <memory>
#include <string>
#include <vector>
#include <map>
#include <cmath>
#include <thread>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/pose.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "moveit/move_group_interface/move_group_interface.h"
#include "moveit/planning_scene_interface/planning_scene_interface.h"
#include "yaml-cpp/yaml.h"

#include "gp7_task_executor_msgs/srv/move_to_named_target.hpp"
#include "gp7_task_executor_msgs/srv/move_to_joint_target.hpp"
#include "gp7_task_executor_msgs/srv/move_to_pose_target.hpp"
#include "gp7_task_executor_msgs/srv/move_to_named_pose_target.hpp"
#include "gp7_task_executor_msgs/srv/move_to_cartesian_target.hpp"
#include "gp7_task_executor_msgs/srv/move_to_named_cartesian_target.hpp"
#include "gp7_task_executor_msgs/srv/move_cartesian_sequence.hpp"
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
    init_named_cartesian_points();
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

    RCLCPP_INFO(this->get_logger(), "[Waypoints] Loading joint waypoints from: '%s'",
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

  void init_named_cartesian_points()
  {
    // Fixed Cartesian tool orientation: tool pointing downward.
    // Rationale:
    //   - Stable vertical orientation for pick/place tasks
    //   - Eliminates orientation drift during Cartesian interpolation
    //   - Simpler DRL action space: future RL agents output only dx, dy, dz
    constexpr double FIXED_ROLL  = M_PI;
    constexpr double FIXED_PITCH = 0.0;
    constexpr double FIXED_YAW   = 0.0;

    double qx, qy, qz, qw;
    rpy_to_quaternion(FIXED_ROLL, FIXED_PITCH, FIXED_YAW, qx, qy, qz, qw);
    cartesian_quat_.x = qx;
    cartesian_quat_.y = qy;
    cartesian_quat_.z = qz;
    cartesian_quat_.w = qw;

    RCLCPP_INFO(this->get_logger(), "[CartesianPoints] =======================================");
    RCLCPP_INFO(this->get_logger(),
                "[CartesianPoints] Cartesian tool orientation is FIXED (roll=pi, pitch=0, yaw=0).");
    RCLCPP_INFO(this->get_logger(),
                "[CartesianPoints]   fixed quaternion: (%.6f, %.6f, %.6f, %.6f)  [norm=%.6f]",
                qx, qy, qz, qw, std::sqrt(qx*qx + qy*qy + qz*qz + qw*qw));
    RCLCPP_INFO(this->get_logger(),
                "[CartesianPoints] Rationale: stable vertical tool, simpler DRL action space (dx/dy/dz only).");

    if (cartesian_points_config_path_.empty())
    {
      RCLCPP_WARN(this->get_logger(),
                  "[CartesianPoints] cartesian_points_config_path is empty — no cartesian points loaded.");
      RCLCPP_INFO(this->get_logger(), "[CartesianPoints] =======================================");
      return;
    }

    RCLCPP_INFO(this->get_logger(),
                "[CartesianPoints] Loading cartesian points from: '%s'",
                cartesian_points_config_path_.c_str());

    try
    {
      YAML::Node root = YAML::LoadFile(cartesian_points_config_path_);
      if (!root["cartesian_points"] || !root["cartesian_points"].IsMap())
      {
        RCLCPP_ERROR(this->get_logger(),
                     "[CartesianPoints] YAML file '%s' is missing or has invalid 'cartesian_points:' map.",
                     cartesian_points_config_path_.c_str());
        RCLCPP_INFO(this->get_logger(), "[CartesianPoints] =======================================");
        return;
      }

      const YAML::Node& cartesian_points = root["cartesian_points"];
      named_cartesian_points_.clear();

      for (const auto& wp : cartesian_points)
      {
        const std::string name = wp.first.as<std::string>();
        const YAML::Node& node = wp.second;

        if (!node["frame_id"] || !node["frame_id"].IsScalar() ||
            node["frame_id"].as<std::string>().empty())
        {
          RCLCPP_ERROR(this->get_logger(),
                       "[CartesianPoints] Skipping '%s': 'frame_id' is missing or empty.",
                       name.c_str());
          continue;
        }

        if (!node["xyz"] || !node["xyz"].IsSequence() ||
            node["xyz"].size() != 3)
        {
          RCLCPP_ERROR(this->get_logger(),
                       "[CartesianPoints] Skipping '%s': 'xyz' must be a sequence of exactly 3 values.",
                       name.c_str());
          continue;
        }

        geometry_msgs::msg::PoseStamped pose_stamped;
        pose_stamped.header.stamp = get_clock()->now();
        pose_stamped.header.frame_id = node["frame_id"].as<std::string>();
        pose_stamped.pose.position.x = node["xyz"][0].as<double>();
        pose_stamped.pose.position.y = node["xyz"][1].as<double>();
        pose_stamped.pose.position.z = node["xyz"][2].as<double>();
        pose_stamped.pose.orientation = cartesian_quat_;

        named_cartesian_points_[name] = pose_stamped;

        RCLCPP_INFO(this->get_logger(),
                    "[CartesianPoints] Loaded '%s':", name.c_str());
        RCLCPP_INFO(this->get_logger(),
                    "[CartesianPoints]   frame_id: '%s'", pose_stamped.header.frame_id.c_str());
        RCLCPP_INFO(this->get_logger(),
                    "[CartesianPoints]   xyz:      (%.4f, %.4f, %.4f)",
                    pose_stamped.pose.position.x,
                    pose_stamped.pose.position.y,
                    pose_stamped.pose.position.z);
        RCLCPP_INFO(this->get_logger(),
                    "[CartesianPoints]   orientation: fixed (%.6f, %.6f, %.6f, %.6f)",
                    cartesian_quat_.x, cartesian_quat_.y,
                    cartesian_quat_.z, cartesian_quat_.w);
      }

      RCLCPP_INFO(this->get_logger(),
                  "[CartesianPoints] Loaded %zu cartesian points.",
                  named_cartesian_points_.size());
      RCLCPP_INFO(this->get_logger(), "[CartesianPoints] =======================================");
    }
    catch (const YAML::Exception& ex)
    {
      RCLCPP_ERROR(this->get_logger(),
                   "[CartesianPoints] Failed to parse '%s': %s",
                   cartesian_points_config_path_.c_str(), ex.what());
      RCLCPP_INFO(this->get_logger(), "[CartesianPoints] =======================================");
    }
    catch (const std::exception& ex)
    {
      RCLCPP_ERROR(this->get_logger(),
                   "[CartesianPoints] Unexpected error loading '%s': %s",
                   cartesian_points_config_path_.c_str(), ex.what());
      RCLCPP_INFO(this->get_logger(), "[CartesianPoints] =======================================");
    }
  }

  static void rpy_to_quaternion(double roll, double pitch, double yaw,
                                 double& qx, double& qy, double& qz, double& qw)
  {
    double cy = std::cos(yaw   * 0.5);
    double sy = std::sin(yaw   * 0.5);
    double cp = std::cos(pitch * 0.5);
    double sp = std::sin(pitch * 0.5);
    double cr = std::cos(roll  * 0.5);
    double sr = std::sin(roll  * 0.5);

    qw = cr * cp * cy + sr * sp * sy;
    qx = sr * cp * cy - cr * sp * sy;
    qy = cr * sp * cy + sr * cp * sy;
    qz = cr * cp * sy - sr * sp * cy;

    double norm = std::sqrt(qw*qw + qx*qx + qy*qy + qz*qz);
    qw /= norm;
    qx /= norm;
    qy /= norm;
    qz /= norm;
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

  bool move_to_named_pose_target(const std::string& name, bool execute)
  {
    auto it = named_pose_targets_.find(name);
    if (it == named_pose_targets_.end())
    {
      RCLCPP_ERROR(this->get_logger(),
                   "[NamedPoseTarget] Unknown named pose target: '%s'", name.c_str());
      return false;
    }

    const geometry_msgs::msg::PoseStamped& stored_pose = it->second;
    const std::string& requested_frame = stored_pose.header.frame_id;

    RCLCPP_INFO(this->get_logger(),
                "[NamedPoseTarget] =======================================");
    RCLCPP_INFO(this->get_logger(),
                "[NamedPoseTarget] Named pose target: '%s'", name.c_str());
    RCLCPP_INFO(this->get_logger(),
                "[NamedPoseTarget]   frame_id:   '%s'", requested_frame.c_str());
    RCLCPP_INFO(this->get_logger(),
                "[NamedPoseTarget]   position:   (%.4f, %.4f, %.4f)",
                stored_pose.pose.position.x,
                stored_pose.pose.position.y,
                stored_pose.pose.position.z);
    RCLCPP_INFO(this->get_logger(),
                "[NamedPoseTarget]   quaternion: (%.6f, %.6f, %.6f, %.6f)",
                stored_pose.pose.orientation.x,
                stored_pose.pose.orientation.y,
                stored_pose.pose.orientation.z,
                stored_pose.pose.orientation.w);

    const std::string planning_frame = move_group_->getPlanningFrame();
    const std::string pose_ref_frame = move_group_->getPoseReferenceFrame();
    const std::string ee_link = move_group_->getEndEffectorLink();

    geometry_msgs::msg::Pose transformed_pose = stored_pose.pose;
    std::string planning_frame_used;

    if (requested_frame == planning_frame)
    {
      transformed_pose = stored_pose.pose;
      planning_frame_used = planning_frame;
      RCLCPP_INFO(this->get_logger(),
                  "[NamedPoseTarget]   frame_id matches planning_frame '%s' — no TF transform needed.",
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
        pose_stamped_in.pose = stored_pose.pose;

        geometry_msgs::msg::PoseStamped pose_stamped_out =
            tf_buffer_->transform(pose_stamped_in, planning_frame);

        transformed_pose = pose_stamped_out.pose;
        planning_frame_used = planning_frame;

        RCLCPP_INFO(this->get_logger(),
                    "[NamedPoseTarget]   TF transform '%s' -> '%s' succeeded.",
                    requested_frame.c_str(), planning_frame.c_str());
        RCLCPP_INFO(this->get_logger(),
                    "[NamedPoseTarget]   transformed pose xyz:  (%.4f, %.4f, %.4f)",
                    transformed_pose.position.x,
                    transformed_pose.position.y,
                    transformed_pose.position.z);
        RCLCPP_INFO(this->get_logger(),
                    "[NamedPoseTarget]   transformed quat xyzw: (%.6f, %.6f, %.6f, %.6f)",
                    transformed_pose.orientation.x,
                    transformed_pose.orientation.y,
                    transformed_pose.orientation.z,
                    transformed_pose.orientation.w);
      }
      catch (const tf2::TransformException& ex)
      {
        RCLCPP_ERROR(this->get_logger(),
                     "[NamedPoseTarget] TF transform failed: %s", ex.what());
        return false;
      }
    }

    move_group_->setStartStateToCurrentState();
    move_group_->setPoseReferenceFrame(planning_frame_used);
    move_group_->setPlanningTime(planning_time_);
    move_group_->setNumPlanningAttempts(num_planning_attempts_);

    bool set_ok = move_group_->setPoseTarget(transformed_pose, ee_link);
    if (!set_ok)
    {
      RCLCPP_ERROR(this->get_logger(),
                   "[NamedPoseTarget] setPoseTarget() returned false for '%s' on link '%s'",
                   name.c_str(), ee_link.c_str());
      move_group_->clearPoseTargets();
      return false;
    }
    RCLCPP_INFO(this->get_logger(),
                "[NamedPoseTarget] setPoseTarget(pose, '%s') → true", ee_link.c_str());

    moveit::planning_interface::MoveGroupInterface::Plan plan;
    auto plan_result = move_group_->plan(plan);

    if (plan_result != moveit::core::MoveItErrorCode::SUCCESS)
    {
      RCLCPP_ERROR(this->get_logger(),
                   "[NamedPoseTarget] plan() failed for '%s' (error code: %d)",
                   name.c_str(), plan_result.val);
      move_group_->clearPoseTargets();
      return false;
    }
    RCLCPP_INFO(this->get_logger(),
                "[NamedPoseTarget] plan() succeeded for '%s' (%lu trajectory points).",
                name.c_str(), plan.trajectory_.joint_trajectory.points.size());

    if (execute)
    {
      RCLCPP_INFO(this->get_logger(),
                  "[NamedPoseTarget] Executing trajectory for '%s'...", name.c_str());
      auto exec_result = move_group_->execute(plan.trajectory_);
      if (exec_result != moveit::core::MoveItErrorCode::SUCCESS)
      {
        RCLCPP_ERROR(this->get_logger(),
                     "[NamedPoseTarget] execute() failed for '%s' (error code: %d)",
                     name.c_str(), exec_result.val);
        move_group_->clearPoseTargets();
        return false;
      }
      RCLCPP_INFO(this->get_logger(),
                  "[NamedPoseTarget] Execution of '%s' completed successfully.", name.c_str());
    }
    else
    {
      RCLCPP_INFO(this->get_logger(),
                  "[NamedPoseTarget] Plan-only for '%s': trajectory not executed.", name.c_str());
    }

    move_group_->clearPoseTargets();
    RCLCPP_INFO(this->get_logger(),
                "[NamedPoseTarget] =======================================");

    return true;
  }

  bool compute_cartesian_path_waypoints(
      std::vector<geometry_msgs::msg::Pose>& waypoints,
      double eef_step,
      double jump_threshold,
      moveit_msgs::msg::RobotTrajectory& trajectory,
      double& fraction)
  {
    move_group_->setStartStateToCurrentState();

    fraction = move_group_->computeCartesianPath(
        waypoints, eef_step, jump_threshold, trajectory,
        /*avoid_collisions=*/true, nullptr);

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] computeCartesianPath returned fraction=%.4f (%lu trajectory points).",
                fraction, trajectory.joint_trajectory.points.size());

    return fraction >= 0.95;
  }

  bool execute_cartesian_plan(const moveit_msgs::msg::RobotTrajectory& trajectory)
  {
    move_group_->setMaxVelocityScalingFactor(max_velocity_scaling_factor_);
    move_group_->setMaxAccelerationScalingFactor(max_acceleration_scaling_factor_);

    auto exec_result = move_group_->execute(trajectory);
    if (exec_result != moveit::core::MoveItErrorCode::SUCCESS)
    {
      RCLCPP_ERROR(this->get_logger(),
                   "[Cartesian] execute() failed (error code: %d)", exec_result.val);
      return false;
    }
    RCLCPP_INFO(this->get_logger(), "[Cartesian] Execution completed successfully.");
    return true;
  }

  /**
   * Shared helper for Cartesian path computation from named cartesian points.
   *
   * Builds a waypoint list from the named points (transformed to the planning frame)
   * and calls computeCartesianPath.  Crucially, this does NOT prepend the current
   * EE pose — computeCartesianPath with setStartStateToCurrentState() already
   * starts from the robot's current state.
   *
   * Both handle_named_cartesian_target() and handle_cartesian_sequence() use this
   * helper so they produce provably equivalent behavior for a single-element
   * sequence.
   */
  bool compute_named_cartesian_path(
      const std::vector<std::string>& waypoint_names,
      moveit_msgs::msg::RobotTrajectory& trajectory,
      double& fraction)
  {
    const std::string planning_frame = move_group_->getPlanningFrame();

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] Shared path builder — %zu named waypoints:", waypoint_names.size());

    std::vector<geometry_msgs::msg::Pose> waypoints;
    for (size_t i = 0; i < waypoint_names.size(); ++i)
    {
      const std::string& name = waypoint_names[i];
      const geometry_msgs::msg::PoseStamped& stored_pose = named_cartesian_points_.at(name);

      geometry_msgs::msg::PoseStamped transformed =
          transform_pose_to_planning_frame(stored_pose);

      waypoints.push_back(transformed.pose);

      RCLCPP_INFO(this->get_logger(),
                  "[Cartesian]   waypoint[%zu] name='%s'  frame='%s'  "
                  "xyz=(%.4f, %.4f, %.4f)  quat=(%.6f, %.6f, %.6f, %.6f)",
                  i, name.c_str(), planning_frame.c_str(),
                  transformed.pose.position.x,
                  transformed.pose.position.y,
                  transformed.pose.position.z,
                  transformed.pose.orientation.x,
                  transformed.pose.orientation.y,
                  transformed.pose.orientation.z,
                  transformed.pose.orientation.w);
    }

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   total waypoints passed to computeCartesianPath: %zu", waypoints.size());
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   NOTE: computeCartesianPath starts from current EE pose internally "
                "(setStartStateToCurrentState). Do NOT prepend current pose manually — "
                "that would inflate the path length denominator and corrupt the fraction metric.");

    geometry_msgs::msg::Pose current_eef = move_group_->getCurrentPose().pose;
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   current eef xyz: (%.4f, %.4f, %.4f)",
                current_eef.position.x,
                current_eef.position.y,
                current_eef.position.z);

    constexpr double EEF_STEP = 0.01;
    constexpr double JUMP_THRESHOLD = 0.0;

    fraction = move_group_->computeCartesianPath(
        waypoints, EEF_STEP, JUMP_THRESHOLD, trajectory,
        /*avoid_collisions=*/true, nullptr);

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   computeCartesianPath fraction=%.6f  trajectory_points=%lu",
                fraction, trajectory.joint_trajectory.points.size());

    return fraction >= 0.95;
  }

  geometry_msgs::msg::PoseStamped transform_pose_to_planning_frame(
      const geometry_msgs::msg::PoseStamped& input_pose)
  {
    const std::string planning_frame = move_group_->getPlanningFrame();

    if (input_pose.header.frame_id == planning_frame)
    {
      return input_pose;
    }

    geometry_msgs::msg::PoseStamped pose_stamped_in;
    pose_stamped_in.header.stamp = get_clock()->now();
    pose_stamped_in.header.frame_id = input_pose.header.frame_id;
    pose_stamped_in.pose = input_pose.pose;

    geometry_msgs::msg::PoseStamped transformed =
        tf_buffer_->transform(pose_stamped_in, planning_frame);

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] TF transform '%s' -> '%s' succeeded.",
                input_pose.header.frame_id.c_str(), planning_frame.c_str());
    return transformed;
  }

private:
  void init_parameters()
  {
    this->declare_parameter<std::string>("move_group_name", "arm");
    this->declare_parameter<std::string>("base_frame", "world");
    this->declare_parameter<std::string>("ee_link", "tool0");
    this->declare_parameter<std::string>("waypoints_config_path", "");
    this->declare_parameter<std::string>("cartesian_points_config_path", "");
    this->declare_parameter<double>("planning_time", 2.0);
    this->declare_parameter<int>("num_planning_attempts", 5);
    this->declare_parameter<double>("max_velocity_scaling_factor", 0.5);
    this->declare_parameter<double>("max_acceleration_scaling_factor", 0.5);

    this->get_parameter("move_group_name", move_group_name_);
    this->get_parameter("base_frame", base_frame_);
    this->get_parameter("ee_link", ee_link_);
    this->get_parameter("waypoints_config_path", waypoints_config_path_);
    this->get_parameter("cartesian_points_config_path", cartesian_points_config_path_);
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

    service_named_pose_target_ = create_service<gp7_task_executor_msgs::srv::MoveToNamedPoseTarget>(
      "/move_to_named_pose_target",
      [this](
        const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedPoseTarget::Request> request,
        std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedPoseTarget::Response> response)
      {
        handle_named_pose_target(request, response);
      });

    service_cartesian_target_ = create_service<gp7_task_executor_msgs::srv::MoveToCartesianTarget>(
      "/move_to_cartesian_target",
      [this](
        const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToCartesianTarget::Request> request,
        std::shared_ptr<gp7_task_executor_msgs::srv::MoveToCartesianTarget::Response> response)
      {
        handle_cartesian_target(request, response);
      });

    service_named_cartesian_target_ = create_service<gp7_task_executor_msgs::srv::MoveToNamedCartesianTarget>(
      "/move_to_named_cartesian_target",
      [this](
        const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedCartesianTarget::Request> request,
        std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedCartesianTarget::Response> response)
      {
        handle_named_cartesian_target(request, response);
      });

    service_cartesian_sequence_ = create_service<gp7_task_executor_msgs::srv::MoveCartesianSequence>(
      "/move_cartesian_sequence",
      [this](
        const std::shared_ptr<gp7_task_executor_msgs::srv::MoveCartesianSequence::Request> request,
        std::shared_ptr<gp7_task_executor_msgs::srv::MoveCartesianSequence::Response> response)
      {
        handle_cartesian_sequence(request, response);
      });

    service_move_sequence_ = create_service<gp7_task_executor_msgs::srv::MoveSequence>(
      "/move_sequence",
      [this](
        const std::shared_ptr<gp7_task_executor_msgs::srv::MoveSequence::Request> request,
        std::shared_ptr<gp7_task_executor_msgs::srv::MoveSequence::Response> response)
      {
        handle_move_sequence(request, response);
      });

    RCLCPP_INFO(this->get_logger(),
                "Services created: /move_to_named_target, /move_to_joint_target, "
                "/move_to_pose_target, /move_to_named_pose_target, "
                "/move_to_cartesian_target, /move_to_named_cartesian_target, "
                "/move_cartesian_sequence, /move_sequence");
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

  void handle_named_pose_target(
    const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedPoseTarget::Request> request,
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedPoseTarget::Response> response)
  {
    const std::string& target_name = request->target_name;
    bool execute = request->execute;

    if (target_name.empty())
    {
      response->success = false;
      response->message = "target_name is empty";
      RCLCPP_WARN(this->get_logger(),
                  "[NamedPoseTarget] %s", response->message.c_str());
      return;
    }

    bool ok = move_to_named_pose_target(target_name, execute);
    response->success = ok;
    response->message = ok
      ? "Named pose target '" + target_name + "' " + (execute ? "executed" : "planned") + " successfully"
      : "Failed to " + std::string(execute ? "plan/execute" : "plan") + " named pose target '" + target_name + "'";
  }

  void handle_cartesian_target(
    const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToCartesianTarget::Request> request,
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToCartesianTarget::Response> response)
  {
    double x = request->x;
    double y = request->y;
    double z = request->z;
    const std::string& frame_id = request->frame_id;
    bool execute = request->execute;

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] =======================================");
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] /move_to_cartesian_target  (execute=%d)", execute);
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   frame_id:   '%s'", frame_id.c_str());
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   position:   (%.4f, %.4f, %.4f)", x, y, z);
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   orientation: FIXED (roll=pi, pitch=0, yaw=0)");
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   quaternion: (%.6f, %.6f, %.6f, %.6f)",
                cartesian_quat_.x, cartesian_quat_.y,
                cartesian_quat_.z, cartesian_quat_.w);

    if (frame_id.empty())
    {
      response->success = false;
      response->message = "frame_id must not be empty";
      response->fraction = 0.0;
      RCLCPP_WARN(this->get_logger(), "[Cartesian] %s", response->message.c_str());
      return;
    }

    geometry_msgs::msg::PoseStamped target_pose_stamped;
    target_pose_stamped.header.stamp = get_clock()->now();
    target_pose_stamped.header.frame_id = frame_id;
    target_pose_stamped.pose.position.x = x;
    target_pose_stamped.pose.position.y = y;
    target_pose_stamped.pose.position.z = z;
    target_pose_stamped.pose.orientation = cartesian_quat_;

    geometry_msgs::msg::PoseStamped target_in_planning_frame =
        transform_pose_to_planning_frame(target_pose_stamped);
    geometry_msgs::msg::Pose target_pose = target_in_planning_frame.pose;

    geometry_msgs::msg::Pose current_eef_pose = move_group_->getCurrentPose().pose;

    std::vector<geometry_msgs::msg::Pose> waypoints;
    waypoints.push_back(target_pose);

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   current eef xyz:   (%.4f, %.4f, %.4f)",
                current_eef_pose.position.x,
                current_eef_pose.position.y,
                current_eef_pose.position.z);
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   target eef xyz:     (%.4f, %.4f, %.4f)",
                target_pose.position.x,
                target_pose.position.y,
                target_pose.position.z);
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   waypoint count:     %zu", waypoints.size());

    moveit_msgs::msg::RobotTrajectory trajectory;
    double fraction = 0.0;

    constexpr double EEF_STEP = 0.01;
    constexpr double JUMP_THRESHOLD = 0.0;

    bool path_ok = compute_cartesian_path_waypoints(
        waypoints, EEF_STEP, JUMP_THRESHOLD, trajectory, fraction);

    response->fraction = fraction;

    if (!path_ok)
    {
      response->success = false;
      response->message = "Cartesian path computation failed or returned fraction < 0.95 (fraction=" +
                           std::to_string(fraction) + "). Check for singularities or unreachable targets.";
      RCLCPP_ERROR(this->get_logger(), "[Cartesian] %s", response->message.c_str());
      return;
    }

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] Cartesian path computed: fraction=%.4f, points=%lu, execute=%d",
                fraction, trajectory.joint_trajectory.points.size(), execute);

    if (execute)
    {
      bool exec_ok = execute_cartesian_plan(trajectory);
      response->success = exec_ok;
      response->message = exec_ok
        ? "Cartesian target executed successfully (fraction=" + std::to_string(fraction) + ")"
        : "Cartesian path computed (fraction=" + std::to_string(fraction) + ") but execution failed";
    }
    else
    {
      response->success = true;
      response->message = "Cartesian path planned successfully (fraction=" + std::to_string(fraction) +
                          "), execution skipped (plan-only mode)";
      RCLCPP_INFO(this->get_logger(),
                  "[Cartesian] Plan-only: trajectory not executed.");
    }

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] =======================================");
  }

  void handle_named_cartesian_target(
    const std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedCartesianTarget::Request> request,
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveToNamedCartesianTarget::Response> response)
  {
    const std::string& target_name = request->target_name;
    bool execute = request->execute;

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] =======================================");
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] /move_to_named_cartesian_target  target='%s'  (execute=%d)",
                target_name.c_str(), execute);

    if (target_name.empty())
    {
      response->success = false;
      response->message = "target_name is empty";
      response->fraction = 0.0;
      RCLCPP_WARN(this->get_logger(), "[Cartesian] %s", response->message.c_str());
      return;
    }

    if (named_cartesian_points_.find(target_name) == named_cartesian_points_.end())
    {
      response->success = false;
      response->message = "Unknown cartesian point: '" + target_name +
                          "'. Available: " + available_cartesian_point_names();
      response->fraction = 0.0;
      RCLCPP_ERROR(this->get_logger(), "[Cartesian] %s", response->message.c_str());
      return;
    }

    const geometry_msgs::msg::PoseStamped& stored_pose = named_cartesian_points_.at(target_name);
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   frame_id:   '%s'", stored_pose.header.frame_id.c_str());
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   xyz:        (%.4f, %.4f, %.4f)",
                stored_pose.pose.position.x,
                stored_pose.pose.position.y,
                stored_pose.pose.position.z);
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian]   orientation: FIXED (roll=pi, pitch=0, yaw=0)  quat=(%.6f, %.6f, %.6f, %.6f)",
                cartesian_quat_.x, cartesian_quat_.y,
                cartesian_quat_.z, cartesian_quat_.w);

    std::vector<std::string> waypoint_names = {target_name};

    moveit_msgs::msg::RobotTrajectory trajectory;
    double fraction = 0.0;

    bool path_ok = compute_named_cartesian_path(waypoint_names, trajectory, fraction);

    response->fraction = fraction;

    if (!path_ok)
    {
      response->success = false;
      response->message = "Cartesian path computation failed or returned fraction < 0.95 (fraction=" +
                           std::to_string(fraction) + "). Check for singularities or unreachable targets.";
      RCLCPP_ERROR(this->get_logger(), "[Cartesian] %s", response->message.c_str());
      return;
    }

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] Cartesian path computed: fraction=%.4f, points=%lu, execute=%d",
                fraction, trajectory.joint_trajectory.points.size(), execute);

    if (execute)
    {
      bool exec_ok = execute_cartesian_plan(trajectory);
      response->success = exec_ok;
      response->message = exec_ok
        ? "Named Cartesian target '" + target_name + "' executed successfully (fraction=" +
          std::to_string(fraction) + ")"
        : "Cartesian path computed (fraction=" + std::to_string(fraction) +
          ") but execution failed";
    }
    else
    {
      response->success = true;
      response->message = "Named Cartesian target '" + target_name +
                          "' planned successfully (fraction=" + std::to_string(fraction) +
                          "), execution skipped (plan-only mode)";
      RCLCPP_INFO(this->get_logger(),
                  "[Cartesian] Plan-only: trajectory not executed.");
    }

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] =======================================");
  }

  void handle_cartesian_sequence(
    const std::shared_ptr<gp7_task_executor_msgs::srv::MoveCartesianSequence::Request> request,
    std::shared_ptr<gp7_task_executor_msgs::srv::MoveCartesianSequence::Response> response)
  {
    const auto& waypoint_names = request->waypoint_names;
    bool execute = request->execute;

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] =======================================");
    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] /move_cartesian_sequence  (execute=%d)", execute);

    if (waypoint_names.empty())
    {
      response->success = false;
      response->message = "Empty sequence: waypoint_names must not be empty";
      response->fraction = 0.0;
      RCLCPP_WARN(this->get_logger(), "[Cartesian] %s", response->message.c_str());
      return;
    }

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] Sequence with %lu waypoints:", waypoint_names.size());
    for (size_t i = 0; i < waypoint_names.size(); ++i)
    {
      RCLCPP_INFO(this->get_logger(), "  step %zu: '%s'", i + 1, waypoint_names[i].c_str());
    }

    for (const auto& name : waypoint_names)
    {
      if (named_cartesian_points_.find(name) == named_cartesian_points_.end())
      {
        response->success = false;
        response->message = "Unknown cartesian point '" + name +
                            "' in sequence. Available: " + available_cartesian_point_names();
        response->fraction = 0.0;
        RCLCPP_ERROR(this->get_logger(), "[Cartesian] %s", response->message.c_str());
        return;
      }
    }

    moveit_msgs::msg::RobotTrajectory trajectory;
    double fraction = 0.0;

    bool path_ok = compute_named_cartesian_path(waypoint_names, trajectory, fraction);

    response->fraction = fraction;

    if (!path_ok)
    {
      response->success = false;
      response->message = "Cartesian sequence path computation failed or returned fraction < 0.95 (fraction=" +
                           std::to_string(fraction) + "). Some poses may be unreachable or in singularity.";
      RCLCPP_ERROR(this->get_logger(), "[Cartesian] %s", response->message.c_str());
      return;
    }

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] Cartesian sequence path computed: fraction=%.4f, points=%lu, execute=%d",
                fraction, trajectory.joint_trajectory.points.size(), execute);

    if (execute)
    {
      bool exec_ok = execute_cartesian_plan(trajectory);
      response->success = exec_ok;
      response->message = exec_ok
        ? "Cartesian sequence executed successfully (" + std::to_string(waypoint_names.size()) +
          " waypoints, fraction=" + std::to_string(fraction) + ")"
        : "Cartesian sequence path computed (fraction=" + std::to_string(fraction) +
          ") but execution failed";
    }
    else
    {
      response->success = true;
      response->message = "Cartesian sequence planned successfully (" +
                          std::to_string(waypoint_names.size()) +
                          " waypoints, fraction=" + std::to_string(fraction) +
                          "), execution skipped (plan-only mode)";
      RCLCPP_INFO(this->get_logger(),
                  "[Cartesian] Plan-only: trajectory not executed.");
    }

    RCLCPP_INFO(this->get_logger(),
                "[Cartesian] =======================================");
  }

  std::string available_cartesian_point_names() const
  {
    if (named_cartesian_points_.empty())
      return "(none loaded)";
    std::string names;
    for (auto it = named_cartesian_points_.begin(); it != named_cartesian_points_.end(); ++it)
    {
      if (!names.empty()) names += ", ";
      names += "'" + it->first + "'";
    }
    return names;
  }

  std::string move_group_name_;
  std::string base_frame_;
  std::string ee_link_;
  std::string waypoints_config_path_;
  std::string cartesian_points_config_path_;
  double planning_time_;
  int num_planning_attempts_;
  double max_velocity_scaling_factor_;
  double max_acceleration_scaling_factor_;

  geometry_msgs::msg::Quaternion cartesian_quat_;

  std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
  std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
  std::shared_ptr<tf2_ros::TransformListener> tf_listener_;

  rclcpp::Service<gp7_task_executor_msgs::srv::MoveToNamedTarget>::SharedPtr service_named_target_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveToJointTarget>::SharedPtr service_joint_target_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveToPoseTarget>::SharedPtr service_pose_target_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveToNamedPoseTarget>::SharedPtr service_named_pose_target_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveToCartesianTarget>::SharedPtr service_cartesian_target_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveToNamedCartesianTarget>::SharedPtr service_named_cartesian_target_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveCartesianSequence>::SharedPtr service_cartesian_sequence_;
  rclcpp::Service<gp7_task_executor_msgs::srv::MoveSequence>::SharedPtr service_move_sequence_;

  std::map<std::string, std::vector<double>> named_joint_targets_;
  std::map<std::string, geometry_msgs::msg::PoseStamped> named_cartesian_points_;
  std::map<std::string, geometry_msgs::msg::PoseStamped> named_pose_targets_;
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
