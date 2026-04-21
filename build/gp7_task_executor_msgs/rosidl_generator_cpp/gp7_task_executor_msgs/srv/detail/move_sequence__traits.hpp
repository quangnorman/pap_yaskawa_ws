// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from gp7_task_executor_msgs:srv/MoveSequence.idl
// generated code does not contain a copyright notice

#ifndef GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_SEQUENCE__TRAITS_HPP_
#define GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_SEQUENCE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "gp7_task_executor_msgs/srv/detail/move_sequence__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace gp7_task_executor_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveSequence_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: waypoint_names
  {
    if (msg.waypoint_names.size() == 0) {
      out << "waypoint_names: []";
    } else {
      out << "waypoint_names: [";
      size_t pending_items = msg.waypoint_names.size();
      for (auto item : msg.waypoint_names) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
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
  const MoveSequence_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: waypoint_names
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.waypoint_names.size() == 0) {
      out << "waypoint_names: []\n";
    } else {
      out << "waypoint_names:\n";
      for (auto item : msg.waypoint_names) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
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

inline std::string to_yaml(const MoveSequence_Request & msg, bool use_flow_style = false)
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
  const gp7_task_executor_msgs::srv::MoveSequence_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  gp7_task_executor_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use gp7_task_executor_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const gp7_task_executor_msgs::srv::MoveSequence_Request & msg)
{
  return gp7_task_executor_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<gp7_task_executor_msgs::srv::MoveSequence_Request>()
{
  return "gp7_task_executor_msgs::srv::MoveSequence_Request";
}

template<>
inline const char * name<gp7_task_executor_msgs::srv::MoveSequence_Request>()
{
  return "gp7_task_executor_msgs/srv/MoveSequence_Request";
}

template<>
struct has_fixed_size<gp7_task_executor_msgs::srv::MoveSequence_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<gp7_task_executor_msgs::srv::MoveSequence_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<gp7_task_executor_msgs::srv::MoveSequence_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace gp7_task_executor_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveSequence_Response & msg,
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
  const MoveSequence_Response & msg,
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

inline std::string to_yaml(const MoveSequence_Response & msg, bool use_flow_style = false)
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
  const gp7_task_executor_msgs::srv::MoveSequence_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  gp7_task_executor_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use gp7_task_executor_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const gp7_task_executor_msgs::srv::MoveSequence_Response & msg)
{
  return gp7_task_executor_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<gp7_task_executor_msgs::srv::MoveSequence_Response>()
{
  return "gp7_task_executor_msgs::srv::MoveSequence_Response";
}

template<>
inline const char * name<gp7_task_executor_msgs::srv::MoveSequence_Response>()
{
  return "gp7_task_executor_msgs/srv/MoveSequence_Response";
}

template<>
struct has_fixed_size<gp7_task_executor_msgs::srv::MoveSequence_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<gp7_task_executor_msgs::srv::MoveSequence_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<gp7_task_executor_msgs::srv::MoveSequence_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<gp7_task_executor_msgs::srv::MoveSequence>()
{
  return "gp7_task_executor_msgs::srv::MoveSequence";
}

template<>
inline const char * name<gp7_task_executor_msgs::srv::MoveSequence>()
{
  return "gp7_task_executor_msgs/srv/MoveSequence";
}

template<>
struct has_fixed_size<gp7_task_executor_msgs::srv::MoveSequence>
  : std::integral_constant<
    bool,
    has_fixed_size<gp7_task_executor_msgs::srv::MoveSequence_Request>::value &&
    has_fixed_size<gp7_task_executor_msgs::srv::MoveSequence_Response>::value
  >
{
};

template<>
struct has_bounded_size<gp7_task_executor_msgs::srv::MoveSequence>
  : std::integral_constant<
    bool,
    has_bounded_size<gp7_task_executor_msgs::srv::MoveSequence_Request>::value &&
    has_bounded_size<gp7_task_executor_msgs::srv::MoveSequence_Response>::value
  >
{
};

template<>
struct is_service<gp7_task_executor_msgs::srv::MoveSequence>
  : std::true_type
{
};

template<>
struct is_service_request<gp7_task_executor_msgs::srv::MoveSequence_Request>
  : std::true_type
{
};

template<>
struct is_service_response<gp7_task_executor_msgs::srv::MoveSequence_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // GP7_TASK_EXECUTOR_MSGS__SRV__DETAIL__MOVE_SEQUENCE__TRAITS_HPP_
