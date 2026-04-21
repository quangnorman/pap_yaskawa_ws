// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from gp7_vision_pipeline:msg/BoxDetection.idl
// generated code does not contain a copyright notice

#ifndef GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "gp7_vision_pipeline/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "gp7_vision_pipeline/msg/detail/box_detection__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace gp7_vision_pipeline
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gp7_vision_pipeline
cdr_serialize(
  const gp7_vision_pipeline::msg::BoxDetection & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gp7_vision_pipeline
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  gp7_vision_pipeline::msg::BoxDetection & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gp7_vision_pipeline
get_serialized_size(
  const gp7_vision_pipeline::msg::BoxDetection & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gp7_vision_pipeline
max_serialized_size_BoxDetection(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace gp7_vision_pipeline

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_gp7_vision_pipeline
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, gp7_vision_pipeline, msg, BoxDetection)();

#ifdef __cplusplus
}
#endif

#endif  // GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
