// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from gp7_task_executor_msgs:srv/MoveToNamedTarget.idl
// generated code does not contain a copyright notice

#ifndef GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_NAMED_TARGET__TRAITS_HPP_
#define GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_NAMED_TARGET__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "gp7_task_executor_msgs/srv/detail/move_to_named_target__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace gp7_task_executor_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveToNamedTarget_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_name
  {
    out << "target_name: ";
    rosidl_generator_traits::value_to_yaml(msg.target_name, out);
    out << ", ";
  }

  // member: execute
  {
    out << "execute: ";
    rosidl_generator_traits::value_to_yaml(msg.execute, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveToNamedTarget_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_name: ";
    rosidl_generator_traits::value_to_yaml(msg.target_name, out);
    out << "\n";
  }

  // member: execute
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "execute: ";
    rosidl_generator_traits::value_to_yaml(msg.execute, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveToNamedTarget_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace gp7_task_executor_msgs

namespace rosidl_generator_traits
{

[[deprecated("use gp7_task_executor_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const gp7_task_executor_msgs::srv::MoveToNamedTarget_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  gp7_task_executor_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use gp7_task_executor_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const gp7_task_executor_msgs::srv::MoveToNamedTarget_Request & msg)
{
  return gp7_task_executor_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<gp7_task_executor_msgs::srv::MoveToNamedTarget_Request>()
{
  return "gp7_task_executor_msgs::srv::MoveToNamedTarget_Request";
}

template<>
inline const char * name<gp7_task_executor_msgs::srv::MoveToNamedTarget_Request>()
{
  return "gp7_task_executor_msgs/srv/MoveToNamedTarget_Request";
}

template<>
struct has_fixed_size<gp7_task_executor_msgs::srv::MoveToNamedTarget_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<gp7_task_executor_msgs::srv::MoveToNamedTarget_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<gp7_task_executor_msgs::srv::MoveToNamedTarget_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace gp7_task_executor_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveToNamedTarget_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveToNamedTarget_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveToNamedTarget_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace gp7_task_executor_msgs

namespace rosidl_generator_traits
{

[[deprecated("use gp7_task_executor_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const gp7_task_executor_msgs::srv::MoveToNamedTarget_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  gp7_task_executor_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use gp7_task_executor_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const gp7_task_executor_msgs::srv::MoveToNamedTarget_Response & msg)
{
  return gp7_task_executor_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<gp7_task_executor_msgs::srv::MoveToNamedTarget_Response>()
{
  return "gp7_task_executor_msgs::srv::MoveToNamedTarget_Response";
}

template<>
inline const char * name<gp7_task_executor_msgs::srv::MoveToNamedTarget_Response>()
{
  return "gp7_task_executor_msgs/srv/MoveToNamedTarget_Response";
}

template<>
struct has_fixed_size<gp7_task_executor_msgs::srv::MoveToNamedTarget_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<gp7_task_executor_msgs::srv::MoveToNamedTarget_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<gp7_task_executor_msgs::srv::MoveToNamedTarget_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<gp7_task_executor_msgs::srv::MoveToNamedTarget>()
{
  return "gp7_task_executor_msgs::srv::MoveToNamedTarget";
}

template<>
inline const char * name<gp7_task_executor_msgs::srv::MoveToNamedTarget>()
{
  return "gp7_task_executor_msgs/srv/MoveToNamedTarget";
}

template<>
struct has_fixed_size<gp7_task_executor_msgs::srv::MoveToNamedTarget>
  : std::integral_constant<
    bool,
    has_fixed_size<gp7_task_executor_msgs::srv::MoveToNamedTarget_Request>::value &&
    has_fixed_size<gp7_task_executor_msgs::srv::MoveToNamedTarget_Response>::value
  >
{
};

template<>
struct has_bounded_size<gp7_task_executor_msgs::srv::MoveToNamedTarget>
  : std::integral_constant<
    bool,
    has_bounded_size<gp7_task_executor_msgs::srv::MoveToNamedTarget_Request>::value &&
    has_bounded_size<gp7_task_executor_msgs::srv::MoveToNamedTarget_Response>::value
  >
{
};

template<>
struct is_service<gp7_task_executor_msgs::srv::MoveToNamedTarget>
  : std::true_type
{
};

template<>
struct is_service_request<gp7_task_executor_msgs::srv::MoveToNamedTarget_Request>
  : std::true_type
{
};

template<>
struct is_service_response<gp7_task_executor_msgs::srv::MoveToNamedTarget_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_TO_NAMED_TARGET__TRAITS_HPP_
