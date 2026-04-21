// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from gp7_vision_pipeline:msg/BoxDetection.idl
// generated code does not contain a copyright notice

#ifndef GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__TRAITS_HPP_
#define GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "gp7_vision_pipeline/msg/detail/box_detection__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace gp7_vision_pipeline
{

namespace msg
{

inline void to_flow_style_yaml(
  const BoxDetection & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: class_name
  {
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: x_min
  {
    out << "x_min: ";
    rosidl_generator_traits::value_to_yaml(msg.x_min, out);
    out << ", ";
  }

  // member: y_min
  {
    out << "y_min: ";
    rosidl_generator_traits::value_to_yaml(msg.y_min, out);
    out << ", ";
  }

  // member: x_max
  {
    out << "x_max: ";
    rosidl_generator_traits::value_to_yaml(msg.x_max, out);
    out << ", ";
  }

  // member: y_max
  {
    out << "y_max: ";
    rosidl_generator_traits::value_to_yaml(msg.y_max, out);
    out << ", ";
  }

  // member: center_x
  {
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << ", ";
  }

  // member: center_y
  {
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
    out << ", ";
  }

  // member: width_px
  {
    out << "width_px: ";
    rosidl_generator_traits::value_to_yaml(msg.width_px, out);
    out << ", ";
  }

  // member: height_px
  {
    out << "height_px: ";
    rosidl_generator_traits::value_to_yaml(msg.height_px, out);
    out << ", ";
  }

  // member: distance_m
  {
    out << "distance_m: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_m, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const BoxDetection & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: class_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "class_name: ";
    rosidl_generator_traits::value_to_yaml(msg.class_name, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }

  // member: x_min
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x_min: ";
    rosidl_generator_traits::value_to_yaml(msg.x_min, out);
    out << "\n";
  }

  // member: y_min
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y_min: ";
    rosidl_generator_traits::value_to_yaml(msg.y_min, out);
    out << "\n";
  }

  // member: x_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x_max: ";
    rosidl_generator_traits::value_to_yaml(msg.x_max, out);
    out << "\n";
  }

  // member: y_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y_max: ";
    rosidl_generator_traits::value_to_yaml(msg.y_max, out);
    out << "\n";
  }

  // member: center_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_x: ";
    rosidl_generator_traits::value_to_yaml(msg.center_x, out);
    out << "\n";
  }

  // member: center_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "center_y: ";
    rosidl_generator_traits::value_to_yaml(msg.center_y, out);
    out << "\n";
  }

  // member: width_px
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width_px: ";
    rosidl_generator_traits::value_to_yaml(msg.width_px, out);
    out << "\n";
  }

  // member: height_px
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height_px: ";
    rosidl_generator_traits::value_to_yaml(msg.height_px, out);
    out << "\n";
  }

  // member: distance_m
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance_m: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_m, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const BoxDetection & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace gp7_vision_pipeline

namespace rosidl_generator_traits
{

[[deprecated("use gp7_vision_pipeline::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const gp7_vision_pipeline::msg::BoxDetection & msg,
  std::ostream & out, size_t indentation = 0)
{
  gp7_vision_pipeline::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use gp7_vision_pipeline::msg::to_yaml() instead")]]
inline std::string to_yaml(const gp7_vision_pipeline::msg::BoxDetection & msg)
{
  return gp7_vision_pipeline::msg::to_yaml(msg);
}

template<>
inline const char * data_type<gp7_vision_pipeline::msg::BoxDetection>()
{
  return "gp7_vision_pipeline::msg::BoxDetection";
}

template<>
inline const char * name<gp7_vision_pipeline::msg::BoxDetection>()
{
  return "gp7_vision_pipeline/msg/BoxDetection";
}

template<>
struct has_fixed_size<gp7_vision_pipeline::msg::BoxDetection>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<gp7_vision_pipeline::msg::BoxDetection>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<gp7_vision_pipeline::msg::BoxDetection>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__TRAITS_HPP_
