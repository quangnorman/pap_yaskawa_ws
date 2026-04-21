// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from gp7_task_executor_msgs:srv/MoveToJointTarget.idl
// generated code does not contain a copyright notice

#ifndef GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_JOINT_TARGET__BUILDER_HPP_
#define GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_JOINT_TARGET__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "gp7_task_executor_msgs/srv/detail/move_to_joint_target__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace gp7_task_executor_msgs
{

namespace srv
{

namespace builder
{

class Init_MoveToJointTarget_Request_execute
{
public:
  explicit Init_MoveToJointTarget_Request_execute(::gp7_task_executor_msgs::srv::MoveToJointTarget_Request & msg)
  : msg_(msg)
  {}
  ::gp7_task_executor_msgs::srv::MoveToJointTarget_Request execute(::gp7_task_executor_msgs::srv::MoveToJointTarget_Request::_execute_type arg)
  {
    msg_.execute = std::move(arg);
    return std::move(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToJointTarget_Request msg_;
};

class Init_MoveToJointTarget_Request_positions
{
public:
  explicit Init_MoveToJointTarget_Request_positions(::gp7_task_executor_msgs::srv::MoveToJointTarget_Request & msg)
  : msg_(msg)
  {}
  Init_MoveToJointTarget_Request_execute positions(::gp7_task_executor_msgs::srv::MoveToJointTarget_Request::_positions_type arg)
  {
    msg_.positions = std::move(arg);
    return Init_MoveToJointTarget_Request_execute(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToJointTarget_Request msg_;
};

class Init_MoveToJointTarget_Request_joint_names
{
public:
  Init_MoveToJointTarget_Request_joint_names()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveToJointTarget_Request_positions joint_names(::gp7_task_executor_msgs::srv::MoveToJointTarget_Request::_joint_names_type arg)
  {
    msg_.joint_names = std::move(arg);
    return Init_MoveToJointTarget_Request_positions(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToJointTarget_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::gp7_task_executor_msgs::srv::MoveToJointTarget_Request>()
{
  return gp7_task_executor_msgs::srv::builder::Init_MoveToJointTarget_Request_joint_names();
}

}  // namespace gp7_task_executor_msgs


namespace gp7_task_executor_msgs
{

namespace srv
{

namespace builder
{

class Init_MoveToJointTarget_Response_message
{
public:
  explicit Init_MoveToJointTarget_Response_message(::gp7_task_executor_msgs::srv::MoveToJointTarget_Response & msg)
  : msg_(msg)
  {}
  ::gp7_task_executor_msgs::srv::MoveToJointTarget_Response message(::gp7_task_executor_msgs::srv::MoveToJointTarget_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToJointTarget_Response msg_;
};

class Init_MoveToJointTarget_Response_success
{
public:
  Init_MoveToJointTarget_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveToJointTarget_Response_message success(::gp7_task_executor_msgs::srv::MoveToJointTarget_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MoveToJointTarget_Response_message(msg_);
  }

private:
  ::gp7_task_executor_msgs::srv::MoveToJointTarget_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::gp7_task_executor_msgs::srv::MoveToJointTarget_Response>()
{
  return gp7_task_executor_msgs::srv::builder::Init_MoveToJointTarget_Response_success();
}

}  // namespace gp7_task_executor_msgs

#endif  // GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_JOINT_TARGET__BUILDER_HPP_
