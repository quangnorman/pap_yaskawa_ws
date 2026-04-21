// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from gp7_task_executor_msgs:srv/MoveToPoseTarget.idl
// generated code does not contain a copyright notice

#ifndef GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_POSE_TARGET__BUILDER_HPP_
#define GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_POSE_TARGET__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "gp7_task_executor_msgs/srv/detail/move_to_pose_target__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace gp7_task_executor_msgs
{

namespace srv
{

namespace builder
{

class Init_MoveToPoseTarget_Request_execute
{
public:
  explicit Init_MoveToPoseTarget_Request_execute(::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request & msg)
  : msg_(msg)
  {}
  ::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request execute(::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request::_execute_type arg)
  {
    msg_.execute = std::move(arg);
    return std::move(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request msg_;
};

class Init_MoveToPoseTarget_Request_frame_id
{
public:
  explicit Init_MoveToPoseTarget_Request_frame_id(::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request & msg)
  : msg_(msg)
  {}
  Init_MoveToPoseTarget_Request_execute frame_id(::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_MoveToPoseTarget_Request_execute(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request msg_;
};

class Init_MoveToPoseTarget_Request_pose
{
public:
  Init_MoveToPoseTarget_Request_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveToPoseTarget_Request_frame_id pose(::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request::_pose_type arg)
  {
    msg_.pose = std::move(arg);
    return Init_MoveToPoseTarget_Request_frame_id(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::gp7_task_executor_msgs::srv::MoveToPoseTarget_Request>()
{
  return gp7_task_executor_msgs::srv::builder::Init_MoveToPoseTarget_Request_pose();
}

}  // namespace gp7_task_executor_msgs


namespace gp7_task_executor_msgs
{

namespace srv
{

namespace builder
{

class Init_MoveToPoseTarget_Response_message
{
public:
  explicit Init_MoveToPoseTarget_Response_message(::gp7_task_executor_msgs::srv::MoveToPoseTarget_Response & msg)
  : msg_(msg)
  {}
  ::gp7_task_executor_msgs::srv::MoveToPoseTarget_Response message(::gp7_task_executor_msgs::srv::MoveToPoseTarget_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToPoseTarget_Response msg_;
};

class Init_MoveToPoseTarget_Response_success
{
public:
  Init_MoveToPoseTarget_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveToPoseTarget_Response_message success(::gp7_task_executor_msgs::srv::MoveToPoseTarget_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MoveToPoseTarget_Response_message(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToPoseTarget_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::gp7_task_executor_msgs::srv::MoveToPoseTarget_Response>()
{
  return gp7_task_executor_msgs::srv::builder::Init_MoveToPoseTarget_Response_success();
}

}  // namespace gp7_task_executor_msgs

#endif  // GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_POSE_TARGET__BUILDER_HPP_
