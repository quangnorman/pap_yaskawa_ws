// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from gp7_vision_pipeline:msg/BoxDetection.idl
// generated code does not contain a copyright notice

#ifndef GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__STRUCT_H_
#define GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'class_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/BoxDetection in the package gp7_vision_pipeline.
typedef struct gp7_vision_pipeline__msg__BoxDetection
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String class_name;
  float confidence;
  int32_t x_min;
  int32_t y_min;
  int32_t x_max;
  int32_t y_max;
  int32_t center_x;
  int32_t center_y;
  int32_t width_px;
  int32_t height_px;
  float distance_m;
} gp7_vision_pipeline__msg__BoxDetection;

// Struct for a sequence of gp7_vision_pipeline__msg__BoxDetection.
typedef struct gp7_vision_pipeline__msg__BoxDetection__Sequence
{
  gp7_vision_pipeline__msg__BoxDetection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gp7_vision_pipeline__msg__BoxDetection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GP7_VISION_PIPELINE__MSG__DETAIL__BOX_DETECTION__STRUCT_H_
